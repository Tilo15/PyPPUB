import struct

class WordBit:

    SIZE = 13

    def __init__(self):
        self.next_0 = None
        self.next_1 = None
        self.collection = None
        self.position = 0

    def serialise(self):
        n0 = self.next_0.position if self.next_0 != None else 0
        n1 = self.next_1.position if self.next_1 != None else 0
        col = self.collection if self.collection != None else 0
        has_col = 255 if self.collection != None else 0
        return struct.pack("<IBII", n0, has_col, col, n1)