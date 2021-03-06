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


class Cores:
    HEADER = '\033[95m'
    AZUL = '\033[94m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'

    FAZUL = '\033[44m'


    ENDC = '\033[0m'

    @classmethod
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''



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
        # X estático
        if(self.tabuleiro[pos] == 1):
            sys.stdout.write("X")
        # 0 estático
        elif(self.tabuleiro[pos] == 2):
            sys.stdout.write("O")
        # X movimentando
        elif(self.tabuleiro[pos] == 3):
            sys.stdout.write("%sX%s" % (Cores.VERMELHO,Cores.ENDC))
        # 0 movimentando
        elif(self.tabuleiro[pos] == 4):
            sys.stdout.write("%sO%s" % (Cores.VERDE,Cores.ENDC))
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
        print Cores.VERMELHO + "CTRL + C" + Cores.ENDC
        Cores.disable()
        sys.exit()
    elif c == 13:
        udp.sendto(str(13), dest)

    else:
        print "%d" % c

def ImprimeMenuNovoJogo(tab,tabuleiro,opcao):
    os.system("clear")
    tab.Imprime(tabuleiro)
    if opcao == 1:
        print "\n\n"
        print Cores.FAZUL + "JOGAR NOVAMENTE" + Cores.ENDC
        print "SAIR"
    elif opcao == 2:
        print "\n\n"
        print "JOGAR NOVAMENTE"
        print Cores.FAZUL + "SAIR" + Cores.ENDC

def Opcao(tab,tabuleiro):
    opcao = 1
    ImprimeMenuNovoJogo(tab,tabuleiro,opcao)

    while(1):
        c = ord(getch())
        if c == 27:
            c = ord(getch())
            c = ord(getch())
            if c == 65:
                opcao = 1
                ImprimeMenuNovoJogo(tab,tabuleiro,opcao)
            elif c == 66:
                opcao = 2
                ImprimeMenuNovoJogo(tab,tabuleiro,opcao)
        elif c == 13:
            if opcao == 1:
                main()
            elif opcao == 2:
                sys.exit()

def main():
    tab = Tabuleiro()
    if len(sys.argv) < 2:
        print 'Uso correto: cliente <servidor>'
        sys.exit()

    # Definição dos parametros para a comunicação
    HOST = sys.argv[1] # Endereco IP do Servidor
    PORT = 15000       # Porta que o Servidor esta
    udp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest=(HOST, PORT)

    try:
        udp.settimeout(1);
        try:
            udp.sendto(str("10"), dest)
        except Exception as e:
            print e
            sys.exit()    

        timeout = True
        while(timeout):
            try:
                timeout = False
                msg, cliente = udp.recvfrom(1024)
                udp.settimeout(None)
            except Exception as e:
                print e
                udp.sendto(str("10"), dest)
                timeout = True
            else:
                print "Desabilitou timeout"
                udp.settimeout(None)

        print cliente

        if msg == "14":
            print "Esperando inicio do jogo"
            msg, cliente = udp.recvfrom(1024)


        print cliente

        dest=cliente
        if msg == "11":
            joga = True
        elif msg == "12":
            joga = False

        while (1):
            # Jogador Ativo:
            while joga:
                print Cores.VERDE + "Sua vez!" + Cores.ENDC + str(dest)
                le(tab,udp,dest)
                
                msg, cliente = udp.recvfrom(1024)
                if msg == "12":
                    joga = False
                    break
                elif msg == "21":
                    print Cores.AZUL + "GANHEEEMO!" + Cores.ENDC
                    Opcao(tab,ultimo)
                elif msg == "23":
                    print Cores.AMARELO + "EMPATE" + Cores.ENDC
                    Opcao(tab,ultimo)
                else:
                    os.system("clear")
                msg = msg.split(" ")
                msg = [int(m) for m in msg]
                tab.Imprime(msg)
                ultimo = [int(m) for m in msg]

            # Jogador em espera:
            while not joga:
                print Cores.AMARELO + "Espere" + Cores.ENDC + str(dest)
                msg, cliente = udp.recvfrom(1024)
                print msg
                if msg == "11":
                    joga = True
                    break
                elif msg == "22":
                    print Cores.VERMELHO + "PERDEU!" + Cores.ENDC
                    Opcao(tab,ultimo)
                elif msg == "23":
                    print Cores.AMARELO + "EMPATE" + Cores.ENDC
                    Opcao(tab,ultimo)
                else:
                    os.system("clear")
                msg = msg.split(" ")
                msg = [int(m) for m in msg]
                tab.Imprime(msg)
                ultimo = [int(m) for m in msg]

    except KeyboardInterrupt:
        # Mandar msg de fim pro servidor!
        print Cores.VERMELHO + "CTRL + C" + Cores.ENDC
        Cores.disable()
        sys.exit()

if __name__ == '__main__': main()



