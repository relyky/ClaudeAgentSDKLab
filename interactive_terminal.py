
from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient, TextBlock
from aioconsole import ainput

async def start_chat_continuous():
  print("Welcome to 簡易互動對話")
  print("type 'exit' to quit.")

  # ClaudeAgentOptions 用於設定 AI 模型的行為參數
  options = ClaudeAgentOptions(
    system_prompt="你是一個樂於助人的助手。你會說中文並展示你的工作步驟。",  # 定義 AI 的角色與行為準則
    max_turns=None,  # 不限制對話輪次（適用於 agent 模式，單次查詢時無影響）
    model="claude-sonnet-4-5-20250929",  # 指定使用的 Claude 模型版本
    mcp_servers={
      "fetch":{
        "command":"uvx",
        "args":["mcp-server-fetch"]
      }
    },
    # 允許使用 fetch 工具
    allowed_tools=["mcp__fetch__fetch"]
  )

  async with ClaudeSDKClient(options=options) as client:
    while True:
      try:
        user_input = (await ainput(">>>")).strip()

        if user_input.lower() in ['exit', 'quit']:
          print("Bye!")
          break
        elif user_input:
          # send message to the AI model
          await client.query(prompt=user_input)
          async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
              for block in message.content:
                if isinstance(block, TextBlock):
                  print(f"Claude: {block.text}")

      except KeyboardInterrupt:
        print("\nBye!")
        break
      except EOFError:
        print("\nBye!")
        break
      except Exception as e:
        print(f"出現例外！ {e}")
        print("繼續對話...")
        continue
