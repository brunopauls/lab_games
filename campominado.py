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
					self.TrataBomba(i, j)

	def Jogada(self, x, y):
		self.tabuleiro[x][y]=self.tabuleiro__[x][y]
		if self.tabuleiro__[x][y]==9:
			self.jogador_vez.bombas+=1
			return False
		return True

	def TrocaJogadores(self):
		if self.jogador_vez == self.jogador_1:
			self.jogador_vez = self.jogador_2
		else:
			self.jogador_vez = self.jogador_1


	def TrataBomba(self, linha, coluna):
		try:
			if self.tabuleiro__[linha-1][coluna-1] <> 9:
				self.tabuleiro__[linha-1][coluna-1]+=1
		except:
			pass
		
		try:
			if self.tabuleiro__[linha-1][coluna] <> 9:
				self.tabuleiro__[linha-1][coluna]+=1
		except:
			pass
		
		try:
			if self.tabuleiro__[linha-1][coluna+1] <> 9:
				self.tabuleiro__[linha-1][coluna+1]+=1
		except:
			pass
		
		try:
			if self.tabuleiro__[linha][coluna-1] <> 9:
				self.tabuleiro__[linha][coluna-1]+=1
		except:
			pass
		
		try:
			if self.tabuleiro__[linha][coluna+1] <> 9:
				self.tabuleiro__[linha][coluna+1]+=1
		except:
			pass
		
		try:
			if self.tabuleiro__[linha+1][coluna-1] <> 9:
				self.tabuleiro__[linha+1][coluna-1]+=1
		except:
			pass
		
		try:
			if self.tabuleiro__[linha+1][coluna] <> 9:
				self.tabuleiro__[linha+1][coluna]+=1
		except:
			pass

		try:
			if self.tabuleiro__[linha+1][coluna+1] <> 9:
				self.tabuleiro__[linha+1][coluna+1]+=1
		except:
			pass

	def ImprimeCampoVetor(self):
		print
		for i in range(0, len(self.tabuleiro)):
			if (i <> 0) and (i % 15 == 0):
				print
			sys.stdout.write(" %s " % str(self.tabuleiro[i]))
		print
		print

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