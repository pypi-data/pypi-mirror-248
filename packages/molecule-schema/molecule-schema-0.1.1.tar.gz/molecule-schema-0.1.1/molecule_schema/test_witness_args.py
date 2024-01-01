import unittest
from molecule_schema.schema import Table
from molecule_schema.predefined import BytesOpt


class WitnessArgs(Table):
    lock: BytesOpt
    input_type: BytesOpt
    output_type: BytesOpt


class TestWitnessArgs(unittest.TestCase):
    def test_pack_default_witness_args(self):
        input = WitnessArgs()
        output = WitnessArgs.pack(input)
        self.assertEqual(output.hex(), "10000000100000001000000010000000")

    def test_pack_witness_args(self):
        input = WitnessArgs(lock=None, input_type=b"", output_type=b"\1")
        output = WitnessArgs.pack(input)
        self.assertEqual(
            output.hex(), "19000000100000001000000014000000000000000100000001"
        )

    def test_pack_witness_args_using_dict(self):
        output = WitnessArgs.pack(
            {"lock": None, "input_type": b"", "output_type": b"\1"}
        )
        self.assertEqual(
            output.hex(), "19000000100000001000000014000000000000000100000001"
        )

    def test_pack_witness_args_using_kwargs(self):
        output = WitnessArgs.pack(lock=None, input_type=b"", output_type=b"\1")
        self.assertEqual(
            output.hex(), "19000000100000001000000014000000000000000100000001"
        )

    def test_unpack_witness_args(self):
        output = WitnessArgs.unpack(
            bytes.fromhex("19000000100000001000000014000000000000000100000001")
        )
        self.assertEqual(output.lock, None)
        self.assertEqual(output.input_type, b"")
        self.assertEqual(output.output_type, b"\1")

    def test_attach_witness_args(self):
        output = WitnessArgs.attach(
            bytes.fromhex("19000000100000001000000014000000000000000100000001")
        )
        self.assertEqual(output.lock, None)
        self.assertEqual(output.input_type.value, b"")
        self.assertEqual(output.output_type.value, b"\1")


if __name__ == "__main__":
    unittest.main()
