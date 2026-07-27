from pathlib import Path

def load_config():
    try:
        from config import TEMPLATES
        return TEMPLATES
    except ImportError:
        try:
            from config_example import TEMPLATES
            return TEMPLATES
        except ImportError:
            print("Ошибка: файл конфигурации не найден")
            exit(1)

