# CS 325
# Project2, algorithms for making change with coin denominations

#SOURCES:
#   For the changedp() function code:
#   http://interactivepython.org/runestone/static/pythonds/Recursion/DynamicProgramming.html

import sys      #for command line args
import time     #for the timer
import os       #for splitting off file extensions

# Constants

# Functions
def usage():
	print "python project2.py <input file>"

def changegreedy(denomArray, value):	
	coinCountArray = []
	for coin in reversed(denomArray):
		coinCount = 0
		while value >= coin:
			coinCount += 1
			value -= coin
		coinCountArray.insert(0, coinCount)
	numCoins = 0
	for coinCount in coinCountArray:
		numCoins += coinCount
	return {'COINS':coinCountArray, 'NUMCOINS':numCoins}

def changedp(coinValueList,change,minCoins,coinsUsed):
	for cents in range(change+1):
		coinCount = cents
		newCoin = 1
		for j in [c for c in coinValueList if c <= cents]:
			if minCoins[cents-j] + 1 < coinCount:
				coinCount = minCoins[cents-j]+1
				newCoin = j
		minCoins[cents] = coinCount
		coinsUsed[cents] = newCoin
	return minCoins[change]

def usedCoins(coinsUsed,change,array):
	coin = change
	usedArray = [0] * len(array)
	while coin > 0:
		thisCoin = coinsUsed[coin]
		for y in range(len(array)):
			if thisCoin == array[y]:
				usedArray[y] = usedArray[y] + 1
		#print(thisCoin)
		coin = coin - thisCoin
	return usedArray
	
def main():
	if (len(sys.argv) < 2):
		usage()
		sys.exit()
	# open files
	inFile = open(sys.argv[1], 'r')
	inFileNoExtension = os.path.splitext(sys.argv[1])[0]
	outFile = open(inFileNoExtension + 'change.txt', 'a+')
	#output file header indicating greedy algorithm data
	outFile.write("changegreedy\n")
	# read file, create input array
	denomArray = []
	value = -1
	#Greedy loop
	for line in inFile:
		if line != '\n':
			# determine if line is input array or value
			if line[0] == "[":
				#input array
				newData = line.replace("[", "")
				newData = newData.replace("]", "")
				denomArray = [int(el) for el in newData.split(',')]
			else:
				#value
				value = int(line)
				coinsUsed = [0] * (value+1)
				coinCount = [0] * (value+1)
			if denomArray != [] and value != -1:
				#run greedy algorithm
				coinResults = changegreedy(denomArray, value)
				outFile.write(str(coinResults['COINS']) + "\n")
				outFile.write(str(coinResults['NUMCOINS']) + "\n")
				denomArray = []
				value = -1
	#reset loop vars
	denomArray = []
	value = -1
	inFile.seek(0)
	#output file header indicating greedy algorithm data
	outFile.write("changedp\n")
	#DP loop
	for line in inFile:
		if line != '\n':
			# determine if line is input array or value
			if line[0] == "[":
				#input array
				newData = line.replace("[", "")
				newData = newData.replace("]", "")
				denomArray = [int(el) for el in newData.split(',')]
			else:
				#value
				value = int(line)
				coinsUsed = [0] * (value+1)
				coinCount = [0] * (value+1)
			if denomArray != [] and value != -1:
				#run greedy algorithm
				dpResult = changedp(denomArray, value, coinCount, coinsUsed)
				usedCoinsArray = usedCoins(coinsUsed, value, denomArray)
				outFile.write(str(usedCoinsArray) + "\n")
				outFile.write(str(dpResult) + "\n")
				denomArray = []
				value = -1
	inFile.close()
	outFile.close()
if __name__ == '__main__': main()