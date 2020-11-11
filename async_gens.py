import socket
import select

tasks = []
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
        client(client_socket)


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

        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock)) # получаем генератор из словаря по ключу sock и добавляем в tasks

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            # передаем в task генератор
            task = tasks.pop(0)


tasks.append(server())
