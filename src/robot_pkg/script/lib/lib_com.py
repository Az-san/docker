#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#==================================================
## @file lib_com
## @author Takumi FUJI
## @brief ライブラリクラス
#==================================================




#==================================================
# import
#==================================================
import sys
import roslib
import socket
import requests

sys.path.append(roslib.packages.get_pkg_dir("robot_pkg") + "/script/import")
from common_import import *

class LibCom:
    def __init__(self):
        self._lib = {}
        self.esp_ip = None

    def initSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("172.17.0.2", 52350))  # 自身のIPアドレスとポート番号を指定
        print("waiting...")
        self.sock.listen(5)
        self.clientsocket, self.address = self.sock.accept()
        print(f"Connection from {self.address} has been established!")
        self.clientsocket.settimeout(15)

    def readSocket(self):
        try:
            recvline = self.clientsocket.recv(1024).decode()
            print(recvline)
        except:
            print("Socket timeout...")
            recvline = None
        return recvline

    def readSocketConv(self):
        try:
            recvline = self.clientsocket.recv(1024).decode()
        except socket.timeout:
            return None

        print(recvline)
        if recvline == "^":
            data = [1, 0, 0, 0]
        elif recvline == "v":
            data = [0, 1, 0, 0]
        elif recvline == ">":
            data = [0, 0, 1, 0]
        elif recvline == "<":
            data = [0, 0, 0, 1]
        elif recvline == "exit":
            data = recvline
        else:
            print("Socket error!")
        return data

    def openArduino(self, esp_ip):
        # ESP8266のIPアドレスを初期化
        self.esp_ip = esp_ip
        print(f"Connected to ESP8266 at {esp_ip}")
        return

    def writeArduino(self, message):
        if self.esp_ip is None:
            print("ESP8266 IP is not set.")
            return
        
        try:
            url = f"http://{self.esp_ip}/send"
            response = requests.post(url, data={'message': message})
            if response.status_code == 200:
                print(f"Message '{message}' sent to Arduino.")
            else:
                print(f"Failed to send message. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error during sending message: {e}")
        return

    def closeArduino(self):
        # Wi-Fi通信のため、特にシリアルポートの終了は不要
        print("Closed connection to ESP8266.")
        return

    def delete(self):
        self.clientsocket.close()
        self.sock.close()
        self.closeArduino()
        return

