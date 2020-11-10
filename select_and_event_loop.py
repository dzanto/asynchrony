import socket
from select import select


to_monitor = []


# create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()

def accept_connection(server_socket):
    while True:
        print('Before .accept()')
        # accept an incoming connection - принять входящиее подключение
        # accept блокирующая функция, ждет входящее подключение
        client_socket, addr = server_socket.accept()
        print('Connection from', addr)
        send_message(client_socket)


def send_message(client_socket):
    while True:
        print('Before .recv()')
        # await receiving a message from a client
        request = client_socket.recv(4096)
        decode_request = request.decode('utf-8')
        print('Client request = ', decode_request)

        if not request:
            print('No data')
            break
        else:
            response = 'Hello world\r\n'.encode()
            # send a message to a client
            client_socket.send(response)

    # close connection after a disconnecting by the client
    print('Disconnect')
    client_socket.close()


def event_loop():
    while True:
        ready_to_read, _, _ = select(to_monitor, [], [])


if __name__ == '__main__':
    to_monitor.append(server_socket)
    # accept_connection(server_socket)

# command for telnet: open servadr port. For example: open localhost 5000
