# -*- coding:utf-8 -*-
"""
Chat room server
env: python3.5
exc: for socket and fork
"""

from socket import *
import os, sys

# 服务端地址
ADDR = ("0.0.0.0",9009)
# 存储用户信息{name:addr}
user = {}

# 搭建网络连接
def udp_server():
    # 创建套接字
    sockfd = socket(AF_INET,SOCK_DGRAM)
    sockfd.bind(ADDR)
    return sockfd

def do_login(s, name, addr):
    if (name in user) or ("管理员" in name):
        s.sendto("用户昵称冲突".encode(),addr)
        return
    s.sendto("OK".encode(),addr)
    # 通知其他人
    msg = "\n欢迎 %s 进入聊天室"%name
    for i in user:
        s.sendto(msg.encode(),user[i])
    # 新用户加入字典
    user[name] = addr

def do_chat(s,name,text):
    msg = "\n%s : %s"%(name,text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])

def do_quit(s,name):
    msg = "\n%s 退出了聊天室"%name
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])
        else:
            s.sendto("EXIT".encode(),user[i])
    del user[name]

def request(s):
    while True:
        data, addr = s.recvfrom(1024)
        msgList = data.decode().split(" ")
        # 区分请求类型
        if msgList[0] == "L":
            do_login(s, msgList[1], addr)
        elif msgList[0] == "C":
            # 重组消息
            text = " ".join(msgList[2:])
            do_chat(s,msgList[1],text)
        elif msgList[0] == "Q":
            do_quit(s,msgList[1])


def main():
    s = udp_server()
    # 单独创建进程发送管理员信息
    pid = os.fork()
    if pid < 0:
        print("Error")
    elif pid == 0:
        while True:
            msg = input("管理员消息>>")
            msg = "C 管理员消息 " + msg
            # 发送给父进程
            s.sendto(msg.encode(),ADDR)    
    else:
        request(s)# 接收请求


main()

