# 使用官方 Python 運行時作為父鏡像
FROM python:3.10-slim

# 設置工作目錄
WORKDIR /app

# 更新包列表並安裝所需的包
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 安裝 datrie
RUN pip install datrie

# 複製並安裝項目依賴
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 設置環境變量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 創建 faiss_index 目錄並設置權限
RUN mkdir -p /app/faiss_index && chmod 777 /app/faiss_index

# 暴露端口 8000 供外部訪問
EXPOSE 8000

# 將當前目錄內容複製到容器中的 /app
COPY ./app /app

# 運行 Django 開發服務器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
