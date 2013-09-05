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

    def Imprime(self):
        for x in xrange(0,3):
            for y in xrange(0,3):
                #print "comparando posicao %d com 1" % ((x*3)+y)
                if self.tabuleiro[(x*3)+y] == 1:
                    sys.stdout.write("_X|")
                else:
                    sys.stdout.write("__|")
            print


def le(tab,udp,dest):

    c = ord(getch())
    if c == 27:
        c = ord(getch())
        c = ord(getch())
        if c == 65:
            #print "cima"
            udp.sendto(str(1), dest)
            tab.Movimenta(1)
        elif c == 67:
            #print "direita"
            udp.sendto(str(3), dest)
            tab.Movimenta(3)
        elif c == 66:
            #print "baixo"
            udp.sendto(str(2), dest)
            tab.Movimenta(2)
        elif c == 68:
            #print "esquerda"
            udp.sendto(str(4), dest)
            tab.Movimenta(4)
    elif c == 3:
        print "CTRL + C"
        sys.exit()
    elif c == 13:
        print "enviando posicao: %d" % tab.posicao
    else:
        print "%d" % c


getch = _Getch()


def main(): 
    tab = Tabuleiro()
    #getch = _GetchUnix()


    if len(sys.argv) < 3:
        print 'Uso correto: cliente <servidor> <porta>'

        sys.exit()

    # Definição dos parametros para a comunicação
    HOST = sys.argv[1]          # Endereco IP do Servidor
    PORT = int(sys.argv[2])     # Porta que o Servidor esta
    udp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest=(HOST, PORT)

    msg = "teste"
    try:
        try:
            udp.sendto(str(1), dest)

        except Exception as e:

            print e
            sys.exit()    
    

        true = True
        print "Vai:"

        while (1):
            le(tab,udp,dest)
            os.system("clear")
            
            #tab.Imprime()


    except KeyboardInterrupt:

        udp.sendto('-1', dest)
        udp.close()
        sys.exit()

if __name__ == '__main__': main()

