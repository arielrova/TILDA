# Syntaxkontroll
from sys import *
from linkedQFile import LinkedQ
from molgrafik import Molgrafik, Ruta
from pprint import pprint

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
        mol = readMolecule(q)

    return mol

def readMolecule(q): #<molekyl> ::= <atom> | <atom><num>    #två vägar:
                                                            # - läsa grupp(molekyl inom parentes - deqeue parantes, kalla readmol)
                                                            # - läsa enbart molekyl(inga parenteser, kalla readatom för koll av rätt atomstruktur)
   
    # --- ARIEL --- # Skapar en rot-ruta, alla andra rutor hänger på den här genom next.
    ruta = Ruta()
    if q.isEmpty():   # om tom efter tidigare tester, return
        return ruta

    if q.currentQ() == '(':
        q.dequeue()
        readGroup(q, ruta)
    elif q.currentQ() in uppercase:
        # --- ARIEL --- # Skriver över den tomma rutan med return från readAtom
        ruta = readAtom(q, ruta)
    elif q.currentQ() in lowercase:
        raise Syntaxfel('Saknad stor bokstav vid radslutet')
    else:
        raise Syntaxfel('Felaktig gruppstart vid radslutet')

    #Borde komma hit om atom-koll har avslutats eller stött på en slutparantes

    if q.isEmpty():

        # --- ARIEL --- # Skickar tillbaka rot-rutan
        return ruta
    elif q.currentQ() != ')': #om kön inte har tömts, gör rekursion av readMol
        readMolecule(q)

    return


def readGroup(q): #Gå tillbaka till readMol för att kolla atomsyntax av grupp inom parantes

    if q.isEmpty(): #kan vara tom eftersom condition för att påbörja readGroup är att kön har börjat med en öppningsparantes
        return

    readMolecule(q)

    if q.isEmpty():
        raise Syntaxfel('Saknad högerparentes vid radslutet')

    if q.currentQ() == ')' and q.peek() in numbers:
        readNumber(q)
        q.dequeue()
    else:
        q.dequeue()
        raise Syntaxfel('Saknad siffra vid radslutet')

    if not q.isEmpty():
        if q.currentQ() in uppercase:
            q.dequeue()
            raise Syntaxfel('Saknad siffra vid radslutet')
        elif q.currentQ() in numbers:
            readNumber(q)

    return


def readAtom(q, ruta): # <atom>  ::= <LETTER> | <LETTER><letter>
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
            # --- ARIEL --- # Om första noden redan innehåller atom,
            # --- ARIEL --- # skapa en ny nod, i båda fallen lägg till atomen.
            if(ruta.atom == "()"):
                ruta.atom = atom
                print(ruta.atom)
            else:
                nyruta = Ruta()
                nyruta.atom = atom
                ruta.next = nyruta
        else:
            raise Syntaxfel('Okänd atom vid radslutet')
    else:
        if upper in atoms: #men om kön inte är tom, kollar vi här om upper är en 1-bokstavig godkänd atom
            pass
        else:
            raise Syntaxfel('Okänd atom vid radslutet')

    if q.isEmpty():     #koll om tom igen efter föregående koll
        return ruta
    elif q.currentQ() in numbers:
        ruta.num = int(readNumber(q))
    elif q.currentQ() in uppercase:
        readAtom(q, ruta)

    # --- ARIEL --- # För kontroll - skriver ut atom och nummer för första noden och andra 
    print(ruta.atom)
    print(ruta.num)
    if(ruta.next):
        print(ruta.next.atom)
        print(ruta.next.num)
    return ruta



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
        grafik = readFormula(q)
        # return "Formeln är syntaktiskt korrekt"
        return grafik
    except Syntaxfel as fel:
        if q.remainderString():
            return str(fel) + " " + q.remainderString()
        else:
            return str(fel)

def main():

    while True:
        # --- ARIEL --- # Molgrafik innehåller allt som behövs för att rita trädet
        # --- ARIEL --- # Vi behöver inte tänka särskilt på det.
        mg = Molgrafik()
        formel = input("Skriv in en formel ")
        resultat = kollaSyntax(formel)
        # print(resultat)

        # --- ARIEL --- # Det händer bara      
        mg.show(resultat)


if __name__ == "__main__":
    main()
