# -*- coding:utf-8 -*-
"""
Chat room client
env: python3.5
exc: for socket and fork
"""

from socket import *
import os,sys

# 服务器地址
# ADDR = ("176.140.7.173",8686)
ADDR = ("176.140.7.75",9009)
# 搭建网络连接
def udp_client():
    # 创建套接字
    return socket(AF_INET,SOCK_DGRAM)

def login(s):
    while True:
        name = input("请输入昵称：\n>>")
        msg = "L " + name# L表示请求类型（和客户端做好约定）
        # 发送给服务端
        s.sendto(msg.encode(),ADDR)
        # 等待回复
        data, addr = s.recvfrom(1024)
        if data.decode() == "OK":
            print("您已进入聊天室,请文明聊天")
            break
        else:
            print(data.decode())
    return name

def send_msg(s,name):
    while True:
        try:
            text = input("发言:")
        except KeyboardInterrupt:
            text = "quit"
        if text.strip() == "quit":
            msg = "Q " + name
            s.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天室")
        msg = "C %s %s"%(name,text)
        s.sendto(msg.encode(),ADDR)

def recv_msg(s):
    while True:
        data, addr = s.recvfrom(2048)
        # 收到服务器EXIT则退出
        if data.decode() == "EXIT":
            sys.exit()
        print(data.decode(),"\n发言：",end="")

def chat(s,name):
    # 创建进程    
    p = os.fork()
    if p < 0:
        sys.exit("Error!")
    elif p == 0:
        send_msg(s,name)
    else:
        recv_msg(s)




def main():
    s = udp_client()
    name = login(s)
    chat(s,name)


main()