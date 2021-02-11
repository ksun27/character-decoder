#Kevin Sun
class DecodeError(Exception): pass
class ChunkError(Exception): pass

class BitList(object):
    def __init__(self, s):
        for i in s:
            if i != '0' and i != '1':
                raise ValueError('value BitList string only allows for 0 or 1 in the string')
                return
        self.s = s  
    def __eq__(self, other):
        return self.s == other
    @staticmethod
    def from_ints(*args):
        s2 = ""
        for i in args:
            if i != 0 and i != 1:
                raise ValueError('value BitList string only allows for 0 or 1 in the string')
                return
        for j in args:
            s2 += str(j)
        return BitList(s2)
    def __str__(self):
        return self.s
    def arithmetic_shift_left(self):
        s4 = ""
        x = [int(y) for y in self.s]
        x.pop(0)
        x.append(0)
        for i in x:
            s4 += str(i)
        self.s = s4
    def arithmetic_shift_right(self):
        s5 = ""
        x = [int(y) for y in self.s]
        temp = x[0]
        x.pop()
        x.insert(0, temp)
        for i in x:
            s5 += str(i)
        self.s = s5
    def bitwise_and(self, otherBitList):
        s3 = ""
        if len(self.s) == len(otherBitList.s):
            for i in range(len(self.s)):
                x = int(self.s[i]) * int(otherBitList.s[i])
                s3 += str(x)
            return BitList(s3)
    def chunk(self, chunk_length):
        if len(self.s) % chunk_length != 0:
            raise ChunkError('BitList string is not divisible by chunk length')
            return
        else:
            chunks = [self.s[i:i+chunk_length] for i in range(0, len(self.s), chunk_length)]
            for i in range(len(chunks)):
                chunks[i] = [int(y) for y in chunks[i]]
            return chunks
    def decode(self, encoding='utf-8'):
        bits = ''
        res = ''
        count = (self.s+'0').index('0')
        if encoding == 'us-ascii':
            if len(self.s) > 7:
                x = [self.s[i:i+7] for i in range(0, len(self.s), 7)]
                for i in x:
                    s6 = ''.join(i)
                    codepoint = int(s6, 2)
                    ch = chr(codepoint)
                    res += ch
                return res
            else:    
                codepoint = int(self.s, 2)
                ch = chr(codepoint)
                return ch
        elif encoding == 'utf-8':
            if len(self.s) > 32:
                q = [self.s[i:i+32] for i in range(0, len(self.s), 32)]
                for u in q:
                    bits = ''
                    count = (u+'0').index('0')
                    if u[:2] == "10":
                        raise DecodeError('invalid leading byte')
                    else:
                        if len(u) / count != 8:
                            raise DecodeError('invalid bits')
                        else:
                            x = [u[i:i+8] for i in range(0, len(u), 8)]
                            for k in range(1, len(x)):
                                if x[k][:2] != '10':
                                    raise DecodeError('invalid bits')
                            bits += x[0][count:]
                            for j in range(1, len(x)):
                                bits += x[j][2:]
                            codepoint = int(bits, 2)
                            ch = chr(codepoint)
                            res += ch
                return res
            else:
                if self.s[:2] == "10":
                    raise DecodeError('invalid leading byte')
                elif count == 0 and len(self.s) == 8:
                    bits = self.s
                else:
                    if len(self.s) / count != 8:
                        raise DecodeError('invalid bits')
                    else:
                        x = [self.s[i:i+8] for i in range(0, len(self.s), 8)]
                        for k in range(1, len(x)):
                            if x[k][:2] != '10':
                                raise DecodeError('invalid bits')
                        bits += x[0][count:]
                        for j in range(1, len(x)):
                            bits += x[j][2:]
                codepoint = int(bits, 2)
                ch = chr(codepoint)
                return ch
        else:
            raise ValueError('encoding is not supported')