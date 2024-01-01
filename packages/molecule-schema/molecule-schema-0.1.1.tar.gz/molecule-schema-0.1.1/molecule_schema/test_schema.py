import unittest
from molecule_schema.schema import Byte, Bytes


class TestByte(unittest.TestCase):
    def test_class_pack(self):
        actual = Byte.pack(1)
        self.assertEqual(actual.hex(), "01")

    def test_unpack(self):
        buffer = bytearray(b"\2")
        actual = Byte.unpack(buffer)
        self.assertEqual(actual, 2)

    def test_attach(self):
        buffer = bytearray(b"\2")
        actual = Byte.attach(buffer)
        self.assertEqual(actual.value, 2)


class TestBytes(unittest.TestCase):
    def test_class_pack(self):
        actual = Bytes.pack(b"\1\2")
        self.assertEqual(actual.hex(), "020000000102")

    def test_unpack(self):
        buffer = bytearray(b"\4\0\0\0\1\2\3\4")
        actual = Bytes.unpack(buffer)
        self.assertEqual(actual, b"\1\2\3\4")

    def test_attach(self):
        buffer = bytearray(b"\4\0\0\0\1\2\3\4")
        actual = Bytes.attach(buffer)
        self.assertEqual(actual.value, b"\1\2\3\4")


if __name__ == "__main__":
    unittest.main()
