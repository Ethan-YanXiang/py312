# 從 包 調用 模組
from flask import Flask

app = Flask(__name__)  # 呼叫 Flask() 模組，初始化一個 app object，定義能找到靜態檔案與範本檔案的目錄（__name__ == myapp/app/）

from app import routes  # 定義路由
# 導至 myapp/app/routes3.py
