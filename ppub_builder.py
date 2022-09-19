from io import BytesIO, StringIO
from PyPPUB.asset import Asset
from PyPPUB.asset_index import AssetIndex
from PyPPUB.metadata import Metadata

import gzip

class PpubBuilder:

    def __init__(self):
        self.assets = []
        self.metadata = Metadata()


    def add_asset(self, path, mimetype, data, flags = None, streamable = False):
        self.assets.append(BuilderAsset(path, mimetype, BytesIO(data), flags, streamable))

    def add_asset_stream(self, path, mimetype, stream, flags = None, streamable = False):
        self.assets.append(BuilderAsset(path, mimetype, stream, flags, streamable))

    def write_to_stream(self, stream):
        stream.write(b"ppub\n")
        data_blob = b""
        index = AssetIndex()
        assets = [BuilderAsset("metadata", "application/x-ppub-metadata", BytesIO(str(self.metadata).encode('utf-8'))),] + self.assets
        for builder_asset in assets:
            start_location = len(data_blob)
            asset_data = builder_asset.data.read()
            if(not builder_asset.streamable):
                asset_data_gzip = gzip.compress(asset_data, 9)
                if(len(asset_data) > len(asset_data_gzip)):
                    asset_data = asset_data_gzip
                    builder_asset.flags.append("gzip")
                    
            data_blob += asset_data
            end_location = len(data_blob)
            asset = Asset(builder_asset.path, builder_asset.mimetype, start_location, end_location, builder_asset.flags)
            index.add_asset(asset)
        
        index_data = str(index)
        stream.write(str.format("{}\n", len(index_data)).encode('utf-8'))
        stream.write(index_data.encode('utf-8'))
        stream.write(data_blob)

class BuilderAsset:
    def __init__(self, path, mimetype, data, flags = None, streamable = False):
        self.path = path
        self.mimetype = mimetype
        self.data = data
        self.flags = flags
        self.streamable = streamable
        if(self.flags == None):
            self.flags = []