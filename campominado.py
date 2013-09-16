#!/usr/bin/python
#coding=utf-8

import random
import sys

class Tabuleiro:
	bombas=[0]*21
	ganhador=0

	def __init__(self):
		self.tabuleiro__ = []
		self.tabuleiro = []

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

if __name__ == '__main__': main()