#coding = utf-8

'''
WebFrame：
从httpserver 接收具体请求
更具请求进行逻辑处理和数据处理
静态页面
逻辑数据
讲需要的数据反馈给客户端httpserver
'''

from socket import *
from setting import *
import time
from urls import *
from views import *

class Application(object):
    def __init__(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(frame_addr)

    #启动
    def start(self):
        self.sockfd.listen(5)
        while True:
            connfd, addr = self.sockfd.accept()
            #第一次接收方法
            method = connfd.recv(128).decode()
            #接受请求内容
            path = connfd.recv(128).decode()
            # print(method,path)

            if method =='GET':
                if path == '/' or path[-5:] == '.html':
                    status,response_Boby = self.get_html(path)
                else:
                    status,response_Boby = self.get_data(path)
                #结果给httpserver
                connfd.send(status.encode())
                time.sleep(0.1)
                connfd.send(response_Boby.encode())

            elif method == 'POST':
                pass

    def get_html(self, path):
        if path == '/':
            get_file = STATIC + './index.html'
        else:
            get_file =STATIC + path
        try:
            f = open(get_file)
        except IOError:
            response = ('404','===Sorry not found the page===')
        else:
            response = ('200',f.read())
        finally:
            return response


    def get_data(self,path):
        for url,handler in urls:
            if path == url:
                response_Boby = handler()
                return '200', response_Boby
        return '404' , 'Sorry,Not found the data'


if __name__ == '__main__':
    app = Application()
    app.start() #启动框架等待request