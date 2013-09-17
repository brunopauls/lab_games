#!/usr/bin/python
#coding=utf-8

import random
import sys
class Jogador():
	bombas=0
	endereco=(0, 0)


class Tabuleiro:
	bombas=[0]*21
	ganhador=0
	jogador_1=Jogador()
	jogador_2=Jogador()

	def __init__(self):
		self.tabuleiro__ = []
		self.tabuleiro = []
		self.jogador_vez=self.jogador_1

		for i in range(0,15):
			vetor = [0]*15
			vetor2 = [-1]*15
			self.tabuleiro__.append(vetor)
			self.tabuleiro.append(vetor2)

	def CriaBombas(self):
		self.bombas = sorted([x for x in random.sample(range(0, 225), 21)])

	def ColocaBombas(self):
		for bomba in self.bombas:
			self.tabuleiro__[(bomba/15)][(bomba%15)] = 9

	def ArrumaCampo(self):
		for i in range(0, 15):
			for j in range(0, 15):
				if self.tabuleiro__[i][j]==9:
					print 'ALO!'
					print i, j
					k=-1
					while (k <= 1):
						l=-1
						while (l <= 1):
							self.TrataBomba(i+k, j+l)
							l+=1
						k+=1
					print 'TCHAU!'

	def ChecaVazios(self, x, y):
		try:
			if (x < 0 or x > 14) or (y < 0 or y > 14):
				return
			if (self.tabuleiro__[x][y]==0) and (self.tabuleiro[x][y]<>0):
				self.tabuleiro[x][y]=0
			else:
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
		if self.tabuleiro__[x][y]==0:
			self.AbreVazios(x, y)
		elif self.tabuleiro__[x][y]==9:
			self.jogador_vez.bombas+=1
			return False
		self.tabuleiro[x][y]=self.tabuleiro__[x][y]
		return True

	def TrocaJogadores(self):
		if self.jogador_vez == self.jogador_1:
			self.jogador_vez = self.jogador_2
		else:
			self.jogador_vez = self.jogador_1


	def TrataBomba(self, linha, coluna):
		try:
			if not ((linha < 0 or linha > 14) or (coluna < 0 or coluna > 14)):
				if self.tabuleiro__[linha][coluna] <> 9:
					print linha, coluna
					self.tabuleiro__[linha][coluna]+=1
		except:
			pass

	def ImprimeCampoRevelado(self):
		print
		for vetor in self.tabuleiro__:
			print vetor
		print

	def ImprimeCampoNaoRevelado(self):
		print
		for vetor in self.tabuleiro:
			print vetor
		print


def main():
	campo = Tabuleiro()
	campo.CriaBombas()
	campo.ColocaBombas()
	campo.ArrumaCampo()
	campo.ImprimeCampoRevelado()
	campo.ImprimeCampoNaoRevelado()

	while(1):
		print vars(campo.jogador_vez)
		print 'Posicao 1'
		x = raw_input()
		print 'Posicao 2'
		y = raw_input()
		troca = campo.Jogada(int(x), int(y))
		if troca:
			campo.TrocaJogadores()
		campo.ImprimeCampoRevelado()
		campo.ImprimeCampoNaoRevelado()
	

if __name__ == '__main__': main()