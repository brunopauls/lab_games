#!/usr/bin/python
#coding=utf-8
import socket
import sys
import os

class Jogador:
    def __init__(self, dados):
        self.infos=dados

class Tabuleiro:
    posicao = 0
    tabuleiro=[0]*9
    __tabuleiro=[0]*9


    def __init__(self, jogador1=None, jogador2=None):
        self.jogador_1 = jogador1
        self.jogador_2 = jogador2

        self.jogador_vez = jogador1
        self.jogador_espera = jogador2

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
            if self.FazerJogada(): 
                return True
        else:
            print "Movimentação errada"
        return False

    def Jogada(self,posicao):
        if self.jogador_vez == self.jogador_1:
            X_O=1
        else:
            X_O=2
        self.tabuleiro = [x for x in self.__tabuleiro]
        self.tabuleiro[posicao] = X_O

    def FazerJogada(self):
        if not self.__tabuleiro[self.posicao] <> 0:
            self.SalvaTabuleiro()
            vitoria = self.ChecaVitoria()
            return True
        else:
            return False


    def SalvaTabuleiro(self):
        self.__tabuleiro = self.tabuleiro

    def Imprime(self):
        sys.stdout.write(" _________________ \n|     |     |     |\n|  ")
        self.ImprimeXouOouEspaco(0)
        sys.stdout.write("  |  ")
        self.ImprimeXouOouEspaco(1)
        sys.stdout.write("  |  ")
        self.ImprimeXouOouEspaco(2)
        sys.stdout.write("  |\n|_____|_____|_____|\n|     |     |     |\n|  ")
        self.ImprimeXouOouEspaco(3)
        sys.stdout.write("  |  ")
        self.ImprimeXouOouEspaco(4)
        sys.stdout.write("  |  ")
        self.ImprimeXouOouEspaco(5)
        sys.stdout.write("  |\n|_____|_____|_____|\n|     |     |     |\n|  ")
        self.ImprimeXouOouEspaco(6)
        sys.stdout.write("  |  ")
        self.ImprimeXouOouEspaco(7)
        sys.stdout.write("  |  ")
        self.ImprimeXouOouEspaco(8)
        sys.stdout.write("  |\n|_____|_____|_____|\n")

    def ImprimeXouOouEspaco(self,pos):
        if(self.tabuleiro[pos] == 1):
            sys.stdout.write("X")
        elif(self.tabuleiro[pos] == 2):
            sys.stdout.write("O")
        else:
            sys.stdout.write(" ")

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
    if len(sys.argv) < 2:
        print 'Uso correto: servidor <porta>'
        sys.exit()
    
    HOST=''                
    PORT=int(sys.argv[1])
    udp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    orig=(HOST, PORT)
    udp.bind(orig)
    doisJogadores=False
    try:
        
        while(not doisJogadores):
            print 'Aguardando jogador 1...'
            while(1):
                msg, cliente = udp.recvfrom(1024)
                if msg == "10":
                    j1 = Jogador(cliente)
                    break
            
            print 'Aguardando jogador 2...'
            while(1):
                msg, cliente = udp.recvfrom(1024)
                if msg == "10":
                    j2 = Jogador(cliente)
                    break
            
            doisJogadores=True
        

        campo = Tabuleiro(j1.infos, j2.infos)

        #Envia as mensagens de aviso
        udp.sendto('11', campo.jogador_vez)
        udp.sendto('12', campo.jogador_espera)

        print 'Aguardando o inicio da partida!'
        while(1):
            msg, cliente = udp.recvfrom(1024)
            if campo.jogador_vez == cliente:
                os.system('clear')
                troca = campo.Movimenta(int(msg))
                campo.Jogada(campo.posicao)
                campo.Imprime()
                msg = ' '.join(str(e) for e in campo.tabuleiro)
                if not troca:
                    udp.sendto(msg, campo.jogador_vez)
                udp.sendto(msg, campo.jogador_espera)
                if troca:
                    aux=campo.jogador_vez
                    campo.jogador_vez=campo.jogador_espera
                    campo.jogador_espera=aux
                    #Envia as mensagens de aviso
                    udp.sendto('12', campo.jogador_espera)
                    udp.sendto('11', campo.jogador_vez)
                    

    except KeyboardInterrupt:
        udp.close()
        sys.exit()
   
if __name__ == '__main__': main()