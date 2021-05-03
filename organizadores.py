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

def organizador():
    msg='Organizador'
    send_msg(msg)

def receive_msg():
    msg_length = server.recv(HEADER).decode('utf-8')
    if msg_length:
        msg_length = int(msg_length)
        msg = server.recv(msg_length).decode('utf-8')
        return msg    

def send_msg(msg):
    msg_length = len(msg.encode('utf-8'))
    send_length = str(msg_length).encode('utf-8')
    if len(send_length) < HEADER:
        send_length+= b' ' * (HEADER - len(send_length))
    server.send(send_length)
    msg = msg.encode('utf-8')
    server.send(msg)
    

def all_candidatos():
    op = "All"
    send_msg(op)
    msg = receive_msg()
    lista = json.loads(msg)
    for number, info in lista.items(): #número:{'name':'Franco', 'votes':0}
        print(f"Candidato {info['name']} de número {number} possui {info['votes']} votos")
    print(" ")

def candidato(number):
    op = "One"
    send_msg(op)
    send_msg(number)
    msg = receive_msg()
    while msg == "Inválido":
        number = input("Digite novamente o número do candidato:")
        send_msg(number)
        msg = receive_msg()
    candidato = json.loads(msg)
    for number, info in candidato.items():
        print(f"\nCandidato {info['name']} de número {number} possui {info['votes']} votos\n")

def close():
    op="Close"
    send_msg(op)
    msg = receive_msg()
    print(msg)


organizador()
print("-------------------- Olá, bem-vindo ao nosso sistema de contagem de votos --------------------")
while True:
    print(''' Digite uma das seguintes opções:
1 - Fazer contagem de votos de um candidato
2 - Fazer contagem de votos de todos candidatos
3 - Sair do programa          
    ''')
    op = int(input())
    if(op == 1):
        number = input("Digite o número do candidato:")
        candidato(number)
    if(op == 2):
        all_candidatos()
    if(op == 3):
        close()
        break
    






