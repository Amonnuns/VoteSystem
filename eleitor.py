# -*- Coding: UTF-8 -*-
#coding: utf-8
import socket
import json

HEADER = 256
PORT = #Porta do servidor que vc vai acessar
SERVER = # Ip do servidor que vc vai acessar
ADDR = (SERVER,PORT)

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect(ADDR);

def send_length(msg):
    msg_length = len(msg)
    send_length = str(msg_length).encode('utf-8')
    if len(send_length) < HEADER:
        send_length+= b' ' * (HEADER - len(send_length))
    server.send(send_length)

def eleitor():
    msg='Eleitor'
    send_length(msg)
    msg=msg.encode('utf-8')
    server.send(msg)

def lista():
    msg_length = server.recv(HEADER).decode("utf-8")
    if msg_length:
        send_length = int(msg_length)
        list = server.recv(send_length).decode("utf-8")
        candidates = json.loads(list)
        for x,info in candidates.items():
            print(f"{info['name']}, número: {info['number']} ")

def votar(name,cpf,number):
    msg = json.dumps({'name':name, 'cpf':cpf,'vote':number})
    msg = msg.encode('utf-8')
    send_length(msg)
    server.send(msg)
    msg_length = server.recv(HEADER).decode("utf-8")
    if msg_length:
        length = int(msg_length)
        msg = server.recv(length).decode("utf-8")
        print(str.upper(msg))


eleitor()
print("-------------------- Olá, bem-vindo ao nosso sistema de votação --------------------\n")
print("Escolha um Candidato para votar na nossa lista:\n")
lista()
print(" ")
print("Para votar insira as seguintes informações:")
nome = input("Digite seu nome:")
cpf = input("Digite seu cpf:")
numero = input("Digite o número do seu convidado:")
votar(nome, cpf, numero)
