from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient, TextBlock, ToolResultBlock, ToolUseBlock, UserMessage, tool, create_sdk_mcp_server
from typing import Any
import numexpr as ne
import json

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
    
  @tool(name="leave_query",
        description="請假申請單維護作業。請假單查詢。",
        input_schema={"applicant": str})
  async def leave_query(args: dict[str,Any]) -> dict[str,Any]:
    try:
      # read data
      applicant = args.get('applicant')

      # process (service) --- 通常這裡叫用服務
      # 查詢資料庫...未實作。或向後呼叫 Web API。
      data = [{
        "application_id": "LV-2025-1113-001",
        "applicant_name": applicant,
        "department": "行銷部",
        "position": "市場專員",
        "application_date": "2025-11-11",
        "leave_type": "年假",
        "start_date": "2025-11-13",
        "end_date": "2025-11-13",
        "number_of_days": 1,
        "reason": "個人事務",
        "emergency_contact": "李美麗",
        "contact_phone": "0912-345-678",
        "supervisor": "陳經理",
        "status": "待審批",
        "remarks": "無"
      }] if applicant != "John" else []

      # process (service) --- 通常這裡叫用服務
      result = json.dumps(data)

      # return 
      return {
        "content": [{"type":"text", "text":f"{result}"}]
      }
    except Exception as e:
      return {
        "content": [{"type":"text", "text":f" Error: {e}"}]
      }  

  tools_mcp = create_sdk_mcp_server(name="General tools", version="2.0.0", tools=[calculator])

  # 假單管理 MCP Server
  leave_application_form_mcp = create_sdk_mcp_server(
    name="Leave Application Form Management", 
    version="1.0.0", 
    tools=[leave_query])

  system_prompt = "你是一個樂於助人的助手。" # "you are a helpful assistant"

  options = ClaudeAgentOptions(
    system_prompt=system_prompt, 
    mcp_servers={
      "leave_application_form": leave_application_form_mcp,
      "extra_tools": tools_mcp
    }, 
    allowed_tools=[
      "Read", "Write", "Bash", 
      "mcp__leave_application_form__leave_query",
      "mcp__extra_tools__calculator"
    ], 
    permission_mode="acceptEdits"
  )
  
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
