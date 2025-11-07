"""
Claude Agent SDK 基本練習

提供基本的 Claude API 對話功能。
"""

from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, TextBlock, query

async def basic_query(prompt: str):
  """
  執行 Claude 查詢並輸出回應
  
  此函式會建立一個單次查詢請求給 Claude API，並以串流方式處理回應。
  每次呼叫都是獨立的，不會保留對話歷史記錄。

  參數:
    prompt (str): 要發送給 Claude 的提示詞/問題

  回傳:
    None - 直接將回應內容印出到標準輸出

  使用範例:
    await basic_query("請說明 Python 的裝飾器")

  注意事項:
    - 此函式為異步函式，需要透過異步執行環境（如 anyio.run）來啟動
    - 每次查詢都是獨立的，不會記住之前的對話內容
  """
  # 配置 Claude Agent 選項
  # ClaudeAgentOptions 用於設定 AI 模型的行為參數
  options = ClaudeAgentOptions(
    system_prompt="你是一個樂於助人的助手。你會說中文並展示你的工作步驟。",  # 定義 AI 的角色與行為準則
    max_turns=None,  # 不限制對話輪次（適用於 agent 模式，單次查詢時無影響）
    model="claude-sonnet-4-5-20250929"  # 指定使用的 Claude 模型版本
  )

  # 執行查詢並處理回應
  # query() 函式會返回一個異步迭代器，以串流方式逐步接收回應
  async for message in query(prompt=prompt, options=options):
    # 檢查訊息類型是否為助手回應（AssistantMessage）
    if isinstance(message, AssistantMessage):
      # 訊息內容（content）是由多個區塊（block）組成的陣列
      for block in message.content:
        # 只處理文字區塊（TextBlock），忽略其他類型的區塊（如工具使用等）
        if isinstance(block, TextBlock):
          print(block.text)  # 將文字內容輸出到標準輸出


async def start_chat_loop():
  """
  啟動簡易互動對話迴圈

  此函式提供一個命令列介面的互動式對話環境，讓使用者可以持續與 Claude 進行對話。
  每次對話都是獨立的查詢，不會保留對話歷史（無記憶功能）。

  使用方式:
    - 在提示符號 (>>>) 後輸入問題或指令
    - 輸入 'exit' 或 'quit' 來結束對話
    - 按下 Ctrl+C 或 Ctrl+D 也可以結束對話

  回傳:
    None

  使用範例:
    anyio.run(start_chat_loop)

  注意事項:
    - 此函式為異步函式，需要透過異步執行環境（如 anyio.run）來啟動
    - 空白輸入會被忽略，不會送出查詢
  """
  print("Welcome to 簡易互動對話")
  print("type 'exit' to quit.")

  # 主要對話迴圈，持續接收使用者輸入直到收到結束指令
  while True:
    try:
      # 從標準輸入讀取使用者輸入，並移除前後空白
      user_input = input(">>>").strip()

      # 檢查是否為結束指令（不區分大小寫）
      if user_input.lower() in ['exit', 'quit']:
        print("Bye!")
        break
      elif user_input:
        # 如果輸入不為空，將對話送至 AI 模型進行處理
        # 注意：每次呼叫 basic_query 都是獨立的查詢，不保留對話歷史
        await basic_query(user_input)

    except KeyboardInterrupt:
      # 捕捉 Ctrl+C 中斷信號
      print("Bye!")
      break
    except EOFError:
      # 捕捉 Ctrl+D (Unix/Mac) 或 Ctrl+Z (Windows) 輸入結束信號
      print("Bye!")
      break
    except Exception as e:
      # 捕捉其他未預期的例外狀況
      print(f"出現例外！ {e}")
      break
