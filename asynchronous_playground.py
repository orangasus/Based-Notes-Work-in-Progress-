import asyncio


async def task0():
    for i in range(0, 20):
        print(i)
        await asyncio.sleep(0.5)

async def task1():
    print("Task 1 started")
    await asyncio.sleep(1)
    print("Task 1 finished")

async def task2():
    print("Task 2 started")
    await asyncio.sleep(1)
    print("Task 2 finished")

# Using await sequentially
async def main():
    await asyncio.gather(task0(), task1(), task2())

asyncio.run(main())