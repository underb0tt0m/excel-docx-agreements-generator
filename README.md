# Генератор договоров из Excel

Универсальный инструмент для массовой генерации DOCX-документов из Excel-данных.

---

## Запуск

### Через Docker (gRPC-сервер)

```bash
docker build -t worker .
docker run -p 50051:50051 worker
```

### Локально

```bash
pip install -r requirements.txt
python grpc_server.py
```

---

## Входной архив

```
archive.zip
├── data.xlsx          # первая колонка — ключи, остальные — контрагенты
├── template.docx      # шаблон с плейсхолдерами
└── images/            # опционально
    └── img.png
```

---

## Выходной архив

```
output.zip
├── контрагент1_template.docx
├── контрагент1_template2.docx
└── контрагент2_template.docx
```

---

## Как это работает

1. Читает Excel, парсит всех контрагентов
2. Берёт все DOCX-шаблоны из архива
3. Для каждого контрагента подставляет данные во все шаблоны
4. Возвращает ZIP с готовыми документами

---

## Картинки

В шаблоне используй плейсхолдер `{{ image_имя }}`.

В Excel в колонке `image_имя` укажи имя файла (без расширения).

Картинки клади в папку `images/` в архиве.

Если картинка не найдена — вставляется красный квадрат.

---

## Структура проекта

```
.
├── app/
│   ├── handler.py       # основная логика
│   ├── docx/
│   │   └── renderer.py  # рендеринг DOCX + картинки
│   └── excel/
│       ├── reader.py    # чтение Excel
│       └── parser.py    # парсинг контрагентов
├── proto/
│   └── generator/       # сгенерированные gRPC-файлы
├── grpc_server.py       # gRPC-сервер
├── requirements.txt
└── Dockerfile
```

---

## API (gRPC)

- **Метод**: `Generate`
- **Запрос**: `GenerateRequest { bytes archive }`
- **Ответ**: `GenerateResponse { bytes zip_archive, repeated string errors, int32 generated_count }`