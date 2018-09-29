#coding=utf-8
'''
name : 2018-09-29
httpserver
获取http请求
解析http请求
将请求发送给WebFrame
从WebFarme接受反馈数据
将数据组织为Response格式发送给客户端
'''

from socket import *
import sys
import re
from threading import Thread #多线程并发
from setting import * #配置文件模块
import time
 
class HTTpServer(object):
    def __init__(self, addr = ('0.0.0.0',80)): #先初始化
        #在创建套接子
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.bind(addr)

    #绑定
    def bind(self,addr):
        self.ip = addr[0] #ip地址
        self.port = addr[1]
        self.sockfd.bind(addr)
    # 启动服务器
    def serve_forever(self):
        #监听客户端
        self.sockfd.listen(10)
        print('Listen the port %d...'%self.port)
        #循环接收
        while True:
            connfd,addr = self.sockfd.accept()
            print('Connect from',addr)
            #启动线程
            handle_client = Thread(target = self.handle_request,args = (connfd,))
            handle_client.setDaemon(True)
            handle_client.start()

    def handle_request(self, connfd):
        #接受浏览器请求
        request = connfd.recv(4096)
        # print(request)
        request_lines = request.splitlines()
        #获取请求行
        request_line = request_lines[0].decode()
        #正则提取请求方法和内容
        pattern = r'(?P<METHOO>[A-Z]+)\s+(?P<PATH>/\S*)'
        try:
            env = re.match(pattern, request_line).groupdict() #形成字典
        except:
            response_handlers = 'HTTP/1.1 500 Server Error\r\n'
            response_handlers += '\r\n'
            response_Boby = 'Sorry argv'
            response = response_handlers + response_Boby
            connfd.send(response.encode())
            return
        print(env)
        #将请求发送给frame 得到返回数据结果
        status,response_Boby = \
        self.send_request(env['METHOO'], env['PATH'])

        #根据响应吗组织响应头内容
        response_handlers = self.get_headlers(status)

        #　将结果组织为http response 发送给客户端
        response = response_handlers + response_Boby
        connfd.send(response.encode())
        connfd.close()

    # 和frame 交互　发送request获取response 
    def send_request(self, method, path): #输入客户端
        #创建套接子发送
        s = socket()
        s.connect(frame_addr)

        #向Webframe发送method 和 path
        s.send(method.encode())
        time.sleep(0.1)
        s.send(path.encode())

        status = s.recv(128).decode()
        # while True:
        response_Boby = s.recv(4096).decode()
        return status,response_Boby
        # return '200','httpserver test'

    def get_headlers(self,status):
        if status == '200':
            response_handlers = 'HTTP/1.1 200 OK\r\n'
            response_handlers += '\r\n'
            # response_Boby = 
        elif status == '404':
            response_handlers = 'HTTP/1.1 404 NOT Fouund\r\n'
            response_handlers += '\r\n'

        return response_handlers

if __name__ == '__main__':
    #测试
    httpd = HTTpServer(ADDR)
    httpd.serve_forever()