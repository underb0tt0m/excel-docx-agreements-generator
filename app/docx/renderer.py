import time
from datetime import datetime
from io import BytesIO
from pathlib import Path

import grpc
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import tempfile
from PIL import Image

from app.exceptions import GeneratorError, ErrorCode


def generate_placeholder_png(size=(100, 100), color='red') -> bytes:
    img = Image.new('RGB', size, color=color)
    output = BytesIO()
    img.save(output, format='PNG')
    return output.getvalue()


def render_template(
        template_bytes: bytes,
        context: dict,
        images: dict[str, bytes] = None,
        image_width_mm: int = 180,
) -> tuple[bytes, list[Exception]]:
    exceptions = []

    if images is None:
        images = {}

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_dir = Path(tmpdir)

        template_path = tmp_dir / "template.docx"
        template_path.write_bytes(template_bytes)

        doc = DocxTemplate(str(template_path))
        render_context = context.copy()
        image_keys = [k for k in render_context.keys() if k.startswith('image_')]

        if image_keys:
            for key in image_keys:
                img_name = context[key]

                if img_name in images:
                    img_bytes = images[img_name]
                else:
                    img_bytes = generate_placeholder_png()
                    exceptions.append(GeneratorError(
                        message=f"Image '{img_name}' not found, using placeholder",
                        code=ErrorCode.IMAGE_NOT_FOUND,
                        grpc_code=grpc.StatusCode.OK
                        )
                    )
                    print(f"Image '{img_name}' not found, using placeholder")

                tmp_path = tmp_dir / f"{key}_{img_name}.png"
                tmp_path.write_bytes(img_bytes)

                render_context[key] = InlineImage(doc, str(tmp_path), width=Mm(image_width_mm))

        try:
            doc.render(render_context)
        except Exception as e:
            exceptions.append(GeneratorError(
                message="can't render document",
                code=ErrorCode.RENDER_FAILED,
                grpc_code=grpc.StatusCode.INTERNAL,
                )
            )
            print("can't render document")

        output_stream = BytesIO()
        doc.save(output_stream)
        return output_stream.getvalue(), exceptions


def render_documents(
        context: dict,
        template_files: list[tuple[str, bytes]],
        images: dict[str, bytes] = None,
        image_width_mm: int = 180,
        output_filename_template: str = "{contractor}_{template}.docx",
) -> tuple[dict[str, bytes], dict[str, list[Exception]]]:
    if images is None:
        images = {}

    results = {}
    exceptions = {}
    contractor_name = context.get("file_name") or context.get("name_short") or datetime.now()

    for template_filename, template_bytes in template_files:
        rendered, doc_exceptions = render_template(
            template_bytes,
            context,
            images,
            image_width_mm,
        )
        out_name = output_filename_template.format(
            contractor=contractor_name,
            template=Path(template_filename).stem
        )
        results[out_name] = rendered
        if doc_exceptions:
            exceptions[out_name] = doc_exceptions

    return results, exceptions