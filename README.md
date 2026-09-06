# Генератор договоров из Excel (Python-воркер)

Инструмент для массовой генерации DOCX-документов из Excel-данных.

Работает как **gRPC-сервер** (синхронный вызов) или как **consumer очереди RabbitMQ** (асинхронная обработка).

---

## 🚀 Запуск

### Через Docker

```bash
make docker-build

make docker-run
```

### Локально

```bash
pip install -r requirements.txt
python -m cmd.main
```

---

## 📁 Входной архив (ZIP)

```
archive.zip
├── data.xlsx          # первая колонка — ключи, остальные — контрагенты
├── template.docx      # шаблон с плейсхолдерами
└── images/            # опционально
    └── img.png
```

---

## 📦 Выходной архив (ZIP)

```
output.zip
├── контрагент1_template.docx
├── контрагент1_template2.docx
└── контрагент2_template.docx
```

---

## 🧠 Как это работает

1. Читает Excel, парсит всех контрагентов.
2. Берёт все DOCX-шаблоны из архива.
3. Для каждого контрагента подставляет данные во все шаблоны.
4. Возвращает ZIP с готовыми документами.

---

## 🖼 Картинки

В шаблоне используй плейсхолдер `{{ image_имя }}`.

В Excel в колонке `image_имя` указывается имя файла (без расширения).

Картинки кладутся в папку `images/` в архиве.

Если картинка не найдена — вставляется красный квадрат.

---

## ⚙️ Конфигурация

Файл `config/local.yaml`:

```yaml
execution_mode: "grpc" #grpc | queue

grpc_server:
  port: 50051

db:
  host: "host.docker.internal"
  port: 5432
  db_name: "generator"
  user: "postgres"

redis:
  host: "host.docker.internal"
  port: 6379
  job_status_ttl: 600

rabbit_mq:
  host: "host.docker.internal"
  port: 5672
  user: "guest"
  v_host: "/"
  queue: "jobs"
```

Пароли и чувствительные данные загружаются из `.env`:

```env
DB_PASSWORD=password
REDIS_PASSWORD=password
RABBITMQ_PASSWORD=password
```

---

## 📦 Структура проекта

```
.
├── cmd/
    ├── main.py                # главная точка входа
│   ├── grpc_server/           # gRPC-сервер
│   │   └── main.py
│   └── consumer/              # консьюмер RabbitMQ
│       └── main.py
├── internal/
│   ├── app/                   # бизнес-логика
│   │   ├── generator/         # генерация документов
│   │   ├── docx/              # рендеринг DOCX
│   │   ├── excel/             # парсинг Excel
│   │   └── exceptions.py
│   ├── config/                # загрузка конфигурации
│   ├── infrastructure/        # работа с БД, Redis, RabbitMQ
│   ├── processor/             # обработка задач (JobProcessor, MessageHandler)
│   └── logger/                # настройка логирования
├── proto/                     # сгенерированные protobuf
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🔌 API (gRPC)

- **Метод**: `Generate`
- **Запрос**: `GenerateRequest { bytes archive }`
- **Ответ**: `GenerateResponse { bytes zip_archive, repeated string errors, int32 generated_count }`