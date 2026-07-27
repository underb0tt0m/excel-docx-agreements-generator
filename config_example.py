from pathlib import Path

from app.utils.paths import get_project_root
import os

# Проверяем, работаем ли мы в Docker-контейнере
def is_docker():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        (os.path.isfile(path) and any('docker' in line for line in open(path)))
    )

# Определяем корневую директорию
if is_docker():
    # В Docker монтируем данные в /data
    PROJECT_ROOT = Path('/data')
else:
    # Обычный режим работы
    PROJECT_ROOT = get_project_root()

TEMPLATES = {
    "EDO": PROJECT_ROOT / "templates" / "examples" / "EDO.docx",
    "BRD_service": PROJECT_ROOT / "templates" / "examples" / "BRD_service.docx",
    "BRD_usluga": PROJECT_ROOT / "templates" / "examples" / "BRD_usluga.docx",
    "data": PROJECT_ROOT / "example_data.xlsx"
}