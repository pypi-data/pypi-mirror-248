
import sys
import json

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def printColumns(data, cols=3):
    # Iterate through the list in steps of 3
    for i in range(0, len(data), cols):
        # Extract up to three elements
        elements = data[i:i+cols]
        # Print elements in one line, formatted as columns
        if len(elements) < cols:
            elements += [""] * (cols - len(elements))
        fstring = ["{:<20}"] * cols
        print("\t\t".join(fstring).format(*elements))

def addMetadata(path, text):
    """Add Exif metadata to png file (path)"""
    from PIL import Image
    from PIL.ExifTags import TAGS
    img = Image.open(path)
    exifdata = img.getexif()
    if exifdata is None:
        exifdata = {}
    exifdata[270] = text
    img.save(path, exif=exifdata)


def sanitizeName(name):
    """
    Sanitize the name of the conversation to be saved."""
    return name.replace(" ", "_").replace("/", "_")

def load_json(file):
    """
    Load json from file"""
    with open(file, "r") as f:
        try:
            return json.load(f)
        except:
            return dict()

def strToValue(val):
    if val == "true":
        val = True
    elif val == "false":
        val = False
    elif val.isnumeric():
        val = int(val)
    elif val.replace(".","",1).isnumeric():
        val = float(val)
    return val