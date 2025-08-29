import json
import os
from pathlib import Path

from mcp.server import FastMCP

# 初始化 MCP 服务
app = FastMCP("devpilot-architecture")

# 测试一个模型调用
import httpx


@app.tool()
async def web_search(query: str) -> str:
    """
    设计到架构设计就使用这个

    Args:
        query: 要生成的架构描述

    Returns:
        搜索结果的总结（字符串），出错时返回错误描述
    """
    print(f"接收到的参数: {query}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url='https://oneapi.wenxiaobai.com/rockopenai/v1/chat/completions',
                headers={
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Authorization': 'Bearer rock-oj43rpEAmWFzBYV0epKQaEu6PFhkygIa6oekkOFTW3p02',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/json',
                    'User-Agent': 'PostmanRuntime-ApipostRuntime/1.1.0'
                },
                json={
                    'max_tokens': 1024,
                    'model': 'claude-3-7-sonnet-20250219',
                    'messages': [{'role': 'user', 'content': f"{query}"}]
                }
            )
            if response.status_code != 200:
                return f"请求失败，状态码：{response.status_code}\n错误内容：{response.text}"
            else:
                return json.dumps(response.json(), ensure_ascii=False)
        except Exception as e:
            return f"异常 prompt={query} ：{str(e)}"

# 启动 MCP Provider
if __name__ == "__main__":
    app.run(transport='stdio')
