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
def readMolecule(q):
    parantes = False
    if q.isEmpty():
        return
    else:
        first = q.currentQ()
        # Fall 1 - Gruppstart
        if (first == "("):
            parantes = True
            q.dequeue()
            print("inne!")
            q.printQueue()
            readGroup(q)

        # Fall 1 - Gruppslut
        elif(first == ")"):
            # parenthesisErrorHandling(q)
            q.dequeue()
            if(q.currentQ().isdigit()):
                if(readNumber(q.currentQ())):
                    q.dequeue()
                    return readMolecule(q)
                else:
                    raise Syntaxfel("Felaktig siffra i slutet av...")
        else:
            readGroup(q)

    if(q.isEmpty() == False):
        if(q.currentQ() == ")" and parantes == False):
            raise Syntaxfel("Felaktig gruppstart vid radslutet " + q.remainderString())
    readMolecule(q)

# <group> ::= <atom> | <atom><num> | (<mol>) <num>
def readGroup(q):

    # Fall 1 - Enkel atom
    readAtom(q)

   # Fall 2 - Siffra efter atom
    if(q.currentQ().isdigit()):
        readNumber(q.currentQ())
        q.dequeue()

   # Fall 3 - Atom eller grupp med nummer efter
    if(q.currentQ() == ")"):
        q.dequeue()
        if not q.isEmpty():
            if(q.currentQ().isdigit()):
                readNumber(q.currentQ())
                q.dequeue()

    return


# <atom>  ::= <LETTER> | <LETTER><letter>
def readAtom(q):
    characterList = []
    first = q.currentQ()
    second = q.peek()

    # Fall 1 - en STOR bokstav
    if (readCapitalLetters(first)):
        characterList.append(first)
        q.dequeue()
    else:
        raise Syntaxfel(first + "Är inte en stor bokstav")

    if not q.isEmpty():
        # Fall 2 - En STOR bokstav följs av en liten bokstav
        if(readLowerCaseLetters(second)):
            q.dequeue()
            characterList.append(second)

        # Undantagsfall:
        elif(q.currentQ().isdigit()):
            pass
        elif(readCapitalLetters(q.currentQ())):           
            readAtom(q)
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
