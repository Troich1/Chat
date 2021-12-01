import socket
import threading
import os
import time
from multiprocessing import Process, Pipe
from datetime import datetime


UDP_MAX_SIZE = 65535 # задаем маскимальный размер сообщения


def listen(s: socket.socket):  # создаем сокет, который бесконечно слушает и при получении сообщения выводит его
    while True:
        msg = s.recv(UDP_MAX_SIZE)
        print ('\r\r' + msg.decode('ascii') + '\n' + f'you: ', end='')


def connect(Process, host: str = '127.0.0.1', port: int = 3000):

    def __init__(self, end):
        Process.__init__(self)
        self.end = end

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # создаем сокет с адресным пространством IPv4 и с протоколом UDP

    s.connect((host, port))  #конектмися к серверу

    threading.Thread(target=listen, args=(s,), daemon=True).start()  # создаем тред с фукцией listlen, чтобы слушать на фоне чат

    s.send('__join'.encode('ascii'))  # говорим серверу что присоединилсь к чату

    while True:  # даем возможность бесконечно писать в чат
        msg = input(f'you: ')
        s.send(msg.encode('ascii'))


class Timer(Process):  # создаем таймер, который будет работать как отдельный процесс и раз в 20 сек выводить время
    def __init__(self, server_point):
        Process.__init__(self)
        self.server_point = server_point

    def run(self):
        while 1:
            current_time = datetime.now()
            time.sleep(20)
            print(current_time)
        self.server_point.close()

if __name__ == '__main__':
    os.system('clear')
    print('Welcome to chat!')

    tm = Timer(Pipe()).start()
    con = connect(Pipe()).start()
    tm.join()
    con.join()





