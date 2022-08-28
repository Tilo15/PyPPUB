

class FileEntry:
    def __init__(self, type, label, filename, meta):
        self.type = type
        self.filename = filename
        self.label = label
        self.metadata = meta

    @staticmethod
    def from_string(string):
        parts = string.split(":", 2)
        type = parts[0]
        parts = parts[1].split(",", 3)
        label = parts[0].strip()
        filename = parts[1].strip()
        
        meta = {}
        for property in parts[2].split("\";"):
            if(property == ""):
                continue
            data = property.split("=\"")
            meta[data[0].strip()] = data[1].strip()

        return FileEntry(type, label, filename, meta)

    def __str__(self) -> str:
        meta = ""
        for key in self.metadata:
            meta += " {}=\"{}\";".format(key, self.metadata[key])
        
        return "{}: {}, {},{}".format(self.type, self.label, self.filename, meta)

class Ppvm:

    def __init__(self, files, metadata):
        self.files = files
        self.metadata = metadata

    @staticmethod
    def from_string(string: str):
        lines = string.split("\n")
        if lines[0] != "PPVM":
            raise Exception("Not a PPVM string")

        line_count = 1
        metadata = {}
        while True:
            line = lines[line_count]
            line_count += 1
            if(line == ""):
                break

            parts = line.split(":", 2)
            metadata[parts[0]] = parts[1].strip()

        entries = []
        while len(lines) > line_count:
            line = lines[line_count]
            line_count += 1
            if(line == ""):
                continue
            entries.append(FileEntry.from_string(line))

        return Ppvm(entries, metadata)
        

    def __str__(self) -> str:
        string = "PPVM\n"
        for key in self.metadata:
            string += "{}: {}\n".format(key, self.metadata[key])

        string += "\n"

        for file in self.files:
            string += "{}\n".format(file)

        string += "\n"
        return string
