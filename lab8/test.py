import unittest

from syntaxkontroll import *


class SyntaxTest(unittest.TestCase):

    def testMolecule(self):
        """ Testar Molekylformeln """
        self.assertEqual(kollaSyntax("Mm4"), "Följer syntaxen!")

    def testFelLitenBokstav(self):
        self.assertEqual(kollaSyntax("cr12"), "Följer inte syntaxen!")

    def testFelLitetNummer(self):
        self.assertEqual(kollaSyntax("Cr0"), "Följer inte syntaxen!")

if __name__ == '__main__':
    unittest.main()