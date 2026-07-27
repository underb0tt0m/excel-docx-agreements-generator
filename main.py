from app.utils.config_loader import load_config
from app.excel.reader import read_excel
from app.excel.parser import build_tasks_from_master
from app.validation.validator import validate_contractor_raw
from app.docx.renderer import render_documents


def main() -> None:
    TEMPLATES = load_config()
    excel_path = TEMPLATES["data"]

    df = read_excel(excel_path)

    tasks = build_tasks_from_master(df)
    print(f"[INFO] Найдено контрагентов к генерации: {len(tasks)}")

    success = 0
    skipped = 0

    for task in tasks:
        model = validate_contractor_raw(
            task.raw,
            source=f"{excel_path.name} | column={task.column}",
        )
        if model is None:
            skipped += 1
            continue

        try:
            render_documents(
                model,
                contractor_type=task.ka_type,
                needs_brd=task.needs_brd,
                needs_edo=task.needs_edo,
            )
            success += 1
        except Exception as e:
            print(f"[ERROR] Ошибка генерации (column={task.column}): {e}")
            skipped += 1

    print(f"[DONE] Успешно: {success}, пропущено: {skipped}")


if __name__ == "__main__":
    main()
