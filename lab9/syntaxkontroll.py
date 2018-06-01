# Syntaxkontroll

from linkedQFile import LinkedQ

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


# <mol> ::= <group> | <group><mol>
def readMol(q):
    stack = list()
    # Fall 1: stöter på parentes-början
    if q.currentQ() == '(':
        stack.append(q.currentQ())
        q.dequeue()
        readGroup(q) #kolla grupp inom parentes
        if q.currentQ() == '(': #om grupp inom ännu en parantes, gör koll av grupp
            stack.append(q.currentQ())
            q.dequeue()
            readGroup(q)

    # Fall 2: stöter på parentes-slut
    if q.currentQ() == ')':
        if len(stack) != 0:  # om parentes-början går att ta bort är det matchad parentes
            stack.pop()
            # kollar första så att slutparentes får inte följas av bokstav
            if readCapitalLetters(q.peek()) or readLowerCaseLetters(q.peek()):
                q.dequeue()
                raise Syntaxfel('Saknad siffra vid radslutet ' + q.remainderString())

            # fortsätter efter med att kolla antal paranteser som matchar
            if len(stack) == 0:
                n = 0
                m = 0
                for i in list(q.remainderString()):
                    if i == ')':
                        n = n+1
                    elif i == '(':
                        m = m+1
                if n == m: # om matchade antal - move on
                    pass
                else:
                    raise Syntaxfel('Felaktig gruppstart vid radslutet ' + q.remainderString())

            # kolla om parantes-slut följs av siffra
            if q.peek().isdigit():
                if readNumber(q.peek()):
                    q.dequeue()
                    q.dequeue()
                    pass
            pass
        else:
            raise Syntaxfel('Felaktig gruppstart vid radslutet ' + q.remainderString())

    # om parenteser inte har slutats
    elif len(stack) != 0:
        rest_str = q.remainderString()
        n = 0
        for i in list(rest_str):
            if i == ')':
                n = n+1
        if n == len(stack):
            pass
        else:
            q.dequeue() #för att stämma med kattis
            raise Syntaxfel('Saknad högerparentes vid radslutet '+ q.remainderString())
    else:
        readGroup(q)

    # Fall 2: Kolla om ny grupp börjar
    if q.isEmpty():
        return
    else:
        readMol(q)
    return

# readGroup ska ropa antingen readAtom eller läser en parentes och anropar readMol med det inom parentesen
def readGroup(q):  # <group> ::= <atom> | <atom><num> | (<mol>) <num>
    if q.currentQ() == '(':
        readMol(q)
    # Fall 2: Atom
    else:
        #om atom börjar med siffra
        if q.currentQ().isdigit():
            raise Syntaxfel('Felaktig gruppstart vid radslutet ' + q.remainderString())
        else:
            readAtom(q)

    # Fortsätt se efter grupp eller atom

    # Enkel Atom
    if q.isEmpty():
        return

    # (eller) Siffra efter atom
        #1. om siffra börjas av 0 ges syntaxfel
        #2. om siffra börjas av 1 - se om följs av ännu en siffra, isåfall pass
        #3. om siffra börjas med 0 (0 = 0:e elementet) och följs av vilken siffra som helst,
        #   se till att readNumber läser in 0:e elementet för att då detta ger syntaxfel
    elif ((q.currentQ().isdigit()) or (q.currentQ() == ')' and q.peek().isdigit()) ):
        numlist = []

        # beroende på vilken som är digit sätter vi num på den respektive
        if q.currentQ().isdigit():
            num = list(q.currentQ())
        else:
            q.dequeue()
            num = list(q.currentQ())

        #koll av rätt siffra
        if num[0] == '0':
            q.dequeue() #för att stämma med kattis
            rest = ''.join(num[1:])
            raise Syntaxfel('För litet tal vid radslutet ' + rest + q.remainderString()) #för att stämma med kattis
        elif num[0] == '1':
            if len(num) > 1:
                numlist.append(num[0])
                numlist.append(num[1]) #detta borde appenda det som innan var q.peek()
                number = ''.join(numlist)    #så länge 1 alltid följs av någon siffra, är det en valid siffra
                readNumber(int(number))      #dubbelkoll av siffra
            else:
                q.dequeue() #för att stämma med kattis
                raise Syntaxfel('För litet tal vid radslutet ' + q.remainderString())
        else:
            readNumber(q.currentQ())
            q.dequeue()
    else: #överflödig?
        return

    return



# <atom>  ::= <LETTER> | <LETTER><letter>
def readAtom(q):
    characterList = []
    first = str(q.currentQ())
    second = str(q.peek())

    # Fall 1: en STOR bokstav
    if (readCapitalLetters(first)):
        characterList.append(first)
        q.dequeue()
    else:
        raise Syntaxfel("Saknad stor bokstav vid radslutet " + q.remainderString())

    # Fall 2: En STOR bokstav följs av en liten bokstav
    if not q.isEmpty():
        if(readLowerCaseLetters(second)):
            q.dequeue()
            characterList.append(second)

    # Undantagsfall:
        # 1. om följs av siffra, gör inget inom denna koll av "valid atom"
        elif(q.currentQ().isdigit()):
            pass
        # 2. om molekyl?
        elif(readCapitalLetters(q.currentQ())):
            readAtom(q)
        # 3. om paranteser, kan dessa fall finnas
        #   a. ny atomgrupp börjas -> gå tillbaka till readGroup/readmol, för att läsa om grupp
        #   b. atomgrupp avslutas -> gå tillbaka till readGroup för att se om grupp följs av siffra
        #   c. felaktig start/slut, detta borde kollas i readGroup för att se om parenteser matchar
        elif(q.currentQ() == "(" or q.currentQ() == ")"):
            pass


    atom = ''.join(characterList)
    if not (isAtom(atom)):
        raise Syntaxfel("Okänd atom vid radslutet " + q.remainderString())
    return


# <LETTER>::= A | B | C | ... | Z
def readCapitalLetters(letter):
    if letter.isupper():
        return letter


# <letter>::= a | b | c | ... | z
def readLowerCaseLetters(letter):
    if letter.islower():
        return letter


# <num>::= 2 | 3 | 4 | ...
def readNumber(number):
    number = int(number)
    if number >= 2:
        return number

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


def isAtom(atom):
    if(atom in atoms):
        return True


# <formel> ::= <molekyl>
def kollaSyntax(formel):
    q = storeFormula(formel)
    try:
        readMol(q)
        return "Formeln är syntaktiskt korrekt"
    except Syntaxfel as fel:
        return str(fel)


def main():
    formel = input("Skriv en formel: ")
    resultat = kollaSyntax(formel)
    print(resultat)

if __name__ == "__main__":
    main()
