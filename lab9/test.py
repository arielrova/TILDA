import unittest

from syntaxkontroll import *


class SyntaxTest(unittest.TestCase):

    # En enkel atom
    def testAtom(self):
        self.assertEqual(kollaSyntax("Na"), "Formeln är syntaktiskt korrekt") #funkar!

    # En enkel molekyl
    def testSimpleMolecule(self):
        self.assertEqual(kollaSyntax("H2O"), "Formeln är syntaktiskt korrekt") #funkar!

    # En grupp med stora numbers
    def bigNumber(self):
        self.assertEqual(kollaSyntax("Na332"), "Formeln är syntaktiskt korrekt") #funkar!

    # En grupp
    def testGroup(self):
        self.assertEqual(kollaSyntax("Si(C3(COOH)2)4(H2O)7"), "Formeln är syntaktiskt korrekt") #funkar!

    # En enkel atom
    def unknownAtom(self):
        self.assertEqual(kollaSyntax("C(Xx4)5"), "Okänd atom vid radslutet 4)5") #funkar!

    def missingNumberAtEndOfGroup(self):
        self.assertEqual(kollaSyntax("C(OH4)C"), "Saknad siffra vid radslutet C") #funkar!

    def missingRightParenthesis(self):
        self.assertEqual(kollaSyntax("C(OH4C"), "Saknad högerparentes vid radslutet") #funkar!

    def wrongGroupStart(self):
        self.assertEqual(kollaSyntax("H2O)Fe"), "Felaktig gruppstart vid radslutet )Fe") #funkar!

    def numberIsZero(self):
        self.assertEqual(kollaSyntax("H0"), "För litet tal vid radslutet") #funkar!

    def numberIsOne(self):
        self.assertEqual(kollaSyntax("H1C"), "För litet tal vid radslutet C") #funkar!

    def numberIsWeird(self):
        self.assertEqual(kollaSyntax("H02C"), "För litet tal vid radslutet 2C") #funkar!

    def capitalLetterIsMissing(self):
        self.assertEqual(kollaSyntax("Nacl"), "Saknad stor bokstav vid radslutet cl") #funkar!

    def capitalLetterIsMissing(self):
        self.assertEqual(kollaSyntax("a"), "Saknad stor bokstav vid radslutet a") #funkar!

    def wrongGroupStart2(self):
        self.assertEqual(kollaSyntax("(Cl)2)3"), "Felaktig gruppstart vid radslutet )3") #funkar!

    def justParenthesis(self):
        self.assertEqual(kollaSyntax(")"), "Felaktig gruppstart vid radslutet )") #funkar!

    def justnumber(self):
        self.assertEqual(kollaSyntax("2"), "Felaktig gruppstart vid radslutet 2") #funkar!


if __name__ == '__main__':
    unittest.main()
