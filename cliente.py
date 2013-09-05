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
    tabuleiro=[]
    def Movimenta(self,x):
        print "movimentou: %d" % x
        # cima
        if x == 1:
            pass
            #posicao = 
        
        # baixo
        elif x == 2:
            pass
            #posicao = ((posicao + 3) % 9)
        
        # direita
        elif x == 3:
            pass
            #posicao = 
        
        #esquerda
        elif x == 4:
            pass
            #posicao = 
        
        else:
            print "movimentação errada"

        print self.posicao

def le():
    tab = Tabuleiro()
    c = ord(getch())
    if c == 27:
        c = ord(getch())
        c = ord(getch())
        if c == 65:
            print "cima"
            print ((7 + 3) % 9)
            tab.Movimenta(1)
        elif c == 67:
            print "direita"
            tab.Movimenta(3)
        elif c == 66:
            print "baixo"
            tab.Movimenta(2)
        elif c == 68:
            print "esquerda"
            tab.Movimenta(4)
    elif c == 3:
        print "CTRL + C"
	sys.exit()
    else:
	print "%d" % c

getch = _Getch()
def main(): 
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
        print "   |   |\n___|___|___\n   |   |\n___|___|___\n   |   |\n   |   |\n"
        print "Vai:"

        while (1):
            le()
    except KeyboardInterrupt:
        udp.sendto('-1', dest)
        udp.close()
        sys.exit()

if __name__ == '__main__': main()

