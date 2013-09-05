#!/usr/bin/python
#coding=utf-8
import socket
import sys

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
        while(1):
            msg, cliente = udp.recvfrom(1024)
            print cliente, ': ', msg
    except KeyboardInterrupt:
        udp.close()
        sys.exit()
   
if __name__ == '__main__': main()