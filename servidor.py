#!/usr/bin/python
#coding=utf-8
import socket
import sys
import os

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
            if self.ChecaVitoria() <> 0:
                self.ganhador = True
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
        return self.ChecaDiagonais()
        
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



def main():
    """
    if len(sys.argv) < 2:
        print 'Uso correto: servidor <porta>'
        sys.exit()
    """
    HOST=''
    PORT=15000
    udp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    orig=(HOST, PORT)
    udp.bind(orig)
    doisJogadores=False
    try:
        while(1):
            print 'Aguardando jogador 1...'
            while(1):
                msg, cliente = udp.recvfrom(1024)
                print 'Jogandor 1: ', cliente, msg
                if msg == "10":
                    jogador_1 = cliente
                    udp.sendto('14', jogador_1)
                    break
            
            print 'Aguardando jogador 2...'
            while(1):
                msg, cliente = udp.recvfrom(1024)
                print 'Jogandor 2: ', cliente, msg
                if msg == "10":
                    if not cliente == jogador_1:
                        jogador_2 = cliente
                        udp.sendto('14', jogador_2)
                        break

            PORT += 1
            if PORT > 15003:
                print 'Acabou espaço na memoria! :-)'
                udp.close()
                sys.exit()

            pid = os.fork()
            if (pid == 0):
                udp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                orig=(HOST, PORT)
                udp.bind(orig)

                campo = Tabuleiro(jogador_1, jogador_2)
                #Envia as mensagens de aviso
                campo.EnviaJogadorVez(udp)
                print 'Aguardando o inicio da partida...'

                while(1):
                    msg, cliente = udp.recvfrom(1024)
                    if campo.jogador_vez == cliente:
                        troca = campo.Movimenta(int(msg))
                        if campo.ganhador <> 0:
                            campo.EnviaVitoria(udp)
                            udp.close()
                            sys.exit()
                        else:
                            campo.EnviaTabuleiro(udp, campo.jogador_espera)
                            if not troca:
                                campo.EnviaTabuleiro(udp, campo.jogador_vez)
                            else:
                                campo.TrocaJogadores()
                                campo.EnviaJogadorVez(udp)


    except KeyboardInterrupt:
        udp.close()
        sys.exit()
   
if __name__ == '__main__': main()