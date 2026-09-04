import zipfile
import tempfile
from pathlib import Path
from io import BytesIO

import grpc

from internal.app.excel.parser import parse_contractors
from internal.app.docx.renderer import render_documents
from internal.app.excel.reader import read_excel
from internal.app.exceptions import GeneratorError, ErrorCode


def generate_from_archive(archive_bytes: bytes) -> tuple[bytes, dict[str, list[Exception]], int]:

    all_exceptions = {}

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        with zipfile.ZipFile(BytesIO(archive_bytes)) as zf:
            zf.extractall(tmp_path)

        excel_files = list(tmp_path.glob("**/*.xlsx")) + list(tmp_path.glob("**/*.xls"))
        if not excel_files:
            raise GeneratorError(
                message="No Excel file (.xlsx/.xls) found in archive",
                code=ErrorCode.EXCEL_NOT_FOUND,
                grpc_code=grpc.StatusCode.INVALID_ARGUMENT
            )
        excel_path = excel_files[0]

        template_files = list(tmp_path.glob("**/*.docx"))
        if not template_files:
            raise GeneratorError(
                message="No .docx template files found in archive",
                code=ErrorCode.TEMPLATE_NOT_FOUND,
                grpc_code=grpc.StatusCode.INVALID_ARGUMENT
            )
        templates = [(f.name, f.read_bytes()) for f in template_files]

        images = {}
        all_images = list(tmp_path.glob("**/*.png")) + list(tmp_path.glob("**/*.jpg")) + list(
            tmp_path.glob("**/*.jpeg"))
        for img_path in all_images:
            images[img_path.stem] = img_path.read_bytes()

        df = read_excel(excel_path)
        contractors = parse_contractors(df)

        if not contractors:
            raise GeneratorError(
                message="No contractors found in Excel",
                code=ErrorCode.NO_CONTRACTORS,
                grpc_code=grpc.StatusCode.INVALID_ARGUMENT
            )

        all_results = {}
        for contractor in contractors:
            context = contractor.fields.copy()

            template_name = context.get("Template")
            chosen_templates = []
            if template_name:
                for fname, fbytes in templates:
                    if Path(fname).stem == template_name:
                        chosen_templates.append((fname, fbytes))
                        break
                else:
                    chosen_templates = [templates[0]]
            else:
                chosen_templates = templates

            rendered, exceptions = render_documents(
                context=context,
                template_files=chosen_templates,
                images=images,
                image_width_mm=180,
                output_filename_template="{contractor}_{template}.docx"
            )
            all_results.update(rendered)
            all_exceptions.update(exceptions)

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            for filename, content in all_results.items():
                zf.writestr(filename, content)
        return zip_buffer.getvalue(), all_exceptions, len(all_results)