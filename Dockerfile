# 使用官方 Python 運行時作為父鏡像
FROM python:3.10-slim

# 設置工作目錄
WORKDIR /app

# 將當前目錄內容複製到容器中的 /app
COPY ./app /app
COPY ./requirements.txt /app

# 安裝項目依賴
RUN pip install --no-cache-dir -r requirements.txt

# 設置環境變量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 暴露端口 8000 供外部訪問
EXPOSE 8000

# 運行 Django 開發服務器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
