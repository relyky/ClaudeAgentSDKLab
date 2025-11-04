"""
Claude Agent SDK Lab 主程式

此程式用於演示 Claude Agent SDK 的基本查詢功能。
程式會載入環境變數並執行異步查詢操作。
"""

import anyio
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
from basic_query import basic_query

def now_str() -> str:
    """
    獲取當前的時間，並格式為 HH:mm:ss (24小時制)。
    """

    current_time = datetime.now()
    time_string = current_time.strftime('%H:%M:%S')    
    return time_string


# 顯示程式標題與開始時間
print(f'[{now_str()}] § Claude Agent SDK Lab 1 - BEGIN')

# 載入(.env )環境變數（例如 API 金鑰等設定）
# 註1：load_dotenv() 預設不會覆蓋已存在的系統環境變數
# 註2：API Key 會預取系統設定的值。
dotenv_path = join(dirname(__file__), '.env')

load_dotenv(dotenv_path)

# 例1：執行基本查詢的異步函數，傳入提示詞。
user_prompt = "計算 9 * 7"
print("user_prompt: " + user_prompt)
anyio.run(basic_query, user_prompt) 

# 例2：執行基本查詢的異步函數，傳入提示詞
user_prompt = "今天台北天氣如何?"
print("user_prompt: " + user_prompt)
anyio.run(basic_query, user_prompt) 

# 標記結束與結束時間
print(f'[{now_str()}] § Claude Agent SDK Lab 1 - END')
