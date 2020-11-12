import asyncio
queue = []


async def counter():
    counter = 0
    while True:
        print(counter)
        counter += 1
        await asyncio.sleep(1)


async def bang():
    counter = 0
    while True:
        if counter % 3 == 0:
            print('Bang')
        counter += 1
        await asyncio.sleep(1)


async def main():
    task1 = asyncio.create_task(counter())
    task2 = asyncio.create_task(bang())

    await asyncio.gather(task1, task2)


if __name__ == '__main__':
    asyncio.run(main())
