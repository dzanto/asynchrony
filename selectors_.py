import socket
import selectors

selector = selectors.DefaultSelector()


def server():
    # create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()
    selector.register(
        fileobj=server_socket,
        events=selectors.EVENT_READ,
        data=accept_connection
    )


def accept_connection(server_socket):
    print('Before .accept()')
    # accept an incoming connection - принять входящиее подключение
    # accept блокирующая функция, ждет входящее подключение
    # после подключения создаем client_socket
    client_socket, addr = server_socket.accept()
    print('Connection from', addr)
    selector.register(
        fileobj=client_socket,
        events=selectors.EVENT_READ,
        data=send_message
    )


def send_message(client_socket):
    print('Before .recv()')
    # await receiving a message from a client
    request = client_socket.recv(4096)
    decode_request = request.decode('utf-8')
    print('Client request = ', decode_request)

    if request:
        response = 'Hello world\r\n'.encode()
        # send a message to a client
        client_socket.send(response)
    else:
        # close connection
        print('Disconnect')
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:
        # возвращаем список кортежей SelectorKey (key, events)
        events = selector.select()

        # SelectorKey
        # fileobj - наш socket
        # events
        # data

        for key, _ in events:
            # возвращаем нашу функцию из data
            callback = key.data
            # запускаем функцию и передаем в нее socket
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()

# command for telnet: open servadr port. For example: open localhost 5000
