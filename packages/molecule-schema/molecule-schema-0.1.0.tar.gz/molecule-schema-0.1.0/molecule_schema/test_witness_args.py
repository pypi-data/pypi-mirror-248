import unittest
from molecule_schema import Table
from molecule_schema.predefined import Bytes, BytesOpt


class WitnessArgs(Table):
    molecule_types: BytesOpt()
    molecule_types: BytesOpt()
    molecule_types: BytesOpt()


class TestStringMethods(unittest.TestCase):
    def test_pack_default_witness_args(self):
        bytes = WitnessArgs().pack()
        self.assertEqual(bytes.hex(), "10000000100000001000000010000000")


if __name__ == "__main__":
    unittest.main()
