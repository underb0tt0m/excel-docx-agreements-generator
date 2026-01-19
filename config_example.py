from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

TEMPLATES = {
    "EDO": PROJECT_ROOT / "templates" / "examples" / "EDO.docx",
    "BRD_service": PROJECT_ROOT / "templates" / "examples" / "BRD_service.docx",
    "BRD_usluga": PROJECT_ROOT / "templates" / "examples" / "BRD_usluga.docx",
}