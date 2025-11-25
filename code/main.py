import json
import sys
import hashlib

# Examples:
#
# - decode_bencode(b"5:hello") -> [b"hello",b""]
# - decode_bencode(b"10:hello12345") -> [b"hello12345",b""]
# will return a list where index 0 is decoded value and 1 is rest of the input
def decode_bencode(bencoded_value):

    #decodes string of length defined by start digits
    if chr(bencoded_value[0]).isdigit():
        first_colon_index = bencoded_value.find(b":")
        string_length = int(bencoded_value[0:first_colon_index])
        if first_colon_index == -1:
            raise ValueError("Invalid encoded value")
        string_start = first_colon_index + 1
        return bencoded_value[string_start:string_start+string_length], bencoded_value[string_start+string_length:]
    
    #decodes for an integer
    elif bencoded_value.startswith(b"i"):
        end = bencoded_value.index(b"e")
        return int(bencoded_value[1:end]), bencoded_value[end+1:]
    
    #decodes a list by calling itself
    elif bencoded_value.startswith(b"l"):
        bencoded_value = bencoded_value[1:]
        outlist = []
        while not bencoded_value.startswith(b"e"):
            item, bencoded_value = decode_bencode(bencoded_value)
            outlist.append(item)
        return outlist, bencoded_value[1:]
    
    #decodes dictionary
    elif bencoded_value.startswith(b"d"):
        result = {}
        rest = bencoded_value[1:]
        while chr(rest[0]) != "e":
            try:
                key, rest = decode_bencode(rest)
                value, rest = decode_bencode(rest)
            except ValueError as ex:
                raise ValueError(
                    "Invalid encoded value; dictionary could not be parsed"
                ) from ex
            else:
                result[key.decode()] = value

        #returns a dictionary sorted lexicographically by key
        return dict(sorted(result.items())), rest[1:]

    else:
        raise NotImplementedError("Not supported data type")

def bencode_any(i):
    if isinstance(i,bytes):
        return bencode_str(i)
    if isinstance(i,int):
        return bencode_int(i)
    elif isinstance(i,str):
        return bencode_str(bytes(i,"utf-8"))
    elif isinstance(i,dict):
        return bencode_dict(i)
    elif isinstance(i,list):
        return bencode_list(i)

def bencode_str(value):
    l = len(value)
    return bytes(str(l), "utf-8") + b":" + value

def bencode_int(value):
    return ("i"+str(value)+"e").encode()

def bencode_list(value):
    result = b"l"
    for i in value:
        result += bencode_any(i)
    return result+b"e"

def bencode_dict(value):
    value = dict(sorted(value.items()))
    result = b"d"
    for key in value:
        result += bencode_any(key)
        result += bencode_any(value[key])
    return result+b"e"

# json.dumps() can't handle bytes, but bencoded "strings" need to be
# bytestrings since they might contain non utf-8 characters.
#
# Let's convert them to strings for printing to the console.
def bytes_to_str(data):
            if isinstance(data, bytes):
                return data.decode()

            raise TypeError(f"Type not serializable: {type(data)}")

def main():
    command = sys.argv[1]

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if command == "decode":
        bencoded_value = sys.argv[2].encode()

        final = decode_bencode(bencoded_value)[0]
        print(json.dumps(final, default=bytes_to_str))
    
    elif command == "info":
        file_name = sys.argv[2]

        try:
            with open(file_name,"rb") as file:
                contents = decode_bencode(file.read())[0]
        except FileNotFoundError:
            raise Exception("File not found")

        try:
            URL = contents["announce"]
        except KeyError:
            URL = b"No found URL"
        
        #try for multi or single file
        try:
            length = contents["info"]["files"][0]["length"]
        except KeyError:
            length = contents["info"]["length"]


        info_hash = hashlib.sha1(bencode_dict(contents["info"])).hexdigest()
        piece_length = contents["info"]["piece length"]
        concat_pieces = contents["info"]["pieces"].hex()
        pieces = []

        #splits the concatenated pieces into pieces of length 20 bytes(40 characters as string)
        for i in range(39,len(concat_pieces),39):
            print(i)
            pieces.append(concat_pieces[i-39:i+1])

        #Dictionary of information displayed when info command is run
        info_dict = {
            "URL":          URL,
            "Length":       length,
            "Info Hash":    info_hash,
            "Piece Length": piece_length,
            "Pieces":       pieces
        }

        print(json.dumps(info_dict, default=bytes_to_str, indent=2))

    elif command == "contents":
        file_name = sys.argv[2]

        try:
            with open(file_name,"rb") as file:
                contents = decode_bencode(file.read())[0]
        except FileNotFoundError:
            raise Exception("File not found")
        
        print(contents)
    else:
        raise NotImplementedError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
