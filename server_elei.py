# -*- Coding: UTF-8 -*-
#coding: utf-8
import socket
import threading
import json

HEADER = 256
PORT = #Porta que vc vai utilizar
SERVER = # Ip do servidor que vc vai utilizar
ADDR = (SERVER,PORT)


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

with open('candidatos.json') as json_file:
    candidates = json.load(json_file)    
    #estrutura dos candidatos {número:{'name':'Franco', 'votes':0}}

eleitores = {} 

def send_msg(msg,conn):
    msg_length = len(msg.encode('utf-8'))
    send_length = str(msg_length).encode('utf-8')
    if len(send_length) < HEADER:
        send_length+= b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    msg = msg.encode('utf-8')
    conn.send(msg)

def send_candidate(conn, candidatos, number):
    msg = {}
    try:
        msg[number]={'name': candidatos[number]['name'],'votes': candidatos[number]['votes']}
        msg = json.dumps(msg)
        send_msg(msg, conn)
    except:
        msg = "Inválido"
        send_msg(msg, conn)
        msg = receive_msg(conn)
        send_candidate(conn, candidatos, msg)



def send_candidates_list(conn, candidatos, option):
    list_candidatos = {}
    i=0
    if option == "Eleitor":
        for number, info in candidatos.items():
            i+=1
            list_candidatos[i]={'name':info['name'],'number':number}
            msg = json.dumps(list_candidatos)
    if option == "Organizador":
        msg = json.dumps(candidatos)
    
    send_msg(msg,conn)
    

def receive_msg(conn):
    msg_length = conn.recv(HEADER).decode('utf-8')
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode('utf-8')
        return msg    


def receive_voting(conn, eleitores, candidatos):
        msg = receive_msg(conn)
        voto = json.loads(msg)
        try:
            eleitores[voto['cpf']]
        except:
            try:
                candidatos[voto['vote']]['votes']+=1
                eleitores[voto['cpf']] = {'name':voto['name'],'candidato':candidatos[voto['vote']]['name']}  
                msg = f"Você votou em {candidatos[voto['vote']]['name']}"
                send_msg(msg,conn)
            except KeyError:
                msg="Número de Candidato Inválido"
                send_msg(msg, conn)
        else:
            msg="Você já efetuou sua votação"
            send_msg(msg, conn)


def handle_client(conn, addr, eleitores, candidatos):
    
    msg = receive_msg(conn)
    print(f"[Nova Conexão] {addr} conectado.")
    if msg == "Eleitor":
        send_candidates_list(conn, candidatos,msg)
        receive_voting(conn, eleitores, candidatos)
    if msg == "Organizador":
        while True:
            option = receive_msg(conn)
            if option == "All":
                send_candidates_list(conn, candidatos, msg)
            if option == "One":
                msg = receive_msg(conn)
                send_candidate(conn, candidatos, msg)
            if option == "Close":
                break
    
    
    print(f"[ACTIVE CONECTIONS]{threading.activeCount() - 2}")
    with open('eleitores.json', 'w') as outfile:
        json.dump(eleitores, outfile)
    conn.close()

def start(eleitores, candidatos):
    #estrutura de eleitores {cpf:{'name':'Franco', 'candidato':'Teotônio'}} 
    server.listen()
    print(f"[Escutando] o servidor está escutando em {SERVER}")
    while True:
        conn, addr = server.accept()
        with open('eleitores.json', 'r') as outfile:
            eleitores=json.load(outfile)
        thread = threading.Thread(target=handle_client, args=(conn, addr, eleitores, candidatos))
        thread.start()
        print(f"[Conexões ativas:]{threading.activeCount() - 1}")
        

print("[Iniciando] a eleição está iniciando....")
start(eleitores, candidates)

 