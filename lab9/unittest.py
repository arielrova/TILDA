from sys import stdin

import unittest



class SyntaxTest(unittest.TestCase):

    def testSample1(self):
        """ Testar Molekylformeln"""
        stdin = open("correct_sample.in")
        stout = open("correct_sample.ans")
        inp = stdin.readline()
        outp = stout.readline()

        self.assertEqual(kollaSyntax(inp), outp)

    def testSample2(self):
        stdin = open("incorrect_sample.in")
        stdout = open("incorrect_sample.ans")
        inp = stdin.readline()
        outp = stdout.readline()
        self.assertEqual(kollaSyntax(inp), outp)


if __name__ == '__main__':
    unittest.main()