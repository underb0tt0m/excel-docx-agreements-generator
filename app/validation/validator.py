from pathlib import Path
from pydantic import ValidationError
from app.schemas.excel_form import AgreementExcelModel

def validate_contractor_raw(raw: dict[str, any], *, source: str | Path = "<master>") -> AgreementExcelModel | None:
    """
    Валидирует raw-данные контрагента (key->value) через Pydantic.

    - Если валидация успешна: возвращает AgreementExcelModel
    - Если нет: печатает ошибки в консоль и возвращает None
    """
    try:
        return AgreementExcelModel.model_validate(raw)
    except ValidationError as e:
        print(f"[ERROR] Ошибка валидации данных: {source}")
        _print_validation_error(e)
        return None


def _print_validation_error(e: ValidationError) -> None:
    errors = e.errors()
    for idx, err in enumerate(errors, start=1):
        loc = ".".join(str(x) for x in err.get("loc", [])) or "<root>"
        msg = err.get("msg", "Validation error")
        typ = err.get("type", "")
        print(f"  {idx}) {loc}: {msg} ({typ})")


if __name__ == "__main__":
    from app.excel.parser import build_tasks_from_master
    from app.excel.reader import read_excel
    df = read_excel('/Users/timur/Desktop/ГПН/Автоматизация заполнения документов/Жизнь тлен/data.xlsx')
    data = build_tasks_from_master(df)
    checked_data = validate_contractor_raw(data[0].raw)
    print(checked_data)
