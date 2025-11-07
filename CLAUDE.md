# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

這是一個 Claude Agent SDK 的實驗專案（ClaudeAgentSDKLab），用於測試和學習 Claude Agent SDK 的基本查詢功能。專案使用 Python 語言，並透過 `uv` 工具管理虛擬環境。

## 開發環境設定

### 虛擬環境
- 使用 `uv` 工具建立和管理虛擬環境
- 虛擬環境位於 `.venv` 目錄

### 環境變數
- API 金鑰等敏感資料存放在 `.env.local` 文件中
- 程式會從 `.env` 檔案載入環境變數（使用 `dotenv` 套件）
- 系統環境變數優先於 `.env` 中的設定（`load_dotenv()` 預設不覆蓋）

## 執行程式

```bash
python main.py
```

主程式會：
1. 載入 `.env` 環境變數
2. 執行預設的查詢範例（計算數學問題、天氣查詢等）
3. 顯示開始和結束時間戳記

## 程式架構

### 核心模組

**basic_query.py**
- 提供 `basic_query(prompt: str)` 異步函數
- 封裝 Claude Agent SDK 的基本查詢邏輯
- 使用 `claude-sonnet-4-5-20250929` 模型
- 系統提示詞設定為中文助手，會展示工作步驟
- 使用 `query()` 函數進行串流式回應處理

**main.py**
- 主要入口點
- 載入環境變數
- 使用 `anyio.run()` 執行異步查詢
- 包含 `now_str()` 工具函數用於格式化時間戳記

### Claude Agent SDK 使用模式

```python
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

## 重要技術細節

- 所有 Claude API 互動都是異步的，使用 `async`/`await` 和 `anyio`
- 回應是串流式處理（`async for`），逐步接收 `AssistantMessage`
- 訊息內容包含多個區塊（blocks），需要過濾 `TextBlock` 來取得文字回應
- 程式預設使用繁體中文進行互動
