# Syntaxkontroll

from linkedQFile import LinkedQ

class Syntaxfel(Exception):
    pass

def readMolecule(q): #<molekyl> ::= <atom> | <atom><num>
    readAtom(q)
    if q.peek():
        while not q.isEmpty():
            qnext = q.dequeue()
            if qnext.isdigit():
                readNumber(qnext)
            else:
               raise Syntaxfel
    else:
        return

def readAtom(q): # <atom>  ::= <LETTER> | <LETTER><letter>
    readCapitalLetters(q)
    if q.peek():
        item = q.dequeue()
        if item.isdigit():
            q.enqueue(item)
        else:
            readLowerCaseLetters(item)
    else:
        return

def readCapitalLetters(q): #<LETTER>::= A | B | C | ... | Z
    letter = q.dequeue()
    if letter.isupper():
        return
    raise Syntaxfel

def readLowerCaseLetters(letter): #<letter>::= a | b | c | ... | z
    if letter.islower():
        return
    raise Syntaxfel

def readNumber(number): #<num>::= 2 | 3 | 4 | ...
    number = int(number)
    print(number)
    if number >=2:
        return number
    raise Syntaxfel

def printQueue(q):
    while not q.isEmpty():
        word = q.dequeue()
        print(word, end = " ")
    print()

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

    print('1. '+str(numlist))
    print('2. ' +(num_node))
    return q

# Formel är input från input-fältet.
# q returneras från storeFormula
# Om readMolecule - Syntaxen följs. Annars, raise exception.
def kollaSyntax(formel):
    q = storeFormula(formel)
    try:
        readMolecule(q)
        return "Följer syntaxen!"
    except Syntaxfel:
        return "Följer inte syntaxen!"

def main():
    formel = input("Skriv en formel: ")
    resultat = kollaSyntax(formel)
    print(resultat)

if __name__ == "__main__":
    main()

