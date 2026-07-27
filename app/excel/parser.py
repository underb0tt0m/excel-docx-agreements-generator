from dataclasses import dataclass
import pandas as pd

@dataclass(frozen=True)
class ContractorTask:
    """
    Что нужно сгенерировать для одного контрагента (одного столбца).
    """
    column: any
    ka_type: str
    needs_brd: bool
    needs_edo: bool
    raw: dict[str, any]

def _to_bool_flag(value: any) -> bool:
    """
    Приводит значения из Excel к bool.
    Поддержка MVP: "Да"/"да"/"YES"/"1"/True.
    """
    if value is True:
        return True
    if value is False:
        return False
    s = str(value).strip().lower()
    return s in {"да", "yes", "true", "1", "y", "ok"}


def _find_row_index_by_key(df: pd.DataFrame, key_col: any, key_value: str) -> int:
    """
    Находит индекс строки, где df[key_col] == key_value (после strip).
    """
    series = df[key_col].astype(str).str.strip()
    matches = series[series == key_value]
    if matches.empty:
        raise KeyError(f"Key '{key_value}' not found in Excel (key column '{key_col}')")
    return int(matches.index[0])

def build_tasks_from_master(
    df: pd.DataFrame,
    *,
    key_col: any = 0,
    needs_brd_key: str = "Needs_brd",
    needs_edo_key: str = "Needs_EDO",
    ka_type_key: str = "KA_type",
    start_from_col_index: int = 2,
) -> list[ContractorTask]:
    """
    Парсит мастер-таблицу и возвращает список задач на генерацию.
    Берём только тех, у кого needs_brd или needs_edo = True.
    """

    # Индексы строк с управляющими полями
    needs_brd_row = _find_row_index_by_key(df, key_col, needs_brd_key)
    needs_edo_row = _find_row_index_by_key(df, key_col, needs_edo_key)
    ka_type_row = _find_row_index_by_key(df, key_col, ka_type_key)

    tasks: list[ContractorTask] = []

    contractor_cols = list(df.columns)[start_from_col_index:]
    for col in contractor_cols:
        needs_brd = _to_bool_flag(df.at[needs_brd_row, col])
        needs_edo = _to_bool_flag(df.at[needs_edo_row, col])

        # пропускаем, если ничего генерировать не нужно
        if not (needs_brd or needs_edo):
            continue

        ka_type = str(df.at[ka_type_row, col]).strip()

        # raw dict: key -> value для данного контрагента
        raw: dict[str, any] = {}
        for idx, key in enumerate(df.iloc[:, key_col].tolist()):
            k = str(key).strip()
            if not k:
                continue
            raw[k] = df.at[df.index[idx], col]

        tasks.append(
            ContractorTask(
                column=col,
                ka_type=ka_type,
                needs_brd=needs_brd,
                needs_edo=needs_edo,
                raw=raw,
            )
        )

    return tasks

if __name__ == "__main__":
    from app.excel.reader import read_excel

    df = read_excel('/Users/timur/Desktop/ГПН/Автоматизация заполнения документов/Жизнь тлен/data.xlsx')
    data = build_tasks_from_master(df)
    print(data)