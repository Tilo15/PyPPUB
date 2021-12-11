from PyPPUB import ppub
from PyPPUB import word_tree
import struct

class PpixBuilder:

    def __init__(self):
        self.words = {}
        self.collections = []
        self.tags = {}
        self.pubs = []

        self.word_tree = word_tree.WordBit()

    def add_publication(self, path, pub: ppub.Ppub):
        index = len(self.pubs)
        self.pubs.append((path, pub))

        pub_tags = pub.metadata.get_value("tags")
        if (pub_tags != None):
            for tag in pub_tags.split(" "):
                if(tag in self.tags):
                    self.collections[self.tags[tag]].add(index)
                else:
                    collection_index = len(self.collections)
                    self.collections.append(set([index,]))
                    self.tags[tag] = collection_index
        
        words = set()
        def add_to_set(word_soup):
            if(word_soup == None):
                return

            stripped = "".join((x if x.isalnum() else " ") for x in word_soup)
            for word in stripped.split(" "):
                words.add(word.lower())

        add_to_set(pub.metadata.get_value("title"))
        add_to_set(pub.metadata.get_value("description"))
        add_to_set(pub.metadata.get_value("author"))
        add_to_set(pub.get_asset_data(pub.default_asset).decode('utf-8').replace("\n", " "))
        words.remove("")
        print(words)

        for word in words:
            if(word in self.words):
                    self.collections[self.words[word]].add(index)
            else:
                collection_index = len(self.collections)
                self.collections.append(set([index,]))
                self.words[word] = collection_index


    def write_out(self, stream):
        # Magic number
        stream.write(b"PPIX\x00")
        start = 21

        publication_index_start = start
        publication_index = self.serialise_publication_index(start)
        start += len(publication_index)

        collection_index_start = start
        collection_index = self.serialise_collections(start)
        start += len(collection_index)

        tag_index_start = start
        tag_index = self.serialise_tags()
        start += len(tag_index)

        stream.write(struct.pack("<IIII", publication_index_start, collection_index_start, tag_index_start, start))
        stream.write(publication_index)
        stream.write(collection_index)
        stream.write(tag_index)
        
        self.serialise_word_tree(start, stream)
        stream.flush()
        stream.close()


    def serialise_publication_index(self, start_position):
        data = struct.pack("<I", len(self.pubs))
        string_data_start = start_position + 4 + (len(self.pubs) * 6)
        string_data = b""

        for pub in self.pubs:
            encoded = pub[0].encode('utf-8')
            data += struct.pack("<IH", string_data_start + len(string_data), len(encoded))
            string_data += encoded
        
        return data + string_data

    def serialise_collections(self, start_position):
        index_data = b""
        collection_data_start = start_position + (len(self.collections) * 6)
        collection_data = b""

        for col in self.collections:
            index_data += struct.pack("<IH", collection_data_start + len(collection_data), len(col))
            for pub_id in col:
                collection_data += struct.pack("<I", pub_id)

        
        return index_data + collection_data

    def serialise_tags(self):
        data = struct.pack("<H", len(self.tags))

        for key, value in self.tags.items():
            encoded = key.encode("utf-8")
            data += struct.pack("<BI", len(encoded), value)
            data += encoded

        return data

    def serialise_word_tree(self, start_position, stream):
        words = sorted(((self.string_to_bool_array(k), v) for k, v in self.words.items()), key=lambda x: x[0][0])
        root = word_tree.WordBit()
        nodes = {"": root}

        for word in words:
            last_bit = None
            for i in range(len(word[0][0])):
                key = word[0][0][:i+1]
                if(key in nodes):
                    last_bit = key
                    continue

                last_bit = word_tree.WordBit()
                past_key = word[0][0][:i]
                if(word[0][1][i]):
                    nodes[past_key].next_1 = last_bit
                else:
                    nodes[past_key].next_0 = last_bit
                nodes[key] = last_bit
        
            last_bit.collection = word[1]

        root.position = start_position
        node_array = [root,]
        del nodes[""]

        counter = root.position + word_tree.WordBit.SIZE
        for node in nodes.values():
            node.position = counter
            node_array.append(node)
            counter += word_tree.WordBit.SIZE

        for node in node_array:
            stream.write(node.serialise())
        

    def string_to_bool_array(self, string):
        data = string.encode("utf-8")
        array = []
        for byte in data:
            for i in [1,2,4,8,16,32,64,128]:
                array.append(byte & i == i)

        return ("".join(("1" if x else "0" for x in array)), array)



if(__name__ == "__main__"):
    a = PpixBuilder()
    import glob
    paths = glob.glob("ppubs/*.ppub")
    for path in paths:
        a.add_publication(path.split("/")[-1], ppub.Ppub.from_stream(open(path, 'rb')))

    f = open("lib.ppix", 'wb')
    a.write_out(f)

    import ppix
    f = open("lib.ppix", 'rb')
    ix = ppix.Ppix(f)
    print("{} publication(s)".format(ix.get_publications_count()))
    print("{} tag(s)".format(ix.get_tags_count()))
    for tag in ix.get_tags():
        print(tag);
    word = "ethics"
    col = ix.find_word_matches(word)
    if(col != None):
        print("The following publications contain the word '{}'".format(word))
        for pub_id in ix.get_collection_by_id(col):
            print(ix.get_publication_by_id(pub_id))
    