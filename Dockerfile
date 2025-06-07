# 使用官方 Python 映像檔作為基底
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製必要檔案
COPY requirements.txt .
COPY manage.py .
COPY Helpee_API/ ./Helpee_API/
COPY core/ ./core/
COPY staticfiles/ ./staticfiles/

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libmariadb-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安裝依賴
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 收集靜態檔案（避免部署時錯誤）
RUN python manage.py collectstatic --noinput

ENV PORT 8080
EXPOSE 8080

# 執行指令
CMD ["gunicorn", "Helpee_API.wsgi:application", "--bind", "0.0.0.0:8080"]
