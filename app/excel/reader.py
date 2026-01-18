from pathlib import Path
import pandas as pd


def read_excel(path: str | Path) -> pd.DataFrame:
    """
    Читает Excel, где:
      - строки = поля
      - 1-й столбец = технический ключ поля
      - остальные столбцы = контрагенты

    Возвращает DataFrame (NaN -> None), без изменения ориентации
    """
    path = Path(path)
    if not path.exists():
        print(f"[ERROR] Excel файл не найден: {path}")
        raise FileNotFoundError(path)

    try:
        df = pd.read_excel(path)
        df = df.where(pd.notna(df), None)
    except Exception as e:
        print(f"[ERROR] Не удалось прочитать Excel: {e}")
        raise

    if df.shape[1] < 2:
        print("[ERROR] Excel должен содержать минимум 2 колонки (key + хотя бы 1 контрагент).")
        raise ValueError("Excel must contain at least 2 columns")

    return df

if __name__ == "__main__":
    data = read_excel('/Users/timur/Desktop/ГПН/Автоматизация заполнения документов/Жизнь тлен/Данные.xlsx')
    print(data.iloc[:, [0]])