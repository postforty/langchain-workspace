import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp") # HTTP(SSE)
# client = Client(r"D:\wsh\langchain-workspace\ch09\sec03\mcp_server.py") # stdio

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)

asyncio.run(call_tool("김일남"))