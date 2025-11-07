"""
Claude Agent SDK 基本查詢模組

提供基本的 Claude API 查詢功能，支援自訂提示詞。
"""

from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, TextBlock, query


async def basic_query(prompt: str):
  """
  執行 Claude 查詢並輸出回應

  參數:
    prompt: 要發送給 Claude 的提示詞
  """
  # 配置 Claude Agent 選項
  options = ClaudeAgentOptions(
    system_prompt="你是一個樂於助人的助手。你會說中文並展示你的工作步驟。",
    max_turns=None,
    model="claude-sonnet-4-5-20250929"
  )

  # 執行查詢並處理回應
  async for message in query(prompt=prompt, options=options):
    if isinstance(message, AssistantMessage):
      for block in message.content:
        if isinstance(block, TextBlock):
          print(block.text)


async def start_chat_loop():
  print("Welcome to 簡易互動對話")
  print("type 'exit' to quit.")

  # system_prompt = "你是一個樂於助人的助手。"
  # system_prompt = "You are a helpful assistant."

  while True:
    try:
      user_input = input(">>>").strip()

      if user_input.lower() in ['exit', 'quit']:
        print("Bye!")
        break
      elif user_input:
        # 對話送至 AI 模型
        await basic_query(user_input)

    except KeyboardInterrupt:
      print("Bye!")
      break
    except EOFError:
      print("Bye!")
      break
    except Exception as e:
      print(f"出現例外！ {e}")
      break
