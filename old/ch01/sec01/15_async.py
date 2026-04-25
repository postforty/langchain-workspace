# 비동기 프로그래밍(async/await)
import asyncio

async def fetch_data(delay):
    print(f"시작(딜레이: {delay})")
    await asyncio.sleep(delay)
    print(f"완료(딜레이: {delay})")
    return f"딜레이: {delay}"

async def main():
    task1 = asyncio.create_task(fetch_data(2))
    task2 = asyncio.create_task(fetch_data(1))

    result = await asyncio.gather(task1, task2)
    print(f"결과: {result}")

asyncio.run(main())