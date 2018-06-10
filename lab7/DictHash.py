from pprint import pprint

class DictHash:

    def __init__(self):
        self.dict = {}

    def store(self, key, value):
        self.key = key
        self.value = value
        self.dict[key] = self.value

    def __getitem__(self, key): 
        return self.dict[key]

    def __contains__(self, key):
        if key in self.dict:
            return True
        else:
            return False 

dictionary = DictHash()
songs = open("unique_tracks.txt", "r")
for song in songs:
    song = song.strip("\n")
    song = song.split("<SEP>")
    key = song[0]
    data = [song[1], song[2], song[3]]
    dictionary.store(key, data)

print(len(dictionary.dict))

print("Hanging on the Telephone finns här: TRWYAPY128F145BFC5")
blondie = dictionary.__getitem__("TRWYAPY128F145BFC5")
pprint(blondie)




    # TRWYAPY128F145BFC5<SEP>SODLTNM12A6D4F7F49<SEP>Blondie<SEP>Hanging On The Telephone