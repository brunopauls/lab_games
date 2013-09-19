#!/usr/bin/python
#coding=utf-8
import socket

class Jogador():
	def __init__(self, nome, dados):
		self.nome = nome
		self.dados = dados

class Servidor():
    def __init__(self, HOST, PORT):
        self.__PORT=PORT
        self.__HOST=HOST
        self.__socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((HOST, PORT))
        self.__salas={	'15001': 0,
						'15002': 0,
				        '15003': 0,
				        '15004': 0,
				        '15005': 0,
				        '15006': 0,
				        '15007': 0,
				        '15008': 0,
				        '15009': 0,
				        '15010': 0,
		}

    def EncerraConexao(self):
        self.__socket.close()

    def EnviaMensagem(self, mensagem, endereco):
        self.__socket.sendto(mensagem, endereco)

    def RecebeMensagem(self,):
        return self.__socket.recvfrom(1024)

    def RetornaPorta(self):
        return self.__PORT

    def RetornaHost(self):
        return self.__HOST

	def ConfereVazio(porta):
	    return self.salas[str(porta)] <> 0

	def TemVazio():
	    while (1):
	        for porta in self.salas:
	            if self.salas[porta]<>1:
	                return int(porta)


class Sala():
    def __init__(self, HOST, PORT):
        self.__socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM).bind((HOST, PORT))
        self.jogador_1=Jogador()
        self.jogador_2=Jogador()
