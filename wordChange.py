#!/usr/bin/py 

import sys
import Queue

# example call: python wordChange.py adobe allay

# important data structures:
# acceptedWords: the dictionary (python hash table) of legitimate 5 letter words
# attemptedWords: the dictionary of words that have been put into the queue, 
# 	ensures that duplicates are not input, thereby reducing time and space usage
# wordQueue: FIFO queue of words. this enables as a breadth first search through 
# 	the word tree, so to speak
# histQueue: the associated history of past words that lead to the current word

#	initializes the data structures and calls BFS
def main():
	(start, fin) = readCommandLine()
	if start == fin:
		print start
		exit(0)
	acceptedWords = readFile(start, fin)
	attemptedWords = {}
	wordQueue = Queue.Queue()
	histQueue = Queue.Queue()
	wordQueue.put(start)
	histQueue.put([])
	attemptedWords[start] = 1
	BFS(fin, wordQueue, histQueue, acceptedWords, attemptedWords)


def BFS(fin, wordQueue, histQueue, acceptedWords, attemptedWords):
	while not wordQueue.empty():
		word = wordQueue.get()
		hist = histQueue.get()
		for x in range(26):
		 	char = chr(ord('A') + x)
		 	for y in range(5):
		 		toAdd = getToAdd(char, y, word)
				isFinalWord(toAdd, word, hist, fin)
		 		if toAdd in acceptedWords and toAdd not in attemptedWords:
		 			attemptedWords[toAdd] = 1
		 			histQueue.put(hist + [word])
		 			wordQueue.put(toAdd)
	print "sadly, there is no transition from the starting word to " + fin

def getToAdd(char, index, word):
	toAdd = word[0:index]
	toAdd += char
	toAdd += word[index+1:5]
	return toAdd

# tests if the new word is the final word, 
# and if so prints the history and the word
def isFinalWord(toAdd, word, hist, fin):
	if toAdd == fin:
		for histWord in hist:
			print histWord
		print word
		print toAdd
		exit(0)

def readCommandLine():
	args = sys.argv
	if len(args) < 3:
		print "too few arguments, must pass start and final string in command line"
		exit(0)
	start = sys.argv[1].upper()
	fin = sys.argv[2].upper()
	if len(start) != 5 or len(fin) != 5:
		print "both strings must be 5 characters in length"
		exit(0)
	return (start, fin)


def readFile(start, fin):	
	acceptedWords = {}
	f = open('acceptedWords.txt', 'r')
	word = ""
	for line in f:
		for char in line:
			if char != ' ' and char != '\n':
				word += char 
			else:
				# test to ensure the wordlist contains only 5 letter words
				if len(word) != 5:
					print word
				# adds the word to the dictionary
				acceptedWords[word] = 1;
				word = ""
	if start not in acceptedWords or fin not in acceptedWords:
		print "starting and final word must be validated 5 letter words"
		exit(0)
	return acceptedWords


if __name__ == "__main__":
	main();