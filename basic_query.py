from claude_agent_sdk import query

async def basic_query():
  async for message in query(prompt="how are you doing?"):
    print(message)