# Syntaxkontroll

from linkedQFile import LinkedQ

class Syntaxfel(Exception):
    pass

# Tar emot listan, q, Kollar molekylen
# <mol>   ::= <group> | <group><mol>
def readMolecule(q, open = False):
    q.printQueue()

    #Det är klart - Returnera till main
    if q.isEmpty():
        if(open == False):
            return
        else:
            raise Syntaxfel(letter + " Det har gått åt helvete")

    else:
        #Fall 1 - Grupp
        readGroup(q)
        #Fall 2 - Grupp med ytterligare en molekyl efter
        readMolecule(q)

# <group> ::= <atom> | <atom><num> | (<mol>) <num>
def readGroup(q):
    firstValue = q.currentQ()
    if (firstValue == "("):
        q.dequeue()
        readMolecule(q, True)

    # Fall 1: Enkel atom
    readAtom(q)

    #Fall 2-3: Atom eller molekyl med nummer efter
    if not q.isEmpty():
        qnu = q.currentQ()
        if(qnu.isdigit()):
            readNumber(qnu)
            q.dequeue()

    #Fall 3: Ny molekyl
    return


   # readMolecule(q)

# <atom>  ::= <LETTER> | <LETTER><letter>
def readAtom(q): 
    characterList = []

    # Fall 1 - en STOR bokstav
    first = readCapitalLetters(q.currentQ())
    second = q.peek()
    q.dequeue()
    characterList.append(first)

    # Fall 2 - En liten bokstav följer
    if not q.isEmpty():
        if(second.isdigit()):
            pass
        elif(readLowerCaseLetters(second)):
            q.dequeue()   
            characterList.append(second)
        elif(readCapitalLetters(second)):
            pass
        else:
            raise Syntaxfel(q.currentQ() + " Är inte en liten bokstav")
        atom = ''.join(characterList)
    return

def readCapitalLetters(letter): #<LETTER>::= A | B | C | ... | Z
    if letter.isupper():
        return letter
    raise Syntaxfel(letter + " Är inte stor bokstav")

def readLowerCaseLetters(letter): #<letter>::= a | b | c | ... | z
    if letter.islower():
        return letter

def readNumber(number): #<num>::= 2 | 3 | 4 | ...
    number = int(number)
    if number >=2:
        return
    raise Syntaxfel(number + " Är inte en siffra")

# def printQueue(q):
#     while not q.isEmpty():
#         word = q.dequeue()
#         print(word, end = " ")
#     print()

# Q är en Linked Queue. 
# Hantering för om tecken är siffra, så att det kan stå 23.
# Lägg till siffror till queuen.
def storeFormula(formel):
    q = LinkedQ()
    numlist = []
    formel = list(formel)
    for tecken in formel:
        if tecken.isdigit():
            numlist.append(tecken)
        else:
            if numlist:
                num_node = ''.join(numlist)
                q.enqueue(num_node)
                numlist = []
            q.enqueue(tecken)

    if numlist:
        num_node = ''.join(numlist)
        q.enqueue(num_node)

    return q

# <formel> ::= <molekyl>
def kollaSyntax(formel):
    q = storeFormula(formel)
    try:
        readMolecule(q)
        return "Formeln är syntaktiskt korrekt"
    except Syntaxfel as fel:
        return str(fel)

def main():
    formel = input("Skriv en formel: ")
    resultat = kollaSyntax(formel)
    print(resultat)

if __name__ == "__main__":
    main()

