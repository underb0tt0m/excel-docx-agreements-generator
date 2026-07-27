from io import BytesIO
from pathlib import Path
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import tempfile
from PIL import Image, ImageDraw


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
) -> bytes:
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
                img_name = key.replace('image_', '').strip()

                if img_name in images:
                    img_bytes = images[img_name]
                else:
                    img_bytes = generate_placeholder_png()
                    print(f"Image '{img_name}' not found, using placeholder")

                tmp_path = tmp_dir / f"{key}_{img_name}.png"
                tmp_path.write_bytes(img_bytes)

                print(f"Inserting image: {key} -> {img_name}")

                render_context[key] = InlineImage(doc, str(tmp_path), width=Mm(image_width_mm))

        doc.render(render_context)

        output_stream = BytesIO()
        doc.save(output_stream)
        return output_stream.getvalue()


def render_documents(
        context: dict,
        template_files: list[tuple[str, bytes]],
        images: dict[str, bytes] = None,
        image_width_mm: int = 180,
        output_filename_template: str = "{contractor}_{template}.docx",
) -> dict[str, bytes]:
    if images is None:
        images = {}

    results = {}
    contractor_name = context.get("name_short") or context.get("Название_краткое") or "unknown"

    for template_filename, template_bytes in template_files:
        rendered = render_template(
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

    return results