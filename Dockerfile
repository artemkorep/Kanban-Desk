FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей + сетевых утилит
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates

# Проверка подключения к PyPI (опционально)
RUN curl -s https://pypi.org >/dev/null && echo "PyPI доступен" || echo "Внимание: Нет подключения к PyPI"

# Копируем requirements отдельно для кэширования
COPY requirements.txt .

# Установка зависимостей с несколькими зеркалами
RUN pip install \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    --trusted-host pypi.tuna.tsinghua.edu.cn \
    --no-cache-dir \
    --default-timeout=300 \
    -r requirements.txt || \
    pip install \
    --index-url https://mirrors.aliyun.com/pypi/simple/ \
    --trusted-host mirrors.aliyun.com \
    --no-cache-dir \
    --default-timeout=300 \
    -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]