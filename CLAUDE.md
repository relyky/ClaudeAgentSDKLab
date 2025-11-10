# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

這是一個 Claude Agent SDK 的實驗專案（ClaudeAgentSDKLab），用於測試和學習 Claude Agent SDK 的各種功能，包含基本查詢、多輪對話、記憶功能和工具整合。專案使用 Python 語言，並透過 `uv` 工具管理虛擬環境。

## 專案功能特性

本專案展示 Claude Agent SDK 的多種使用模式：

### 1. 基本查詢（無記憶）
- 檔案：`main_basic_query.py` + `basic_query.py`
- 功能：單次問答，每次查詢獨立
- 適用：簡單的一問一答場景
- 特點：使用 `query()` 函數，無狀態

### 2. 互動對話（無記憶）
- 檔案：`main_basic_interactive.py` + `basic_query.py`
- 功能：持續對話但不記憶歷史
- 適用：不需要上下文的連續查詢
- 特點：使用 `query()` 函數在迴圈中

### 3. 互動對話（有記憶）
- 檔案：`main_client_interactive.py` + `interactive_terminal.py`
- 功能：多輪對話，自動記憶對話歷史
- 適用：需要上下文的複雜對話
- 特點：使用 `ClaudeSDKClient`，支援 WebSearch、WebFetch 等工具

### 4. Agent 與工具整合
- 檔案：`main_client_use_tools.py` + `agent_with_tools.py`
- 功能：整合自訂工具（計算器範例）
- 適用：需要特殊能力的 Agent 應用
- 特點：使用 MCP 伺服器、`@tool` 裝飾器

## 開發環境設定

### 虛擬環境
- 使用 `uv` 工具建立和管理虛擬環境
- 虛擬環境位於 `.venv` 目錄

### 環境變數
- API 金鑰等敏感資料存放在 `.env.local` 檔案中
- 程式會從 `.env` 檔案載入環境變數（使用 `dotenv` 套件）
- 系統環境變數優先於 `.env` 中的設定（`load_dotenv()` 預設不覆蓋）

### 套件依賴
專案使用 `requirements.txt` 管理依賴：
- `claude-agent-sdk==0.1.6` - Claude AI Agent 核心 SDK
- `aioconsole==0.8.2` - 非同步控制台輸入/輸出
- `anyio==4.11.0` - 異步 I/O 執行環境
- `python-dotenv==1.2.1` - 環境變數管理
- `numexpr==2.10.2` - 數值表達式求值器（用於計算器工具）

## 執行程式

### 基本查詢範例
```bash
python main_basic_query.py
```
執行兩個預設查詢範例：
- 數學計算問題（1234 * 567）
- 天氣詢問

主程式會：
1. 載入 `.env` 環境變數
2. 執行預設的查詢範例
3. 顯示開始和結束時間戳記

### 互動對話（無記憶）
```bash
python main_basic_interactive.py
```
啟動互動式命令列介面：
- 每次查詢獨立，不記憶對話歷史
- 輸入 `exit` 或 `quit` 離開

### 互動對話（有記憶）
```bash
python main_client_interactive.py
```
啟動具有記憶功能的對話：
- 自動記憶對話歷史
- 可進行多輪上下文對話
- 支援 WebSearch、WebFetch、Read、Write、Bash 等工具
- 輸入 `exit` 或 `quit` 離開

### 工具整合範例
```bash
python main_client_use_tools.py
```
展示如何整合自訂工具：
- 內建計算器工具（使用 `numexpr`）
- 展示 MCP 伺服器整合
- 處理 ToolUseBlock 和 ToolResultBlock

## 程式架構

### 核心模組

#### basic_query.py
提供基礎查詢功能：
- `basic_query(prompt: str)` - 執行單次查詢
  - 封裝 Claude Agent SDK 的基本查詢邏輯
  - 使用 `claude-sonnet-4-5-20250929` 模型
  - 系統提示詞設定為中文助手
  - 使用 `query()` 函數進行串流式回應處理
- `start_chat_loop()` - 無記憶互動對話迴圈
  - 持續接受使用者輸入
  - 每次查詢獨立，不保留歷史
  - 使用 `input()` 處理同步輸入

#### interactive_terminal.py
提供有記憶的互動對話：
- `start_chat_continuous()` - 有記憶互動對話
  - 使用 `ClaudeSDKClient` 保持對話狀態
  - 使用 `aioconsole.ainput` 處理非同步輸入
  - 使用 `receive_response()` 確保每次對話完整結束
  - 支援 WebSearch、WebFetch、Read、Write、Bash 等工具
  - 錯誤處理使用 `continue` 保持對話不中斷

#### agent_with_tools.py
展示工具整合：
- `start_chat_tools()` - 整合自訂工具的對話
  - 定義計算器工具（使用 `@tool` 裝飾器）
  - 使用 `create_sdk_mcp_server` 建立 MCP 伺服器
  - 處理 `ToolUseBlock` 和 `ToolResultBlock`
  - 支援複雜數學表達式運算

### 主程式入口

#### main_basic_query.py
- 執行預設查詢範例
- 展示時間戳記記錄
- 適合測試 API 連線

#### main_basic_interactive.py
- 啟動無記憶互動對話
- 使用 `start_chat_loop()`

#### main_client_interactive.py
- 啟動有記憶互動對話
- 使用 `start_chat_continuous()`
- 載入環境變數

#### main_client_use_tools.py
- 啟動工具整合範例
- 使用 `start_chat_tools()`
- 展示 MCP 伺服器整合

### Claude Agent SDK 使用模式

#### 模式 1：基本查詢（無狀態）

適用於單次查詢，不需要保留對話歷史。

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock

options = ClaudeAgentOptions(
    system_prompt="你是一個樂於助人的助手。你會說中文並展示你的工作步驟。",
    max_turns=None,
    model="claude-sonnet-4-5-20250929"
)

async for message in query(prompt=prompt, options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
```

#### 模式 2：ClaudeSDKClient（有狀態）

適用於多輪對話，自動保留對話歷史。

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock
from aioconsole import ainput

options = ClaudeAgentOptions(
    system_prompt="你是一個樂於助人的助手。你會說中文並展示你的工作步驟。你可以搜尋網路獲取最新資訊。",
    max_turns=None,
    model="claude-sonnet-4-5-20250929",
    permission_mode="default",
    allowed_tools=["WebSearch", "WebFetch", "Read", "Write", "Bash"]
)

async with ClaudeSDKClient(options=options) as client:
    while True:
        user_input = (await ainput(">>>")).strip()

        if user_input.lower() in ['exit', 'quit']:
            break
        elif user_input:
            await client.query(prompt=user_input)
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"Claude: {block.text}")
```

**重要**：
- 使用 `receive_response()` 而非 `receive_messages()`
- `receive_response()` 會在收到 `ResultMessage` 後自動終止
- Client 實例在 while 迴圈外建立，自動保留對話歷史

#### 模式 3：工具整合

適用於需要擴展 AI 能力的應用，整合自訂工具。

```python
from claude_agent_sdk import (
    tool,
    create_sdk_mcp_server,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    AssistantMessage,
    UserMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock
)
from typing import Any
import numexpr as ne

# 定義工具
@tool(
    name="calculator",
    description="Evaluate mathematical expressions using Python syntax",
    input_schema={"expression": str}
)
async def calculator(args: dict[str, Any]) -> dict[str, Any]:
    try:
        result = ne.evaluate(args.get('expression'))
        return {
            "content": [
                {"type": "text", "text": f"計算結果: {result}"}
            ]
        }
    except Exception as e:
        return {
            "content": [
                {"type": "text", "text": f"計算錯誤: {str(e)}"}
            ]
        }

# 建立 MCP 伺服器
tools_mcp = create_sdk_mcp_server(
    name="General tools",
    version="2.0.0",
    tools=[calculator]
)

# 設定選項
system_prompt = """你是一個樂於助人的助手。你會說中文並展示你的工作步驟。
你有計算器工具可以計算數學表達式。"""

options = ClaudeAgentOptions(
    system_prompt=system_prompt,
    mcp_servers={"extra_tools": tools_mcp},
    allowed_tools=["Read", "Write", "Bash", "mcp__extra_tools__calculator"],
    permission_mode="acceptEdits",
    max_turns=None,
    model="claude-sonnet-4-5-20250929"
)

# 使用 Client
async with ClaudeSDKClient(options=options) as client:
    await client.query(prompt=user_input)
    async for message in client.receive_response():
        if isinstance(message, UserMessage):
            # 處理工具執行結果
            for block in message.content:
                if isinstance(block, ToolResultBlock):
                    print(f"工具結果: {block.content}")
        elif isinstance(message, AssistantMessage):
            # 處理 AI 回應
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
                elif isinstance(block, ToolUseBlock):
                    print(f"使用工具: {block.name}")
```

**重要**：
- 工具名稱格式：`mcp__<server_name>__<tool_name>`
- 需要設定 `permission_mode` 為 `"acceptEdits"` 或 `"bypassPermissions"`
- 需要處理 `ToolUseBlock` 和 `ToolResultBlock`

## 重要技術細節

### 異步處理
- 所有 Claude API 互動都是異步的，使用 `async`/`await` 和 `anyio`
- 回應是串流式處理（`async for`），逐步接收 `AssistantMessage`
- 互動對話使用 `aioconsole.ainput` 進行非同步輸入
- 同步輸入使用標準 `input()` 函數（無記憶模式）

### 訊息處理
- 訊息內容包含多個區塊（blocks）
- **TextBlock** - 文字回應內容
- **ToolUseBlock** - 工具呼叫請求（包含工具名稱和參數）
- **ToolResultBlock** - 工具執行結果
- **ThinkingBlock** - AI 的思考過程（extended thinking 模式）

### 記憶機制
- **無記憶**：使用 `query()` 函數，每次查詢獨立
  - 適合單次查詢或不需上下文的場景
  - 效能較好，無狀態管理開銷

- **有記憶**：使用 `ClaudeSDKClient`，在迴圈外建立 client 實例
  - Client 自動保存對話歷史
  - 需要使用 `async with` 管理生命週期
  - 使用 `receive_response()` 而非 `receive_messages()`
  - `receive_response()` 在收到 `ResultMessage` 後自動終止

### 錯誤處理
- 使用 `try-except` 捕捉例外
- **無記憶模式**：使用 `break` 中斷對話（basic_query.py）
- **有記憶模式**：使用 `continue` 保持對話，不因錯誤而中斷（interactive_terminal.py）
- 捕捉 `KeyboardInterrupt` 和 `EOFError` 處理使用者中斷

```python
try:
    user_input = await ainput(">>>")
    await client.query(prompt=user_input)
    # 處理回應
except KeyboardInterrupt:
    print("\nBye!")
    break
except EOFError:
    print("\nBye!")
    break
except Exception as e:
    print(f"出現例外！ {e}")
    print("繼續對話...")
    continue  # 保持對話持續
```

### 工具整合
- 使用 `@tool` 裝飾器定義自訂工具
- 透過 `create_sdk_mcp_server` 建立 MCP 伺服器
- 工具名稱格式：`mcp__<server_name>__<tool_name>`
- 需要設定 `allowed_tools` 和 `permission_mode`
- 工具函數必須是 `async` 函數
- 返回格式：`{"content": [{"type": "text", "text": "..."}]}`

### 權限管理
- **permission_mode** - 權限模式設定
  - `"default"` - 危險操作需要確認（推薦）
  - `"acceptEdits"` - 自動接受檔案編輯
  - `"bypassPermissions"` - 繞過所有權限檢查（僅限測試）

- **allowed_tools** - 明確指定可用的工具清單
  - 內建工具：`WebSearch`、`WebFetch`、`Read`、`Write`、`Bash`、`Grep`、`Glob` 等
  - 自訂工具：`mcp__<server_name>__<tool_name>` 格式
  - 空列表表示允許所有工具

### WebSearch 工具
- 僅支援 Anthropic 官方 API（不支援 Bedrock/Vertex）
- 需要在 `allowed_tools` 中明確列出：`["WebSearch", "WebFetch"]`
- 費用：每 1,000 次搜尋 $10 美金
- 支援的模型：Sonnet 4.5、Opus 4、Haiku 4.5 等

### 環境設定
- 程式預設使用繁體中文進行互動
- API 金鑰從 `.env.local` 載入（使用 `python-dotenv`）
- 系統環境變數優先於 `.env` 中的設定
- 支援的環境變數：
  - `ANTHROPIC_API_KEY` - Claude API 金鑰（必須）
  - 其他自訂環境變數

## 常見問題

### 為什麼對話無法進入下一輪？
- 確認使用 `receive_response()` 而非 `receive_messages()`
- `receive_messages()` 不會自動終止，導致迴圈無法繼續

### 為什麼對話沒有記憶？
- 確認使用 `ClaudeSDKClient` 而非 `query()` 函數
- 確認 Client 實例在 while 迴圈外建立

### 如何啟用 WebSearch？
- 在 `allowed_tools` 中加入：`["WebSearch", "WebFetch"]`
- 確認使用 Anthropic 官方 API

### 工具整合失敗怎麼辦？
- 檢查工具名稱格式：`mcp__<server_name>__<tool_name>`
- 確認 `mcp_servers` 設定正確
- 設定 `permission_mode="acceptEdits"` 或 `"bypassPermissions"`

### 如何處理錯誤但不中斷對話？
- 使用 `continue` 而非 `break`
- 參考 `interactive_terminal.py` 的錯誤處理實作
