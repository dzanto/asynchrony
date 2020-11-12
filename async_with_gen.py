from time import sleep
queue = []


def counter():
    counter = 0
    while True:
        print(counter)
        counter += 1
        yield


def bang():
    counter = 0
    while True:
        if counter % 3 == 0:
            print('Bang')
        counter += 1
        yield


def main(queue):
    while True:
        task = queue.pop(0)
        next(task)
        queue.append(task)
        sleep(0.5)


if __name__ == '__main__':
    cnt = counter()
    ban = bang()
    queue.append(cnt)
    queue.append(ban)
    main(queue)
