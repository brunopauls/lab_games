#!/usr/bin/python
#coding=utf-8

import random
import sys

class Tabuleiro:
	tabuleiro=[0]*225
	bombas=[0]*21
	ganhador=0

	def __init__(self):
		self.__tabuleiro = []
		for i in range(0,15):
			vetor=[0]*15
			self.__tabuleiro.append(vetor)

	def CriaBombas(self):
		self.bombas = sorted([x for x in random.sample(range(0, len(self.tabuleiro)), len(self.bombas))])

	def ColocaBombas(self):
		for bomba in self.bombas:
			self.tabuleiro[bomba] = 9
		
		contador=0
		for i in range(0, 15):
			for j in range(0,15):
				self.__tabuleiro[i][j]=self.tabuleiro[contador]
				contador+=1

	def ArrumaCampo(self):
		for i in range(0, 15):
			for j in range(0, 15):
				if self.__tabuleiro[i][j]==9:
					self.TrataBomba(i, j)

	def TrataBomba(self, linha, coluna):
		try:
			if self.__tabuleiro[linha-1][coluna-1] <> 9:
				self.__tabuleiro[linha-1][coluna-1]+=1
		except:
			pass
		
		try:
			if self.__tabuleiro[linha-1][coluna] <> 9:
				self.__tabuleiro[linha-1][coluna]+=1
		except:
			pass
		
		try:
			if self.__tabuleiro[linha-1][coluna+1] <> 9:
				self.__tabuleiro[linha-1][coluna+1]+=1
		except:
			pass
		
		try:
			if self.__tabuleiro[linha][coluna-1] <> 9:
				self.__tabuleiro[linha][coluna-1]+=1
		except:
			pass
		
		try:
			if self.__tabuleiro[linha][coluna+1] <> 9:
				self.__tabuleiro[linha][coluna+1]+=1
		except:
			pass
		
		try:
			if self.__tabuleiro[linha+1][coluna-1] <> 9:
				self.__tabuleiro[linha+1][coluna-1]+=1
		except:
			pass
		
		try:
			if self.__tabuleiro[linha+1][coluna] <> 9:
				self.__tabuleiro[linha+1][coluna]+=1
		except:
			pass

		try:
			if self.__tabuleiro[linha+1][coluna+1] <> 9:
				self.__tabuleiro[linha+1][coluna+1]+=1
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

	def ImprimeCampo(self):
		print
		for vetor in self.__tabuleiro:
			print vetor
		print


def main():
	campo = Tabuleiro()
	campo.CriaBombas()
	campo.ColocaBombas()
	campo.ArrumaCampo()
	campo.ImprimeCampo()

if __name__ == '__main__': main()