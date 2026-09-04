import grpc
import pandas as pd
from pathlib import Path

from internal.app.exceptions import GeneratorError, ErrorCode


def read_excel(path: str | Path) -> pd.DataFrame:
    try:
        df = pd.read_excel(path, header=None, dtype=str)
        return df
    except Exception as e:
        raise GeneratorError(
            message=f"Failed to read Excel file {path}: {e}",
            code=ErrorCode.INTERNAL,
            grpc_code=grpc.StatusCode.INTERNAL
        )