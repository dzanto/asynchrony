import socket
from select import select

tasks = []
#ключи словарей - сокеты, а значения - генераторы
to_read = {}
to_write = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        yield ('read', server_socket)
        client_socket, addr = server_socket.accept()
        print('Connection from', addr)
        # добавляем генератор с клиентским сокетом в список задач
        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        yield ('read', client_socket)
        print('Before .recv()')
        request = client_socket.recv(4096)
        decode_request = request.decode('utf-8')
        print('Client request = ', decode_request)

        if not request:
            print('No data')
            break
        else:
            response = 'Hello world\r\n'.encode()
            yield ('write', client_socket)
            client_socket.send(response)

    client_socket.close()


def event_loop():
    while any([tasks, to_read, to_write]): # если один из списков или словарей пустой, any вернет False

        # если список пустой обеспечиваем список tasks новыми элементами
        while not tasks:
            #селект в цикле проверяет готовность сокетов на чтение или запись, и возвращает ключи - сокеты в виде списков.
            #если буфер наполнился, из него можно читать. Если буфер опустел, в него можно записать.
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock)) # получаем генератор из словаря по ключу sock и добавляем в tasks

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            # Извлекаем из списка tasks генератор - задачу
            task = tasks.pop(0)
            # reason, sock = ('read', server_socket) or ('read', client_socket) or ('write', client_socket)
            reason, sock = next(task)

            # записывает генератор в словарь to_read или to_write в зависимости от метки 'read' или 'write'
            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task

        except StopIteration:
            print('Done!')


tasks.append(server())
event_loop()
