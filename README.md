# 佈署流程

1. 參考 <a href="https://docs.docker.com/engine/install/ubuntu/">docker 安裝步驟</a>安裝 docker 及 docker compose。
2. 下載本專案
   ```bash for Linux
   git clone https://github.com/hsiehpinghan/django_demo.git
   ```
3. 佈署系統

   ```bash for Linux
   cd django_demo
   sudo docker compose up -d
   ```

4. 測試網址: `http://localhost`
