from PyPPUB import asset

class AssetIndex:

    def __init__(self):
        self.__assets = {}
        self.__assets_ordered = []
    
    def has_asset(self, path):
        return path in self.__assets

    def get_asset(self, path):
        return self.__assets[path]

    def add_asset(self, asset):
        self.__assets_ordered.append(asset)
        self.__assets[asset.path] = asset

    def get_nth_asset(self, n):
        return self.__assets_ordered[n]

    def asset_count(self):
        return len(self.__assets_ordered)

    @staticmethod
    def from_string(string):
        lines = string.split("\n")[:-1]
        assets_ordered = [asset.Asset.from_string(x) for x in lines]
        assets = {x.path: x for x in assets_ordered}
        index = AssetIndex()
        index.__assets_ordered = assets_ordered
        index.__assets = assets
        return index

    def __str__(self) -> str:
        return str.join("\n", (str(x) for x in self.__assets_ordered)) + "\n"
