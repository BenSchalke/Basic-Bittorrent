import json
import sys

# import bencodepy - available if you need it!
# import requests - available if you need it!

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

        with open(file_name,"rb") as file:
            contents = decode_bencode(file.read())[0]

        URL = contents["announce"]
        try:
            length = contents["info"]["files"][0]["length"] #all sorts of nested dictionary and list fuckery
        except KeyError:
            length = contents["info"]["length"]

        print("URL:",end="\t")
        print(json.dumps(URL, default=bytes_to_str))
        print("Length:",end="\t")
        print(json.dumps(length, default=bytes_to_str))
    else:
        raise NotImplementedError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
