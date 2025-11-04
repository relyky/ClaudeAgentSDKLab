"""
Claude Agent SDK Lab 主程式

此程式用於演示 Claude Agent SDK 的基本查詢功能。
程式會載入環境變數並執行異步查詢操作。
"""

import anyio
from os.path import join, dirname
from dotenv import load_dotenv
from basic_query import basic_query

# 顯示程式標題
print('§ Claude Agent SDK Lab 1')

# 建立 .env 檔案的完整路徑。API Key 會預取系統設定的值。
#dotenv_path = join(dirname(__file__), '.env.local')
dotenv_path = join(dirname(__file__), '.env')

# 載入環境變數（例如 API 金鑰等設定）
load_dotenv(dotenv_path)

# 執行基本查詢的異步函數
anyio.run(basic_query) 
