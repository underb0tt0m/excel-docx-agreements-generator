from dataclasses import dataclass
import pandas as pd

@dataclass(frozen=True)
class ContractorData:
    name: str
    fields: dict[str, str]

def parse_contractors(
    df: pd.DataFrame,
    key_col: int = 0,
    start_col: int = 1,
) -> list[ContractorData]:
    contractors = []
    keys = df.iloc[:, key_col].dropna().astype(str).str.strip().tolist()
    key_rows = df.iloc[:, key_col].dropna().index

    for col_idx in range(start_col, len(df.columns)):
        col_name = str(df.columns[col_idx]).strip()
        if df.iloc[:, col_idx].isnull().all():
            continue
        fields = {}
        for row_idx, key in zip(key_rows, keys):
            val = df.iloc[row_idx, col_idx]
            if pd.isna(val):
                fields[key] = ""
            else:
                fields[key] = str(val).strip()
        contractors.append(ContractorData(name=col_name, fields=fields))
    return contractors