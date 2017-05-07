import unittest
from unittest.mock import patch

from tinp import finput, tinput
from tinp import InputDoesNotMatchFStr
from tinp import TypeConvertError
from tinp import InputCountNotInRange


class TestTinFunctions(unittest.TestCase):

    @patch('builtins.input', return_value='John,  30, 70.5')
    def test_finput(self, input):
        self.assertEqual(finput(fstr='%s, *%d, *%f', re_escape=False), ('John', 30, 70.5))
        self.assertRaises(InputDoesNotMatchFStr, finput, fstr='%s, %d, %f', re_escape=False)
        self.assertRaises(TypeConvertError, finput, fstr='%d, *%d, *%f', re_escape=False)

    @patch('builtins.input', return_value='5+5')
    def test_finput2(self, input):
        self.assertEqual(finput(fstr='%d+%d'), (5, 5))

    @patch('builtins.input', return_value='1 2 3 4 5')
    def test_tinput(self, input):
        self.assertEqual(sum(tinput(typ=int)), 15)
        self.assertRaises(InputCountNotInRange, tinput, typ=int, min=1, max=3)


if __name__ == '__main__':
    unittest.main()
