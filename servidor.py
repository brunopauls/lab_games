#!/usr/bin/python
#coding=utf-8
import socket
import thread
import sys
import os

class UDPSocket:
    def __init__(self, HOST, PORT):
        self.__PORT=PORT
        self.__HOST=HOST
        self.__socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((HOST, PORT))

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

class Tabuleiro:
    posicao = 0
    ganhador = 0
    tabuleiro=[0]*9
    __tabuleiro=[0]*9

    def __init__(self, jogador1, jogador2):
        self.jogador_1 = self.jogador_vez = jogador1
        self.jogador_2 = self.jogador_espera = jogador2

    def TrocaJogadores(self):
        aux=self.jogador_vez
        self.jogador_vez = self.jogador_espera
        self.jogador_espera=aux

    def EnviaVitoria(self, socket):
        socket.sendto('21', self.jogador_vez)
        socket.sendto('22', self.jogador_espera)

    def EnviaEmpate(self, socket):
        socket.sendto('23', self.jogador_vez)
        socket.sendto('23', self.jogador_espera)

    def EnviaJogadorVez(self, socket):
        socket.sendto('11', self.jogador_vez)
        socket.sendto('12', self.jogador_espera)

    def EnviaTabuleiro(self, socket, jogador):
        socket.sendto(self.PegaTabuleiro(), jogador)

    def Movimenta(self,x):
        # cima
        aux=0
        if x == 1:  
            self.posicao = ((self.posicao - 3) % 9)
        # baixo
        elif x == 2:
            self.posicao = ((self.posicao + 3) % 9)
        # direita
        elif x == 3:
            if ((self.posicao + 1) % 3) == 0:
                self.posicao -= 2 
            else:
                self.posicao += 1
        #esquerda
        elif x == 4:
            if ((self.posicao % 3) == 0):
                self.posicao += 2 
            else:
                self.posicao -= 1
        elif x == 13:
            return self.ValidaJogada()
        else:
            print "Movimentação errada"
        return self.ArrumaPosicao()

    def ArrumaPosicao(self):
        if self.jogador_vez == self.jogador_1:
            X_O=3
        else:
            X_O=4
        self.tabuleiro = [x for x in self.__tabuleiro]
        self.tabuleiro[self.posicao] = X_O
        return False

    def ValidaJogada(self):
        if not self.__tabuleiro[self.posicao] <> 0:
            self.SalvaTabuleiro()
            vitoria = self.ChecaVitoria()
            if vitoria <> 0:
                self.ganhador = vitoria
            return True
        else:
            return False

    def SalvaTabuleiro(self):
        if self.jogador_vez == self.jogador_1:
            self.tabuleiro[self.posicao] = 1
        else:
            self.tabuleiro[self.posicao] = 2

        self.__tabuleiro = self.tabuleiro

    def PegaTabuleiro(self):
        return ' '.join(str(e) for e in self.tabuleiro)

    #funcao q retorna 0 se ngm ganhou ainda, 1 se X ganhou e 2 se O ganhou
    def ChecaVitoria(self):
        z=0
        for x in xrange(3):
            z+=self.ChecaLinha(x)
            if(z <> 0):
                return z
            z=self.ChecaColuna(x)
            if(z <> 0):
                return z
        z=self.ChecaDiagonais()
        if (z<>0):
            return z
        return self.ChecaEmpate()


    def ChecaLinha(self,linha):
        linha *= 3
        if(self.tabuleiro[linha] == self.tabuleiro[linha + 1]):
            if(self.tabuleiro[linha] == self.tabuleiro[linha + 2] ):
                return self.tabuleiro[linha]
        return 0

    def ChecaColuna(self,coluna):
        if(self.tabuleiro[coluna] == self.tabuleiro[coluna + 3]):
            if(self.tabuleiro[coluna] == self.tabuleiro[coluna + 6]):
                return self.tabuleiro[coluna]
        return 0

    def ChecaDiagonais(self):
        if(self.tabuleiro[0] == self.tabuleiro[4]):
            if(self.tabuleiro[0] == self.tabuleiro[8]):
                return self.tabuleiro[4]
        elif(self.tabuleiro[2] == self.tabuleiro[4]):
            if(self.tabuleiro[2] == self.tabuleiro[6]):
                return self.tabuleiro[4]
        return 0

    def ChecaEmpate(self):
        for pos in self.__tabuleiro:
            if pos == 0:
                return 0
        return 3

def JogoDaVelha(host, porta, jogador_1, jogador_2):
    salas[str(porta)]=1
    #Cria um socket para a conexao
    udp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind((host, porta))

    campo = Tabuleiro(jogador_1, jogador_2)
    #Envia as mensagens de aviso
    campo.EnviaJogadorVez(udp)

    while(1):
        msg, cliente = udp.recvfrom(1024)
        if campo.jogador_vez == cliente:
            troca = campo.Movimenta(int(msg))
            if campo.ganhador <> 0:
                if campo.ganhador == 3:
                    campo.EnviaEmpate(udp)
                else:
                    campo.EnviaVitoria(udp)
                salas[str(porta)]=0
                udp.close()
                sys.exit()
            else:
                campo.EnviaTabuleiro(udp, campo.jogador_espera)
                if not troca:
                    campo.EnviaTabuleiro(udp, campo.jogador_vez)
                else:
                    campo.TrocaJogadores()
                    campo.EnviaJogadorVez(udp)

def ConfereVazio(porta):
    return salas[str(porta)] <> 0

def TemVazio():
    while (1):
        for porta in salas:
            if salas[porta]<>1:
                return int(porta)

salas={ '15001': 0,
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

def main():
    socket = UDPSocket('', 15000)
    PORTA_disponivel = socket.RetornaPorta()
    HOST = socket.RetornaHost()

    try:
        while(1):
            print 'Aguardando jogador 1...'
            while(1):
                mensagem, jogador_1 = socket.RecebeMensagem()
                if mensagem == "10":
                    socket.EnviaMensagem('14', jogador_1)
                    break
            print 'Aguardando jogador 2...'
            while(1):
                mensagem, jogador_2 = socket.RecebeMensagem()
                if mensagem == "10":
                    if not jogador_2 == jogador_1:
                        socket.EnviaMensagem('14', jogador_2)
                        break
            PORTA_disponivel += 1
            if PORTA_disponivel > socket.RetornaPorta()+10 or ConfereVazio(PORTA_disponivel):
                PORTA_disponivel = TemVazio()
            thread.start_new_thread(JogoDaVelha, (HOST, PORTA_disponivel, jogador_1, jogador_2))
    except KeyboardInterrupt:
        socket.EncerraConexao()
        sys.exit()
   
if __name__ == '__main__': main()