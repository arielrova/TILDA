# Syntaxkontroll
from sys import *

class Node:
    def __init__(self, value, next = None):
        self.value = value
        self.next = next

    def __str__(self):
        return str(self.value)

class LinkedQ:
    def __init__(self):
        self.__first=None
        self.__last=None

    def enqueue(self, item):
        newnode = Node(item)
        if self.isEmpty():
            self.__first=self.__last = newnode
        else:
            self.__last.next = newnode
            self.__last = newnode
        return newnode

    def dequeue(self):                  #syfte: ta bort och returnera det första nod-värdet i kön
        if self.isEmpty():              #om listan är tom, då e den tom
            return None
        else:
            value = self.__first.value                  #det vi vill ta bort och returnera
            secondNode = self.__first.next                #vill veta vad vi sätter till nytt value = second
            if secondNode is None:                        #om det bara finns en nod i ledet
                self.__first=self.__last = None           #då blir det en tom kö
            else:
                self.__first = secondNode               #annars blir det nya
            return value

    def isEmpty(self):
       if self.__first is None:
            return True

    def peek(self):
        if self.__first.next is None:
            return False
        else:
            nextnode = self.__first.next
            return nextnode.value

    def currentQ(self):
        return self.__first.value


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

uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lowercase = 'abcdefghijklmnopqrstuvwxyz'
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

atoms = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg",
            "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr",
            "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
            "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd",
            "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
            "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf",
            "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po",
            "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm",
            "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh",
            "Hs", "Mt", "Ds", "Rg", "Cn", "Fl", "Lv"]

class Syntaxfel(Exception):
    pass

def readFormula(q):                                             #om tom, ge syntaxfel
    if q.isEmpty():
        raise Syntaxfel('Felaktig gruppstart vid radslutet')

    while not q.isEmpty():
        readMolecule(q)

    return

# <mol>   ::= <group> | <group><mol>
def readMolecule(q):  
    if q.isEmpty():   # om tom efter tidigare tester, return
        return
    else:
        readGroup(q)
        if not q.isEmpty():
            if q.currentQ() == ')' and q.peek() in numbers:
                readNumber(q)
                q.dequeue()
            elif q.currentQ() in uppercase or q.currentQ() in lowercase:
                q.dequeue()
                raise Syntaxfel('Saknad siffra vid radslutet')
    return


        # raise Syntaxfel('Felaktig gruppstart vid radslutet')

# <group> ::= <atom> |<atom><num> | (<mol>) <num>
def readGroup(q): #Gå tillbaka till readMol för att kolla atomsyntax av grupp inom parantes

    if q.currentQ() in uppercase:
        readAtom(q)
        if not q.isEmpty() and q.currentQ() is not ')':
            readGroup(q)
    elif q.currentQ() in lowercase:
        raise Syntaxfel('Saknad stor bokstav vid radslutet')

    if q.isEmpty(): #kan vara tom eftersom condition för att påbörja readGroup är att kön har börjat med en öppningsparantes
        return

    if q.currentQ() == '(':
        q.dequeue()
        readMolecule(q)

    q.printQueue()

    if q.isEmpty():
        raise Syntaxfel('Saknad högerparentes vid radslutet')
    else:
        if q.currentQ() in uppercase:
            q.dequeue()
            raise Syntaxfel('Saknad siffra vid radslutet')
        elif q.currentQ() in numbers:
            readNumber(q)
        else:
            return
            # raise Syntaxfel('Felaktig gruppstart vid radslutet')

    return


def readAtom(q): # <atom>  ::= <LETTER> | <LETTER><letter>
    #Här borde atom kollas igenom om den har rätt syntax OCH finns i listan av atomer
    upper = q.currentQ()

    if upper in uppercase:
        q.dequeue()
    else:
        raise Syntaxfel('Saknad stor bokstav vid radslutet')


    if q.isEmpty():         #kolla om tom, annars försöker programmet läsa NoneType-objects och ger errors
        if upper in atoms:  #eftersom vi dequat innan måste vi också att upper är en 1-bokstavig godkänd atom
            return
        else:
            raise Syntaxfel('Okänd atom vid radslutet')

    if q.currentQ() in lowercase: #kolla 2-bokstavig godkänd atom
        lower = q.dequeue()
        atom = upper+lower
        if atom in atoms:
            pass
        else:
            raise Syntaxfel('Okänd atom vid radslutet')
    else:
        if upper in atoms: #men om kön inte är tom, kollar vi här om upper är en 1-bokstavig godkänd atom
            pass
        else:
            raise Syntaxfel('Okänd atom vid radslutet')

    if q.isEmpty():     #koll om tom igen efter föregående koll
        return
    elif q.currentQ() in numbers:
        readNumber(q)
    elif q.currentQ() in uppercase:
        readAtom(q)

    return



def readNumber(q): #<num>::= 2 | 3 | 4 | ...
    if q.isEmpty():
        return

    if q.currentQ():
        first = q.currentQ()

        if first == '0' or first == '1' and q.peek() not in numbers:
            q.dequeue()
            raise Syntaxfel('För litet tal vid radslutet')
        else:
            while q.currentQ() in numbers:
                q.dequeue()
                #kommer nu kolla om det efter first (som blir q.currentQ()) är in numbers,
                # men om tom, kommer den ge error pga den försöker läsa none-type object
                if q.isEmpty():
                    break

    return

def printQueue(q):
    while not q.isEmpty():
        word = q.dequeue()
        print(word, end = " ")
    print()

def storeFormula(formel):
    q = LinkedQ()
    formel = list(formel)
    for tecken in formel:
        q.enqueue(tecken)

    return q

def kollaSyntax(formel):
    q = storeFormula(formel)
    try:
        readFormula(q)
        return "Formeln är syntaktiskt korrekt"
    except Syntaxfel as fel:
        if q.remainderString():
            return str(fel) + " " + q.remainderString()
        else:
            return str(fel)

def main():

    for line in stdin:
        line = line.rstrip('\n')
        if (line != '#'):
            resultat = kollaSyntax(line)
            print(resultat)
        else:
            break


if __name__ == "__main__":
    main()
