import pandas as pd
from pathlib import Path

def read_excel(path: str | Path) -> pd.DataFrame:
    df = pd.read_excel(path, header=None, dtype=str)
    return df