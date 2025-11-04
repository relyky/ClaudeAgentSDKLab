from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, TextBlock, query

async def basic_query():
  # 你是一個樂於助人的助手。你會說中文並展示你的工作步驟。
  # You are a helpful assistant. You speak latin and show your working.
  options = ClaudeAgentOptions(system_prompt="你是一個樂於助人的助手。你會說中文並展示你的工作步驟。", 
                               max_turns=None, 
                               model="claude-sonnet-4-5-20250929")

  # calculate 2+2
  async for message in query(prompt="計算 9 * 7", options=options):
    if isinstance(message, AssistantMessage):
       for block in message.content:
        if isinstance(block, TextBlock):
          print(block.text)
