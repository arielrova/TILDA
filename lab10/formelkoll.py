from linkedQFile import LinkedQ
from molgrafik import *
from hashtest import hashtabell



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
        tree = readMolecule(q, ruta = Ruta())

    return tree

def readMolecule(q, ruta):
    tree = readGroup(q, ruta)

    if not q.isEmpty() and q.currentQ() is not ')':
        readMolecule(q, tree)

    return tree

def readGroup(q, ruta = Ruta()):
    if not q.isEmpty() and q.currentQ() in uppercase:
        ruta = readAtom(q)

    elif q.currentQ() is '(':
        q.dequeue()
        ruta.next = Ruta()
        ruta.next.down = readMolecule(q, ruta)
        if not q.isEmpty() and q.currentQ() is ')':
            q.dequeue()
        else:
            raise Syntaxfel("Saknad högerparantes vid radslutet")
        if not q.isEmpty() and q.currentQ().isdigit():
            ruta.next.num = readNumber(q)
        else:
            raise Syntaxfel("Saknad siffra vid radslutet")
        return ruta.next

    else:
        if q.currentQ() is ')' or q.currentQ().isdigit():
            raise Syntaxfel("Felaktig gruppstart vid radslutet")
        elif q.currentQ() in lowercase:
            raise Syntaxfel("Saknad stor bokstav vid radslutet")
        else:
            return ruta

    return ruta


def readAtom(q): # <atom>  ::= <LETTER> | <LETTER><letter>
    #Här borde atom kollas igenom om den har rätt syntax OCH finns i listan av atomer
    ruta = Ruta()
    upper = q.currentQ()

    if upper in uppercase:
        upperAtom = q.dequeue()
        ruta.atom = upperAtom
    else:
        raise Syntaxfel('Saknad stor bokstav vid radslutet')


    if q.isEmpty():         #kolla om tom, annars försöker programmet läsa NoneType-objects och ger errors
        if upper in atoms:  #eftersom vi dequat innan måste vi också att upper är en 1-bokstavig godkänd atom
            return ruta
        else:
            raise Syntaxfel('Okänd atom vid radslutet')

    if q.currentQ() in lowercase: #kolla 2-bokstavig godkänd atom
        lower = q.dequeue()
        atom = upper+lower
        if atom in atoms:
            ruta.atom = atom
        else:
            raise Syntaxfel('Okänd atom vid radslutet')
    else:
        if upper in atoms: #men om kön inte är tom, kollar vi här om upper är en 1-bokstavig godkänd atom
            pass
        else:
            raise Syntaxfel('Okänd atom vid radslutet')

    if q.isEmpty():     #koll om tom igen efter föregående koll
        return ruta
    else:
        if q.currentQ() in numbers:
            ruta.num = int(readNumber(q))
        if not q.isEmpty():
            if q.currentQ() in uppercase:
                ruta.next = readAtom(q)
    return ruta


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

    return int(first)

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
        tree = readFormula(q)
        return tree
    except Syntaxfel as fel:
        if q.remainderString():
            return str(fel) + " " + q.remainderString()
        else:
            return str(fel)

def calcWeight(tree):
     #hashtabellens uppbyggnad har atomnamn som 'key'
     #varje key har ett objekt med attributen namn och vikt

    if tree:       # kolla om true för varje rekursion
        if tree.down: # om formel har molekylgrupper inom parenteser
            grupp_vikt = float(calcWeight(tree.down))*float(tree.num)
            return grupp_vikt + float(calcWeight(tree.next))
        else:
            atom_obj = hashtabell.get(tree.atom)
            vikt = float(atom_obj.value.vikt) * float(tree.num)
            return vikt + float(calcWeight(tree.next))

    return 0

def main():
    while True:
        mg = Molgrafik()
        formel = input("Skriv in en formel!")
        tree = kollaSyntax(formel)
        weight = calcWeight(tree)
        mg.show(tree)
        print('Total vikt: ' + str(weight))


if __name__ == "__main__":
    main()
