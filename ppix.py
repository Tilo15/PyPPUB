import struct
import typing

class Ppix:

    def __init__(self, stream):
        self.__stream = stream
        stream.seek(0)
        if(stream.read(5) != b"PPIX\x00"):
            raise Exception("Stream does not begin with PPIX magic number")

        self.__publication_index_location, self.__collection_index_location, self.__tag_index_location, self.__word_tree_root_location = struct.unpack("<IIII", stream.read(16))

    def get_publications_count(self) -> int:
        self.__stream.seek(self.__publication_index_location)
        return struct.unpack("<I", self.__stream.read(4))[0]

    def get_publication_by_id(self, id) -> str:
        position = self.__publication_index_location + 4 + (id * 6)
        self.__stream.seek(position)
        string_location, string_length = struct.unpack("<IH", self.__stream.read(6))
        self.__stream.seek(string_location)
        return self.__stream.read(string_length).decode("utf-8")

    def get_collection_by_id(self, id) -> typing.List[int]:
        position = self.__collection_index_location + (id * 6)
        self.__stream.seek(position)
        collection_location, collection_item_count = struct.unpack("<IH", self.__stream.read(6))
        self.__stream.seek(collection_location)
        return struct.unpack("<{}".format("I"*collection_item_count), self.__stream.read(collection_item_count * 4))

    def get_tags_count(self) -> int:
        self.__stream.seek(self.__tag_index_location)
        return struct.unpack("<H", self.__stream.read(2))[0]

    def get_tags(self):
        count = self.get_tags_count()
        for i in range(count):
            tag_string_length, collection_id = struct.unpack("<BI", self.__stream.read(5))
            yield (self.__stream.read(tag_string_length).decode('utf-8'), collection_id)

    def find_word_matches(self, word):
        node = self.__get_word_node_from_string(word)
        return node[2] if node != None else None
        
    def __get_word_node_from_string(self, word):
        bin_string = self.__string_to_bin(word)
        node = self.__read_tree_node(self.__word_tree_root_location)

        for bit in bin_string:
            if(bit == "0" and node[0] != 0):
                node = self.__read_tree_node(node[0])
            elif(bit == "1" and node[1] != 0):
                node = self.__read_tree_node(node[1])
            else:
                return None
    
        return node

    def __read_tree_node(self, position):
        self.__stream.seek(position)
        c0, has_col, col, c1 = struct.unpack("<IBII", self.__stream.read(13))
        if(has_col != 255):
            col == None

        return (c0, c1, col)

    def __string_to_bin(self, string):
        data = string.encode("utf-8")
        array = []
        for byte in data:
            for i in [1,2,4,8,16,32,64,128]:
                array.append(byte & i == i)

        return "".join(("1" if x else "0" for x in array))