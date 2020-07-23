import os
import zlib

def size_check(file):
    s = os.stat(file)
    return s.st_size
        

def crc_check(file):
    with open(file, "rb") as f:
        sum = (zlib.crc32(f.read()))

    return f"{sum:08X}"

def list_rel(path):
    """
    Return a list of all files in the directory
    and remove "./" from beginning of
    files in dirs to match srrdb output
    """

    res = {"files": []}

    for root, dirs, files in os.walk("."):
        for name in files:
            # Ignore srt files
            if name.endswith(".srt"):
                continue
            if root == ".":
                name = name
            else:
                name = os.path.join(root[2:], name)

            res["files"].append({"name": name})
    return res

if __name__ == "__main__":
    path = ""
    os.chdir(path)
    files = list_rel(path)
    print(files)

