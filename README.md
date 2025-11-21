# Project purpose
This project is more of a learning experience for myself, it is quite rudementary and not intended for use. I am quite early on in this project but so far I have leanrt alot about bencoding, hashing (specifically the old SHA1 which is what is used to validate files), and git which I previously haven't used extesnively.

I have found this project to be quite enjoyable at the moment, learning new things about data, torrents, and file sharing. I hope to be able to finish soonish and move on to something else as I get back into the flow of things

# Project use
As of now, the python file can be run with specific commands and a torrent file to run the command on I will be adding more capability in future and I have only really built the basics to continue from in future.
## Commands
### decode
- The argument passed after this commanded should be a bencoded value to be decoded into its string, integer, list, or dictionary form (in python).
- Example:
- py main.py decode i605e
- would return 605 as an integer
### info
- This command is used in conjunction with a torrent file, at the moment it will retrieve, decode and display data about the file such as, the URL it has come from, the length of the file in bytes, and the info hash (all data in file hashed through SHA1)
- Example:
- py main.py info sample.torrent
- would return:
- URL:            "udp://tracker.openbittorrent.com:80"
- Length:         20
- Info Hash:      "d0d14c926e6e99761a2fdcff27b403d96376eff6"
