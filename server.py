import socket


UDP_MAX_SIZE = 65535  # задаем маскимальный размер сообщения

def listen (host: str = '127.0.0.1', port: int = 3000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # создаем сокет с адресным пространством IPv4 и с протоколом UDP

    s.bind((host, port))  # привязываем сокет к нашему дефолтному адресу и к нему можно конектиться
    print(f'Listening at {host}:{port}')

    members=[]
    while True:
        msg, addr = s.recvfrom(UDP_MAX_SIZE)  # получаем само сообщение и адрес откуда оно пришло

        if addr not in members:  # если клиента нет в списке чата, то добавляем его
            members.append(addr)

        if not msg:  # если сообщение пустое то ничего не делаем
            continue

        client_id = addr[1]  # говорим что клиент присоединился к чату и в качестве его id используем его порт
        if msg.decode('ascii') == '__join':
            print(f'Cleint {client_id} joined chat')
            continue

        msg = f'client{client_id}: {msg.decode("ascii")}'  # говорим серверу отравлять сообщение всем кроме самого отправителя сообщения
        for member in members:
            if member == addr:
                continue

            s.sendto(msg.encode('ascii'), member)


if __name__ == '__main__':
    listen()
