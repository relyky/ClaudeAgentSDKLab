"""
Claude Agent SDK Lab 主程式

此程式用於演示 Claude Agent SDK 的基本查詢功能。
程式試執行簡易的互動對話。(有記憶能力)
"""

import anyio
from os.path import join, dirname
from dotenv import load_dotenv
from interactive_terminal import start_chat_continuous 

# 載入(.env )環境變數（例如 API 金鑰等設定）
# 註1：load_dotenv() 預設不會覆蓋已存在的系統環境變數
# 註2：API Key 會預取系統設定的值。
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# 例：簡易的互動對話。
anyio.run(start_chat_continuous)
