import sys

sys.setrecursionlimit(2000)

class Node:
    def __init__(self, value, next = None):
        self.value = value
        self.next = next

    def __str__(self):
        s = str(self.value)
        return s

class LinkedQ:

    def __init__(self):
        self.__first = None
        self.__last = None

    def enqueue(self, item):
        newnode = Node(item)
        if self.isEmpty():
            self.__first = self.__last = newnode
        else:
            self.__last.next = newnode
            self.__last = newnode
        return newnode

    def dequeue(self):                  #syfte: ta bort och returnera det första nod-värdet i kön
        if self.isEmpty():              #om listan är tom, då e den tom
            return None
        else:
            value = self.__first.value                  #det vi vill ta bort och returnera
            secondNode = self.__first.next              #vill veta vad vi sätter till nytt value = second
            if secondNode is None:                      #om det bara finns en nod i ledet
                self.__first = self.__last = None           #då blir det en tom kö
            else:
                self.__first = secondNode               #annars blir det nya
            return value

    def isEmpty(self):
       if self.__first is None:
            return True

    def currentQ(self):
        return self.__first.value

    def peek(self):
        if self.isEmpty():
            return None 
        elif not self.__first.next:
            return self.__first.value
        else:
            nextnode = self.__first.next
            return nextnode.value

    def printQueue(self):
        nextNode = self.__first
        while(nextNode != None):
            print(nextNode.value)
            nextNode = nextNode.next
            if nextNode == None:
                print("\n" + "\n")

    def remainderString(self):
        remainderList = []
        nextNode = self.__first
        while(nextNode != None):
            remainderList.append(nextNode.value)
            nextNode = nextNode.next

        return ''.join(remainderList)



