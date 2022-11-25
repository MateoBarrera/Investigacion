import unittest
from potentials.source import *


class TestStringMethods(unittest.TestCase):

    def test_read_csv(self):
        """read_csv return true for correct read csv file.
        """
        test_obj = PrimaryResource(source='Ideam')
        self.assertTrue(test_obj.from_csv('./recursos/hydro/caudal_medio_mensual/Valle.csv.csv'))

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
