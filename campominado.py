#!/usr/bin/python
#coding=utf-8
import random
import sys

import servidor

class Jogador():
	bombas=0
	endereco=(0, 0)

	def __init__(self, nome):
		self.nome = nome

class Tabuleiro:
	tamanho=15
	bombas=21
	ganhador=0
	jogador_1=Jogador('Jogador 1')
	jogador_2=Jogador('Jogador 2')

	def __init__(self):
		self.tabuleiro__ = []
		self.tabuleiro = []
		self.jogador_vez=self.jogador_1

		for i in range(0,self.tamanho):
			vetor = [0]*self.tamanho
			vetor2 = [-1]*self.tamanho
			self.tabuleiro__.append(vetor)
			self.tabuleiro.append(vetor2)

	def TransformaMatriz(self, lista):
		nova_lista=[]
		lista_atual=[]
		for i in range(0, len(lista)):
			if (i%self.tamanho == 0) and (i>0):
				nova_lista.append(lista_atual)
				lista_atual=[]
			lista_atual.append(lista.pop(0))
		nova_lista.append(lista_atual)
		return nova_lista

	def InverteMatrizLista(self, lista):
		if isinstance(lista, list):
			if isinstance(lista[0], list):
				return sum(self.tabuleiro__, [])
			else:
				return self.TransformaMatriz(lista)
		return None

	def ColocaBombas(self):
		for bomba in sorted([x for x in random.sample(range(0, (self.tamanho*self.tamanho)), self.bombas)]):
			self.tabuleiro__[(bomba/self.tamanho)][(bomba%self.tamanho)] = 9

	def TrataBomba(self, linha, coluna):
		if not ((linha < 0 or linha >= self.tamanho) or (coluna < 0 or coluna >= self.tamanho)):
			if self.tabuleiro__[linha][coluna] <> 9:
				self.tabuleiro__[linha][coluna]+=1

	def ArrumaCampo(self):
		for i in range(0, self.tamanho):
			for j in range(0, self.tamanho):
				if self.tabuleiro__[i][j]==9:
					for k in range(-1, 2):
						for l in range(-1, 2):
							self.TrataBomba(i+k, j+l)

	def ChecaVazios(self, x, y):
		try:
			if (x < 0 or x >= self.tamanho) or (y < 0 or y >= self.tamanho):
				return
			if (self.tabuleiro__[x][y]==0) and (self.tabuleiro[x][y]<>0):
				self.tabuleiro[x][y]=0
			else:
				if (self.tabuleiro__[x][y]>0) and (self.tabuleiro__[x][y]<9):
					self.tabuleiro[x][y]=self.tabuleiro__[x][y]
				return
			self.ChecaVazios(x-1, y-1)
			self.ChecaVazios(x-1, y)
			self.ChecaVazios(x-1, y+1)
			self.ChecaVazios(x, y-1)
			self.ChecaVazios(x, y+1)
			self.ChecaVazios(x+1, y-1)
			self.ChecaVazios(x+1, y)
			self.ChecaVazios(x+1, y+1)
		except:
			return

	def AbreVazios(self, x, y):
		self.ChecaVazios(x, y)

	def Jogada(self, x, y):
		if self.tabuleiro[x][y]<>-1:
			return False
		if self.tabuleiro__[x][y]==0:
			self.AbreVazios(x, y)
		elif self.tabuleiro__[x][y]==9:
			self.tabuleiro[x][y]=self.tabuleiro__[x][y]
			self.jogador_vez.bombas+=1
			return False
		self.tabuleiro[x][y]=self.tabuleiro__[x][y]
		return True

	def TrocaJogadores(self):
		if self.jogador_vez == self.jogador_1:
			self.jogador_vez = self.jogador_2
		else:
			self.jogador_vez = self.jogador_1

	def ImprimeCampoRevelado(self):
		print
		for vetor in self.tabuleiro__:
			print vetor
		print

	def ImprimeCampoNaoRevelado(self):
		print '-----------------------------------------------'
		for vetor in self.tabuleiro:
			sys.stdout.write('|')
			for elemento in vetor:
				string = str(elemento) if elemento<>-1 else ' '
				sys.stdout.write(" %s " % string)
			print '|'
		print '-----------------------------------------------'

def main():
	campo = Tabuleiro()
	campo.ColocaBombas()
	campo.ArrumaCampo()
	campo.ImprimeCampoRevelado()
	campo.ImprimeCampoNaoRevelado()

	while(1):
		print '%s (Bombas: %s)' % (campo.jogador_vez.nome, str(campo.jogador_vez.bombas))
		sys.stdout.write('Linha [0..14]: ')
		x = raw_input()
		sys.stdout.write('Coluna [0..14]: ')
		y = raw_input()
		troca = campo.Jogada(int(x), int(y))
		if troca:
			campo.TrocaJogadores()
		campo.ImprimeCampoRevelado()
		campo.ImprimeCampoNaoRevelado()

if __name__ == '__main__': main()