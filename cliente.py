#!/usr/bin/python
#coding=utf-8
import socket
import os
import sys
import contextlib
import termios

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

class Tabuleiro:
    posicao = 0
    tabuleiro=[0]*8

    def Movimenta(self,x):
        #print "movimentou: %d" % x
        # cima
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
        
        else:
            print "movimentação errada"

        return self.posicao


    def AddPosicao(self,posicao):
        self.tabuleiro = [0]*8
        return (self.tabuleiro).insert(posicao,1)


    def Imprime(self,tabuleiro=None):
        if tabuleiro:
            self.tabuleiro = tabuleiro

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


def le(tab,udp,dest):
    c = ord(getch())
    if c == 27:
        c = ord(getch())
        c = ord(getch())
        if c == 65:
            udp.sendto(str(1), dest)

        elif c == 67:
            udp.sendto(str(3), dest)

        elif c == 66:
            udp.sendto(str(2), dest)

        elif c == 68:
            udp.sendto(str(4), dest)

    elif c == 3:
        print "CTRL + C"
        sys.exit()
    elif c == 13:
        udp.sendto(str(13), dest)

    else:
        print "%d" % c


def main(): 
    tab = Tabuleiro()
    if len(sys.argv) < 3:
        print 'Uso correto: cliente <servidor> <porta>'
        sys.exit()

    # Definição dos parametros para a comunicação
    HOST = sys.argv[1]          # Endereco IP do Servidor
    PORT = int(sys.argv[2])     # Porta que o Servidor esta
    udp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest=(HOST, PORT)

    try:
        try:
            udp.sendto(str("10"), dest)
        except Exception as e:
            print e
            sys.exit()    

        msg, cliente = udp.recvfrom(1024)
        if msg == "11":
            joga = True
        elif msg == "12":
            joga = False
        print "Vai:"

        while (1):
            while joga:
                le(tab,udp,dest)
                os.system("clear")
                msg, cliente = udp.recvfrom(1024)
                if msg == "12":
                    joga = False
                    break
                msg = msg.split(" ")
                msg = [int(m) for m in msg]
                tab.Imprime(msg)

            while not joga:
                msg, cliente = udp.recvfrom(1024)
                os.system("clear")
                if msg == "11":
                    joga = True
                    break
                msg = msg.split(" ")
                msg = [int(m) for m in msg]
                tab.Imprime(msg)

    except KeyboardInterrupt:
        udp.sendto('-1', dest)
        udp.close()
        sys.exit()

if __name__ == '__main__': main()

