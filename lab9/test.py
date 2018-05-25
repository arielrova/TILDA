import unittest

from syntaxkontroll import *


class SyntaxTest(unittest.TestCase):

    # En enkel atom
    def testAtom(self):
        self.assertEqual(kollaSyntax("Na"), "Formeln är syntaktiskt korrekt")

    # En enkel molekyl
    def testSimpleMolecule(self):
        self.assertEqual(kollaSyntax("H2O"), "Formeln är syntaktiskt korrekt")

    # En grupp med stora numbers
    def bigNumber(self):
        self.assertEqual(kollaSyntax("Na332"), "Formeln är syntaktiskt korrekt")

    # En grupp
    def testGroup(self):
        self.assertEqual(kollaSyntax("Si(C3(COOH)2)4(H2O)7"), "Formeln är syntaktiskt korrekt") 

    # En enkel atom
    def unknownAtom(self):
        self.assertEqual(kollaSyntax("C(Xx4)5"), "Okänd atom vid radslutet 4)5")

    def missingNumberAtEndOfGroup(self):
        self.assertEqual(kollaSyntax("C(OH4)C"), "Saknad siffra vid radslutet C")

    def missingRightParenthesis(self):
        self.assertEqual(kollaSyntax("C(OH4C"), "Saknad högerparentes vid radslutet")

    def wrongGroupStart(self):
        self.assertEqual(kollaSyntax("H2O)Fe"), "Felaktig gruppstart vid radslutet )Fe")

    def numberIsZero(self):
        self.assertEqual(kollaSyntax("H0"), "För litet tal vid radslutet")

    def numberIsOne(self):
        self.assertEqual(kollaSyntax("H1C"), "För litet tal vid radslutet C")

    def numberIsWeird(self):
        self.assertEqual(kollaSyntax("H02C"), "För litet tal vid radslutet 2C") #dequear 2 för att den läser 02 som ett tal

    def capitalLetterIsMissing(self):
        self.assertEqual(kollaSyntax("Nacl"), "Saknad stor bokstav vid radslutet cl")

    def capitalLetterIsMissing(self):
        self.assertEqual(kollaSyntax("a"), "Saknad stor bokstav vid radslutet a")

    def wrongGroupStart2(self):
        self.assertEqual(kollaSyntax("(Cl)2)3"), "Felaktig gruppstart vid radslutet )3")

    def justParenthesis(self):
        self.assertEqual(kollaSyntax(")"), "Felaktig gruppstart vid radslutet )")

    def justnumber(self):
        self.assertEqual(kollaSyntax("2"), "Felaktig gruppstart vid radslutet 2")


if __name__ == '__main__':
    unittest.main()
