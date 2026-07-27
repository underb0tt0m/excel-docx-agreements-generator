# app/utils/paths.py (обновлённый)
from __future__ import annotations

from pathlib import Path
import sys
import os


def is_docker() -> bool:
    """Проверяем, запущены ли мы в Docker-контейнере."""
    path = '/proc/self/cgroup'
    return (
            os.path.exists('/.dockerenv') or
            (os.path.isfile(path) and any('docker' in line for line in open(path)))
    )


def get_project_root() -> Path:
    """
    Корень данных (Данные.xlsx, Шаблоны/, Карточки/) должен быть рядом с бинарником.
    В Docker используем /data как корень.
    """
    if is_docker():
        return Path("/data")

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent  # рядом с agreements-tool
    return Path(__file__).resolve().parents[2]