from PyPPUB.asset_index import AssetIndex
from PyPPUB.metadata import Metadata
import gzip

class Ppub:

    def __init__(self):
        self.metadata = None
        self.asset_index = None
        self.default_asset = None
        self.__stream = None
        self.__blob_start = 0
        self.__flag_handlers = {
            "gzip": lambda x: gzip.decompress(x)
        }

    @staticmethod
    def from_stream(stream):
        if (stream.read(5) != b"ppub\n"):
            raise Exception("Stream did not start with magic number")

        index_length_bytes = b""
        next_byte = b""
        while(next_byte != b"\n"):
            index_length_bytes += next_byte
            next_byte = stream.read(1)

        index_length = int(index_length_bytes)
        index_bytes = stream.read(index_length)
        blob_start = len(index_length_bytes) + index_length + 6

        index = AssetIndex.from_string(index_bytes.decode('utf-8'))

        obj = Ppub()
        obj.__stream = stream
        obj.__blob_start = blob_start
        obj.asset_index = index
        obj.metadata = Metadata.from_string(obj.get_asset_data(index.get_asset("metadata")).decode('utf-8'))
        obj.default_asset = index.get_nth_asset(1)
        return obj

    def get_asset_data(self, asset):
        start_location = asset.start_location + self.__blob_start
        length = asset.end_location - asset.start_location
        self.__stream.seek(start_location)
        data = self.__stream.read(length)
        for flag in asset.flags:
            if (flag not in self.__flag_handlers):
                raise Exception("Flag '%s' not understood" % flag)
            data = self.__flag_handlers[flag](data)
        return data

    

