import sys
from PyPPUB import ppub_builder
from PyPPUB import mimetypes
import datetime

builder = ppub_builder.PpubBuilder()

def set_if_not_empty(field, question):
    answer = input(question)
    if(answer == ""):
        return
    builder.metadata.set_value(field, answer)

set_if_not_empty("title", "[Metadata] Title? ")
set_if_not_empty("tags", "[Metadata] Tags? ")
set_if_not_empty("description", "[Metadata] Description? ")
set_if_not_empty("author", "[Metadata] Author? ")
set_if_not_empty("copyright", "[Metadata] Copyright? ")
set_if_not_empty("licence", "[Metadata] Licence? ")
builder.metadata.set_value("date", datetime.datetime.now().astimezone().isoformat())

for arg in sys.argv[1:]:
    print("Adding %s" % arg)
    f = open(arg, 'rb')
    builder.add_asset(arg, mimetypes.guess_type(arg)[0], f.read())
    f.close()

print("Writing output")
f = open("output.ppub", 'wb')
builder.write_to_stream(f)
f.close()
print("Complete")

import ppub

print("Reading")

f = open("output.ppub", 'rb')
pub = ppub.Ppub.from_stream(f)
for i in range(pub.asset_index.asset_count()):
    asset = pub.asset_index.get_nth_asset(i)
    print("Extracting asset %s" % asset.path)
    of = open("asset_%i" % i, 'wb')
    of.write(pub.get_asset_data(asset))
    of.close()

print("Done")