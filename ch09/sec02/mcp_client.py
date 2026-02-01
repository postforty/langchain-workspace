import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def main():
    try:
        async with client:
            tools_list = await client.list_tools()
            print("도구 목록:", tools_list)

            res_hello = await client.call_tool("hello", {"name": "김일남"})
            print("hello 도구 호출 결과:", res_hello)

            res_content = await client.read_resource("simple://info")
            print("결과:", res_content)
    except:
        pass

if __name__ == "__main__":
    asyncio.run(main())