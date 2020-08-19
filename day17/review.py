from socket import *
from select import select
import  re

class WebServer():
    def __init__(self,html = None,host = "0.0.0.0",port = 80):
        self.html = html
        self.host = host
        self.port= port
        self.rlist = []
        self.wlist = []
        self.xlist = []

        self.set_socket()
        self.bind_socket()

    def set_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)

    def bind_socket(self):
        self.add = (self.host,self.port)
        self.sock.bind(self.add)

    def handle(self,connfd):
        data = connfd.recv(1024*10).decode()
        pattern = r"[A-Z]+\s+(?P<info>/\S*)"
        result = re.match(pattern,data)
        if result:
            info = result.group("info")
            print(f"收到请求{info}")
            self.send_html(connfd,info)
        else:
            self.rlist.remove(connfd)
            connfd.close()
            return

    def send_html(self,reslut,info):
        pass

    def start(self):
        self.sock.listen(5)
        print("Listen...",self.port)
        self.rlist.append(self.sock)
        while True:
            rs,ws,xs = select(self.rlist,self.wlist,self.xlist)
            for r in rs:
                if r is self.sock:
                    connfd,addr = r.accept()
                    connfd.setblocking(False)
                    self.rlist.append(connfd)
                    print("Connect:",addr)
                else:
                    try:
                        self.handle(r)
                    except:
                        r.close()
                        self.rlist.remove(r)


if __name__ == '__main__':
    httfd = WebServer(html = "/home/tarena/month02/day17/static",
                      host = "127.0.0.1",
                      port = 1231)

    httfd.start()