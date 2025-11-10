from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient, TextBlock, ToolResultBlock, ToolUseBlock, UserMessage, tool, create_sdk_mcp_server
from typing import Any
import numexpr as ne

async def start_chat_tools():
  print("Welcome to AI mode 取用工具")
  print("type 'exit' to quit.")

  @tool(name="calculator",
        description="Evaluate an expression using our calculator. The calculator evaluates numexpr expressions eg. 0.5 * 70 * 25**2 ",
        input_schema={"expression": str})
  async def calculator(args: dict[str,Any]) -> dict[str,Any]:
    try:
      # read data
      expression = args.get('expression')

      # process (service) --- 通常這裡叫用服務
      result = ne.evaluate(expression)

      # return 
      return {
        "content": [{"type":"text", "text":f"{result}"}]
      }
    except Exception as e:
      return {
        "content": [{"type":"text", "text":f" Error: {e}"}]
      }
    

  tools_mcp = create_sdk_mcp_server(name="General tools", version="2.0.0", tools=[calculator])

  system_prompt = "你是一個樂於助人的助手。" # "you are a helpful assistant"
  allowed_tools = ["Reac", "Write", "Bash", "mcp__extra_tools__calculator"]

  options = ClaudeAgentOptions(system_prompt=system_prompt, 
                               mcp_servers={"extra_tools": tools_mcp}, 
                               allowed_tools=allowed_tools, 
                               permission_mode="acceptEdits")
  
  async with ClaudeSDKClient(options=options) as client:
    while True:
      try:
        user_input = input(">>>").strip()

        if user_input.lower() in ['exit', 'quit']:
          print("Bye!")
          break
        elif user_input:
          # send message to the AI model
          await client.query(prompt=user_input)          
          async for message in client.receive_response():
            
            if isinstance(message, UserMessage):
              for block in message.content:
                if isinstance(block, TextBlock): # show user message
                  print(f"User: {block.text}")
                elif isinstance(block, ToolResultBlock): # show tool result
                  print(
                    f"Tool Result: {block.content[:100] if block.content else 'None'}..."
                  )
            elif isinstance(message, AssistantMessage):
              for block in message.content:

                if isinstance(block, ToolUseBlock):
                  print(f"Using tool: {block.name}")
                  if block.input:
                    print(f"  Input: {block.input}")
                elif isinstance(block, TextBlock): # if the model is responding in text
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
