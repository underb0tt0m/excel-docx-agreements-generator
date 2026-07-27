from pathlib import Path
from typing import Optional
from app.utils.config_loader import load_config
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from app.utils.paths import get_project_root

from app.schemas.excel_form import AgreementExcelModel

PROJECT_ROOT = get_project_root()

class TemplatePaths:
    TEMPLATES = load_config()
    EDO = TEMPLATES["EDO"]
    BRD_SERVICE = TEMPLATES["BRD_service"]
    BRD_USLUGA = TEMPLATES["BRD_usluga"]


class OutputPaths:
    ROOT = PROJECT_ROOT / "results"
    SERVICES = ROOT / "services"
    USLUGI = ROOT / "uslugi"


def _safe_org_dir_name(name: str) -> str:
    return name.replace("«", "").replace("»", "").strip()


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _service_card_paths(org_name: str) -> list[Path]:
    base = PROJECT_ROOT / "cards" / "services" / org_name
    return [base / "1.png", base / "2.png", base / "3.png"]


def _usluga_card_path(org_name: str) -> Path:
    return PROJECT_ROOT / "cards" / "uslugi" / f"{org_name}.png"


def _build_context(model: AgreementExcelModel) -> dict:
    return model.model_dump(by_alias=True, exclude_none=True)


def render_edo(
    model: AgreementExcelModel,
    *,
    contractor_type: str,
    output_dir: Optional[Path] = None,
) -> Path:
    org_name = model.name_short
    org_dir = _safe_org_dir_name(org_name)

    if contractor_type == "Услуга":
        base_out = output_dir or (OutputPaths.USLUGI / org_name)
    else:
        base_out = output_dir or (OutputPaths.SERVICES / org_name)

    _ensure_dir(base_out)

    tpl_path = TemplatePaths.EDO
    if not tpl_path.exists():
        raise FileNotFoundError(f"EDO template not found: {tpl_path}")

    doc = DocxTemplate(str(tpl_path))
    context = _build_context(model)

    try:
        doc.render(context)
    except Exception as e:
        print(f"[ERROR] Ошибка рендера ЭДО для {org_name}: {e}")
        raise

    out_path = base_out / f"{org_dir} Соглашение об ЭДО.docx"
    doc.save(str(out_path))
    print(f"[OK] ЭДО: {Path(out_path).name}")
    return out_path


def render_brd(
    model: AgreementExcelModel,
    *,
    contractor_type: str,
    output_dir: Optional[Path] = None,
) -> Path:
    org_name = model.name_short
    org_dir = _safe_org_dir_name(org_name)

    if contractor_type == "Услуга":
        base_out = output_dir or (OutputPaths.USLUGI / org_name)
        tpl_path = TemplatePaths.BRD_USLUGA
    else:
        base_out = output_dir or (OutputPaths.SERVICES / org_name)
        tpl_path = TemplatePaths.BRD_SERVICE

    _ensure_dir(base_out)

    if not tpl_path.exists():
        raise FileNotFoundError(f"BRD template not found: {tpl_path}")

    doc = DocxTemplate(str(tpl_path))
    context = _build_context(model)


    if contractor_type == "Услуга":
        img_path = _usluga_card_path(org_name)
        if img_path.exists():
            context["Image1"] = InlineImage(doc, str(img_path), width=Mm(180))
        else:
            print(f"[WARN] Нет карточки(ек) услуги для {org_name}: {Path(img_path).name}")
    else:
        imgs = _service_card_paths(org_name)
        keys = ["Image1", "Image2", "Image3"]
        for k, p in zip(keys, imgs):
            if p.exists():
                if k == "Image1":
                    width = Mm(60)
                else:
                    width = Mm(180)
                context[k] = InlineImage(doc, str(p), width=width)
            else:
                print(f"[WARN] Нет карточки(ек) сервиса для {org_name}: {Path(p).name}")

    try:
        doc.render(context)
    except Exception as e:
        print(f"[ERROR] Ошибка рендера БРД для {org_name}: {e}")
        raise

    out_path = base_out / f"{org_dir} Соглашение о публикации в Экосистеме БРД.docx"
    doc.save(str(out_path))
    print(f"[OK] БРД: {Path(out_path).name}")
    return out_path


def render_documents(
    model: AgreementExcelModel,
    *,
    contractor_type: str,
    needs_brd: bool,
    needs_edo: bool,
) -> list[Path]:
    """
    Генерирует нужные документы по флагам.
    Возвращает список сохраненных файлов.
    """
    results: list[Path] = []

    if needs_brd:
        results.append(render_brd(model, contractor_type=contractor_type))
    if needs_edo:
        results.append(render_edo(model, contractor_type=contractor_type))

    return results

if __name__ == "__main__":
    from app.excel.parser import build_tasks_from_master
    from app.excel.reader import read_excel
    from app.validation.validator import validate_contractor_raw

    df = read_excel(PROJECT_ROOT / 'data.xlsx')
    data = build_tasks_from_master(df)
    if data:
        checked_data = validate_contractor_raw(data[0].raw)
        print(render_documents(
            checked_data,
            contractor_type=checked_data.ka_type,
            needs_brd=True,
            needs_edo=True
        ))
