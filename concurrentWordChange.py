#!/usr/bin/py 

import sys
import Queue
import threading

# use of the two mutexes:
# mutex: used to ensure that threads put corresponding elements in histQueue 
# 	wordQueue. in other words, histQueue and wordQueue must have the the word
#  	and its history at the same index
# queueMutex: in python calling queue.get() blocks until there is an element in
# 	the queue. for threading, this can be bad as processes use an empty queue. 
# 	as a signal that there is no path to the desired 5 letter word. thus, we 
#  	use a mutex to ensure that we check that the queue is not empty and take the
# 	first element out of the queue in one solid operation

mutex = threading.Lock()
queueMutex = threading.Lock()

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
	threadNum = 4;
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

	# a somewhat hacky way to share a flag between threads. 
	# python integers are local, but arrays are passed by reference
	isFinished = [False, 0]
	threads = [threading.Thread(target = BFS, 
		args = (start, fin, wordQueue, histQueue, acceptedWords, attemptedWords, isFinished)) 
		for i in range(threadNum)]
	for thread in threads:
		thread.start()
	while True:
		if isFinished[0]:
			exit(0)
	# BFS(fin, wordQueue, histQueue, acceptedWords, attemptedWords)


def BFS(start, fin, wordQueue, histQueue, acceptedWords, attemptedWords, isFinished):
	loopCount = 0
	while True:
		if isFinished[0]:
			exit(0)
		queueMutex.acquire()
		if not wordQueue.empty():
			word = wordQueue.get()
			hist = histQueue.get()
		else:
			loopCount += 1
			if loopCount > 100:
				queueMutex.release()
				break
			else:
				word = start
				hist = []
		queueMutex.release()
		for x in range(26):
			char = chr(ord('A') + x)
			for y in range(5):
				toAdd = getToAdd(char, y, word)
				isFinalWord(toAdd, word, hist, fin, isFinished)
				if toAdd in acceptedWords and toAdd not in attemptedWords:
					attemptedWords[toAdd] = 1
					mutex.acquire()
					histQueue.put(hist + [word])
					wordQueue.put(toAdd)
					mutex.release()

	# adds one to the number of threads that have finished the queue
	isFinished[1] += 1
	if isFinished[1] == 4:
		isFinished[0] = True
		print "sadly, there is no transition from " + start + " to " + fin

def getToAdd(char, index, word):
	toAdd = word[0:index]
	toAdd += char
	toAdd += word[index+1:5]
	return toAdd

# tests if the new word is the final word, 
# and if so prints the history and the word
# sets isFinished shared flag to true, so threads know to exit
def isFinalWord(toAdd, word, hist, fin, isFinished):
	if toAdd == fin:
		isFinished[0] = True
		for histWord in hist:
			print histWord
		print word
		print toAdd

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