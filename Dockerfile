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
COPY .env .

# 安裝依賴
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 收集靜態檔案（避免部署時錯誤）
RUN python manage.py collectstatic --noinput

# 設定埠口（Cloud Run 預設 8080）
ENV PORT 6007
EXPOSE 6007

# 執行指令
CMD ["gunicorn", "Helpee_API.wsgi:application", "--bind", "0.0.0.0:6007"]
