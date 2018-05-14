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

if __name__ == '__main__':
    unittest.main()