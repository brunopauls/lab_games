#!/usr/bin/python
#coding=utf-8
import socket
import sys
import os

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
            print "Movimentação errada"

        return self.posicao

    def Zera(self,posicao):
        self.tabuleiro = [0]*8
        return (self.tabuleiro).insert(posicao,1)

    def Imprime(self):
        for x in xrange(0,3):
            for y in xrange(0,3):
                if self.tabuleiro[(x*3)+y] == 1:
                    sys.stdout.write("_X|")
                else:
                    sys.stdout.write("__|")
            print

def main():
    if len(sys.argv) < 2:
        print 'Uso correto: servidor <porta>'
        sys.exit()
    
    HOST=''                
    PORT=int(sys.argv[1])
    udp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    orig=(HOST, PORT)
    udp.bind(orig)
    try:
        campo = Tabuleiro()
        while(1):
            msg, cliente = udp.recvfrom(1024)
            os.system('clear')
            campo.Movimenta(int(msg))
            campo.Zera(campo.posicao)
            campo.Imprime()
            msg = ' '.join(str(e) for e in campo.tabuleiro)
            udp.sendto(msg, cliente)

    except KeyboardInterrupt:
        udp.close()
        sys.exit()
   
if __name__ == '__main__': main()