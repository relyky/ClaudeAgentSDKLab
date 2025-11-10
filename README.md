# Claude Agent SDK Lab

Claude Agent SDK 的實驗專案，用於學習和測試 Claude Agent SDK 的各種功能和使用模式。

## 專案簡介

本專案展示如何使用 Claude Agent SDK 建立各種 AI 應用，從簡單的單次查詢到複雜的多輪對話和工具整合。專案包含多個範例程式，逐步展示 SDK 的不同功能特性。

## 功能特性

- ✅ **基本查詢**：單次問答，展示最基本的 SDK 使用方式
- ✅ **互動對話（無記憶）**：持續對話但不保留歷史，每次查詢獨立
- ✅ **互動對話（有記憶）**：多輪對話with上下文記憶，可進行複雜的對話流程
- ✅ **工具整合**：自訂工具（計算器範例），展示如何擴展 AI 能力
- ✅ **非同步處理**：完整的異步 I/O 支援，使用 `aioconsole` 處理輸入
- ✅ **權限管理**：支援 WebSearch、WebFetch 等工具的權限設定
- ✅ **錯誤處理**：健壯的例外處理機制，對話不會因錯誤而中斷

## 快速開始

### 環境需求

- Python 3.10+
- Claude API Key（從 [Anthropic Console](https://console.anthropic.com/) 取得）

### 安裝步驟

1. **Clone 專案**
```bash
git clone https://github.com/your-username/ClaudeAgentSDKLab.git
cd ClaudeAgentSDKLab
```

2. **建立虛擬環境（使用 uv）**
```bash
uv venv
```

3. **啟動虛擬環境**
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

4. **安裝依賴**
```bash
pip install -r requirements.txt
```

5. **設定環境變數**

建立 `.env.local` 檔案並加入你的 API Key：
```
ANTHROPIC_API_KEY=your_api_key_here
```

### 執行範例

#### 1. 基本查詢
```bash
python main_basic_query.py
```
執行兩個預設查詢範例：
- 數學計算問題
- 天氣詢問

適合用來測試 API 連線和基本功能。

#### 2. 互動對話（無記憶）
```bash
python main_basic_interactive.py
```
啟動互動式命令列介面，特點：
- 每次查詢獨立，不記憶對話歷史
- 適合不需要上下文的連續查詢
- 輸入 `exit` 或 `quit` 離開

#### 3. 互動對話（有記憶）⭐ 推薦
```bash
python main_client_interactive.py
```
啟動具有記憶功能的對話，特點：
- 自動記憶對話歷史
- 可進行多輪上下文對話
- 支援 WebSearch、WebFetch 等工具
- 輸入 `exit` 或 `quit` 離開

#### 4. 工具整合範例
```bash
python main_client_use_tools.py
```
展示如何整合自訂工具，特點：
- 內建計算器工具（使用 `numexpr`）
- 展示 MCP 伺服器整合
- 可處理複雜的數學表達式

## 專案結構

```
ClaudeAgentSDKLab/
├── basic_query.py              # 基礎查詢模組（無記憶）
├── interactive_terminal.py     # 有記憶互動對話模組
├── agent_with_tools.py         # 工具整合模組（計算器）
├── main_basic_query.py         # 基本查詢入口
├── main_basic_interactive.py   # 無記憶對話入口
├── main_client_interactive.py  # 有記憶對話入口
├── main_client_use_tools.py    # 工具整合入口
├── test_interactive.py         # 測試腳本
├── requirements.txt            # Python 依賴
├── .env                        # 環境變數範本
├── .env.local                  # 實際環境變數（需自行建立）
├── CLAUDE.md                   # Claude Code 專案指引
└── README.md                   # 本檔案
```

### 核心模組說明

#### basic_query.py
提供基礎查詢功能：
- `basic_query(prompt: str)` - 執行單次查詢
- `start_chat_loop()` - 無記憶互動對話迴圈
- 使用 `query()` 函數（無狀態）

#### interactive_terminal.py
提供有記憶的互動對話：
- `start_chat_continuous()` - 有記憶互動對話
- 使用 `ClaudeSDKClient` 保持對話狀態
- 使用 `aioconsole.ainput` 處理非同步輸入
- 支援 WebSearch、WebFetch、Read、Write、Bash 等工具

#### agent_with_tools.py
展示工具整合：
- `start_chat_tools()` - 整合自訂工具的對話
- 定義計算器工具（使用 `@tool` 裝飾器）
- 使用 MCP 伺服器整合工具
- 處理 `ToolUseBlock` 和 `ToolResultBlock`

## 開發指南

### 使用模式對比

| 模式 | 檔案 | 記憶 | 工具 | 適用場景 |
|------|------|------|------|---------|
| 基本查詢 | `basic_query.py` | ❌ | ❌ | 單次問答 |
| 無記憶對話 | `basic_query.py` | ❌ | ❌ | 不需上下文的連續查詢 |
| 有記憶對話 | `interactive_terminal.py` | ✅ | ✅ | 多輪對話、網路搜尋 |
| 工具整合 | `agent_with_tools.py` | ✅ | ✅ | 需要特殊能力的 Agent |

### API 使用模式

#### 模式 1：無狀態查詢（適合單次查詢）
```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    system_prompt="你是一個樂於助人的助手。",
    model="claude-sonnet-4-5-20250929"
)

async for message in query(prompt=prompt, options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
```

#### 模式 2：有狀態對話（適合多輪對話）
```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from aioconsole import ainput

options = ClaudeAgentOptions(
    system_prompt="你是一個樂於助人的助手。",
    model="claude-sonnet-4-5-20250929",
    permission_mode="default",
    allowed_tools=["WebSearch", "WebFetch", "Read", "Write", "Bash"]
)

async with ClaudeSDKClient(options=options) as client:
    while True:
        user_input = await ainput(">>>")
        await client.query(prompt=user_input)
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")
```

#### 模式 3：工具整合（適合擴展 AI 能力）
```python
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeAgentOptions
import numexpr as ne

@tool(
    name="calculator",
    description="Evaluate mathematical expressions",
    input_schema={"expression": str}
)
async def calculator(args: dict[str, Any]) -> dict[str, Any]:
    try:
        result = ne.evaluate(args.get('expression'))
        return {"content": [{"type": "text", "text": f"計算結果: {result}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"錯誤: {str(e)}"}]}

tools_mcp = create_sdk_mcp_server(
    name="General tools",
    version="2.0.0",
    tools=[calculator]
)

options = ClaudeAgentOptions(
    system_prompt="你是一個樂於助人的助手。",
    mcp_servers={"extra_tools": tools_mcp},
    allowed_tools=["Read", "Write", "Bash", "mcp__extra_tools__calculator"],
    permission_mode="acceptEdits"
)
```

### 自訂工具開發

使用 `@tool` 裝飾器定義工具：

```python
from claude_agent_sdk import tool
from typing import Any

@tool(
    name="my_tool",               # 工具名稱
    description="Tool description",  # 工具描述（供 AI 理解用途）
    input_schema={"param": str}    # 輸入參數定義
)
async def my_tool(args: dict[str, Any]) -> dict[str, Any]:
    # 工具實作邏輯
    result = do_something(args.get('param'))

    # 返回格式
    return {
        "content": [
            {"type": "text", "text": f"結果: {result}"}
        ]
    }
```

## 技術細節

### 異步處理
- 所有 Claude API 互動都是異步的，使用 `async`/`await` 和 `anyio`
- 回應是串流式處理（`async for`），逐步接收訊息
- 互動對話使用 `aioconsole.ainput` 進行非同步輸入

### 訊息類型
- **TextBlock** - 文字回應內容
- **ToolUseBlock** - 工具呼叫請求（包含工具名稱和參數）
- **ToolResultBlock** - 工具執行結果

### 記憶機制
- **無記憶**：使用 `query()` 函數，每次查詢獨立
- **有記憶**：使用 `ClaudeSDKClient`，在迴圈外建立 client 實例
  - Client 自動保存對話歷史
  - 需要使用 `async with` 管理生命週期
  - 使用 `receive_response()` 確保每次對話完整結束

### 權限管理
- **permission_mode** - 權限模式設定
  - `"default"` - 危險操作需要確認（推薦）
  - `"acceptEdits"` - 自動接受檔案編輯
  - `"bypassPermissions"` - 繞過所有權限檢查（僅限測試）
- **allowed_tools** - 明確指定可用的工具清單

### 錯誤處理
- 使用 `try-except` 捕捉例外
- 互動程式使用 `continue` 保持對話，不因錯誤而中斷
- 捕捉 `KeyboardInterrupt` 和 `EOFError` 處理使用者中斷

## 參考資源

- [Claude Agent SDK 官方文檔](https://docs.anthropic.com/claude/docs/agent-sdk)
- [Quick Getting Started Guide (YouTube)](https://www.youtube.com/watch?v=Lh4IV9MLnuI)
- [Anthropic API Reference](https://docs.anthropic.com/claude/reference)
- [Claude Code 工具文檔](https://docs.claude.com/en/docs/claude-code)

## 常見問題

### Q: 如何切換 AI 模型？
在 `ClaudeAgentOptions` 中設定 `model` 參數：
```python
model="claude-sonnet-4-5-20250929"  # Sonnet 4.5（推薦）
model="claude-opus-4-20250514"      # Opus 4（更強但較慢）
model="claude-haiku-4-5-20250929"   # Haiku 4.5（更快但較弱）
```

### Q: 為什麼對話沒有記憶？
確保：
1. 使用 `ClaudeSDKClient` 而非 `query()` 函數
2. Client 實例在 while 迴圈外建立
3. 使用 `receive_response()` 而非 `receive_messages()`

### Q: 如何啟用網路搜尋？
在 `allowed_tools` 中加入：
```python
allowed_tools=["WebSearch", "WebFetch", "Read", "Write", "Bash"]
```

### Q: 工具整合失敗怎麼辦？
檢查：
1. 工具名稱格式：`mcp__<server_name>__<tool_name>`
2. `mcp_servers` 設定正確
3. `permission_mode` 設定為 `"acceptEdits"` 或 `"bypassPermissions"`

## 授權

MIT License

## 貢獻

歡迎提交 Issues 和 Pull Requests！

## 開發環境

- 程式語言：Python 3.10+
- IDE：VSCode（推薦）
- 套件管理：uv
