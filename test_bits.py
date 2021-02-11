import unittest
from bits import BitList, DecodeError, ChunkError

class TestBitList(unittest.TestCase):

    def test_constructor_value_error_bits(self):
        with self.assertRaises(ValueError):
            b = BitList('FE110000')

    def test_from_ints(self):
        self.assertEqual(BitList.from_ints(1, 1, 0, 0), BitList('1100'))

    def test_from_ints_error(self):
        with self.assertRaises(ValueError):
            BitList.from_ints(1, 2, 3, 4)

    def test_arithmetic_shift_left(self):
        b = BitList('01000001')
        b.arithmetic_shift_left()
        self.assertEqual(b, BitList('10000010'))

        b = BitList('01000000')
        b.arithmetic_shift_left()
        self.assertEqual(b, BitList('10000000'))

    def test_arithmetic_shift_right_1(self):
        b = BitList('10000000')
        b.arithmetic_shift_right()
        self.assertEqual(b, BitList('11000000'))

        b = BitList('10000001')
        b.arithmetic_shift_right()
        self.assertEqual(b, BitList('11000000'))

    def test_arithmetic_shift_right_0(self):
        b = BitList('01111111')
        b.arithmetic_shift_right()
        self.assertEqual(b, BitList('00111111'))

        b = BitList('01111110')
        b.arithmetic_shift_right()
        self.assertEqual(b, BitList('00111111'))

    def test_and(self):
        b1 = BitList('10000011')
        b2 = BitList('11000001')
        self.assertEqual(b1.bitwise_and(b2), BitList('10000001'))

    def test_str(self):
        self.assertEqual(str(BitList('1010')), '1010')

    def test_equals(self):
        self.assertEqual(BitList('1010'), BitList('1010'))

    def test_decode_ascii_A(self):
        b = BitList('1000001')
        self.assertEqual(b.decode('us-ascii'), 'A')

    def test_decode_ascii_bracket(self):
        b = BitList('1011011')
        self.assertEqual(b.decode('us-ascii'), '[')

    def test_decode_ascii_multiple_chars(self):
        b = BitList('10000011011011')
        self.assertEqual(b.decode('us-ascii'), 'A[')

    def test_decode_utf8_4_bytes_multiple_chars(self):
        b = BitList('11110000100111111001100010000010111000101000001010101100')
        self.assertEqual(b.decode('utf-8'), '😂€')

    def test_decode_utf8_4_bytes(self):
        b = BitList('11110000100111111001100010000010')
        self.assertEqual(b.decode('utf-8'), '😂')

    def test_decode_utf8_3_bytes(self):
        b = BitList('111000101000001010101100')
        self.assertEqual(b.decode('utf-8'), '€')

    def test_decode_utf8_1_byte(self):
        b = BitList('01000001')
        self.assertEqual(b.decode('utf-8'), 'A')

    def test_decode_utf8_default(self):
        b = BitList('01000011')
        self.assertEqual(b.decode(), 'C')

    def test_decode_utf8_error_continuation_byte(self):
        b = BitList('11110000000111111001100010000010')
        with self.assertRaises(DecodeError):
            b.decode('utf-8')

    def test_decode_utf8_error_leading_byte(self):
        b = BitList('10000011')
        with self.assertRaises(DecodeError):
            b.decode('utf-8')
    
    def test_decode_invalid_encoding_name(self):
        b = BitList('1111000010011111100110001000001')
        with self.assertRaises(ValueError):
            b.decode('foo')

    def test_chunk(self):
        b = BitList('01000011')
        self.assertEqual(b.chunk(4), [[0, 1, 0, 0], [0, 0, 1, 1]])

    def test_chunk_error(self):
        b = BitList('010000111')
        with self.assertRaises(ChunkError):
            b.chunk(4)


if __name__ == '__main__':
    unittest.main()
