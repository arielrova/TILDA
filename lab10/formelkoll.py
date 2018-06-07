# Syntaxkontroll
from sys import *
from linkedQFile import LinkedQ
from molgrafik import Molgrafik, Ruta

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

def readMolecule(q): #<molekyl> ::= <atom> | <atom><num>    #två vägar:
                                                            # - läsa grupp(molekyl inom parentes - deqeue parantes, kalla readmol)
                                                            # - läsa enbart molekyl(inga parenteser, kalla readatom för koll av rätt atomstruktur)
    if q.isEmpty():   # om tom efter tidigare tester, return
        return

    if q.currentQ() == '(':
        q.dequeue()
        readGroup(q)
    elif q.currentQ() in uppercase:
        readAtom(q)
    elif q.currentQ() in lowercase:
        raise Syntaxfel('Saknad stor bokstav vid radslutet')
    else:
        raise Syntaxfel('Felaktig gruppstart vid radslutet')

    #Borde komma hit om atom-koll har avslutats eller stött på en slutparantes

    if q.isEmpty():
        return
    elif q.currentQ() != ')': #om kön inte har tömts, gör rekursion av readMol
        readMolecule(q)

    return


def readGroup(q): #Gå tillbaka till readMol för att kolla atomsyntax av grupp inom parantes
    ruta = Ruta()

    if q.isEmpty(): #kan vara tom eftersom condition för att påbörja readGroup är att kön har börjat med en öppningsparantes
        return

    ruta.down = readMolecule(q)

    if q.isEmpty():
        raise Syntaxfel('Saknad högerparentes vid radslutet')

    if q.currentQ() == ')' and q.peek() in numbers:
        ruta.num = readNumber(q)
        q.dequeue()
    else:
        q.dequeue()
        raise Syntaxfel('Saknad siffra vid radslutet')

    if not q.isEmpty():
        if q.currentQ() in uppercase:
            q.dequeue()
            raise Syntaxfel('Saknad siffra vid radslutet')
        elif q.currentQ() in numbers:
            ruta.num = readNumber(q)

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
    tal = ""
    if q.isEmpty():
        return

    if q.currentQ():
        first = q.currentQ()

        if first == '0' or first == '1' and q.peek() not in numbers:
            tal += q.dequeue()
            raise Syntaxfel('För litet tal vid radslutet')
        else:
            while q.currentQ() in numbers:
                tal += q.dequeue()
                #kommer nu kolla om det efter first (som blir q.currentQ()) är in numbers,
                # men om tom, kommer den ge error pga den försöker läsa none-type object
                if q.isEmpty():
                    break

    return tal

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
    mg = Molgrafik()

    while True:
        formel = input("Skriv in en formel ")
        resultat = kollaSyntax(formel)
        print(resultat)
        # mg.show(resultat)


    # for line in stdin:
    #     line = line.rstrip('\n')
    #     if (line != '#'):
    #         resultat = kollaSyntax(line)
    #         print(resultat)
    #     else:
    #         break


if __name__ == "__main__":
    main()
