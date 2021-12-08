import socket
import time
import sys
from multiprocessing import Process, Pipe
from threading import Thread
from datetime import datetime



class Server(Thread):
    def __init__(self, end, port):
        Thread.__init__(self)
        self.end = end
        self.port = port


    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Server started successfully\n")
        hostname = ''  # символическое имя обозначающее все доступные интерфейсы подкл
        port = self.port
        self.sock.bind((hostname, port))
        self.sock.listen(1)
        print("Listening on port %d\n" % port)
        (clientname, address) = self.sock.accept()
        print("Connection from %s\n" % str(address))
        while 1:
            chunk = clientname.recv(4096)
            buf = self.end.recv()
            print(buf)
            print('\n' + str(address) + '-', buf, ':' + str(chunk, encoding='UTF-8'))


class Client(Thread, *sys.argv[1:]):
    def __init__(self, end):
        Thread.__init__(self)
        self.end = end

    def connect(self, host, port):
        self.sock.connect((host, port))

    def client(self, host, port, msg, ):
        sent = self.sock.send(bytes(msg, encoding='UTF-8'))
        buf = self.end.recv()  # принимаем данные от таймера
        print("YOU " , buf, ':' + msg)

    def run(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            host = input("Enter the hostname (IP)\n>>")
            port = int(input("Enter the port\n>>"))
        except EOFError:
            print('err')
            return 1

        print("Connecting\n")
        self.connect(host, port)
        print("Connected\n")
        while 1:
            msg = input('>>')
            if msg == '':
                continue
            self.client(host, port, msg)
        return (1)


class Net(Process):  # процесс чата с двумя потоками (сервер и клиент)

    def __init__(self, end, port):
        Process.__init__(self)
        self.end = end
        self.port = port

    def run(self):
        sys.stdin = open(0)
        srv = Server(self.end, self.port)  # инициализация сервера
        srv.daemon = True  # ставим его в режим демона для постоянной фоновой работы
        print("Starting server")
        srv.start()  # запускаем
        time.sleep(1)
        print("Starting client")
        cli = Client(self.end)
        cli.start()
        print("Started successfully")


class Time(Process):

    def __init__(self, begin):
        Process.__init__(self)

        self.begin = begin

    def sd(self, date):
        self.begin.send(date)  # отправляем данные процессу на другом конце пайпа

    def run(self):

        while True:
            timeval = datetime.now()
            time.sleep(1)
            self.sd(timeval)
        self.begin.close()






if __name__ == '__main__':
    port = int(input("Input your port: "))  # вводим удобный для нас порт
    print('\n')
    end, begin = Pipe()  # используем пайп чтобы наши процессы работали без блокировки и чтобы время передавалось в чат
    nt = Net(end, port)  # инициализируем процесс P2P соединения
    nt.start()  # запускаем наш чат
    tm = Time(begin)  # инициализируем процесс таймера
    tm.start()  # запускаем таймер
    nt.join()
    tm.join()
