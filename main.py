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

    else:
        raise NotImplementedError("Not supported data type")


def main():
    command = sys.argv[1]

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if command == "decode":
        bencoded_value = sys.argv[2].encode()

        # json.dumps() can't handle bytes, but bencoded "strings" need to be
        # bytestrings since they might contain non utf-8 characters.
        #
        # Let's convert them to strings for printing to the console.
        def bytes_to_str(data):
            if isinstance(data, bytes):
                return data.decode()

            raise TypeError(f"Type not serializable: {type(data)}")

        # Uncomment this block to pass the first stage
        print(json.dumps(decode_bencode(bencoded_value), default=bytes_to_str))
    else:
        raise NotImplementedError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
