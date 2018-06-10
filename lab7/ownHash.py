from pprint import pprint   

# Huvudprogrammet = key, value
# Hashtabellen = Hashindex, och en vektor med Hashnoder
# Hashnoden = key, value

class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    def __init__(self, size):
        self.size = 2 * size
        self.vector = [None for x in range(self.size)]

    def put(self, key, value):
        Node = HashNode(key, value)
        HashIndex = self.hash(key)
        nodeInVector = self.vector[HashIndex]

        if nodeInVector == None:
            self.vector[HashIndex] = Node
        else:
            while nodeInVector.next is not None:
                nodeInVector = nodeInVector.next
            nodeInVector.next = Node

    def get(self, key):
        HashIndex = self.hash(key)
        if self.vector[HashIndex]:
            Node = self.vector[HashIndex]
        else:
            raise KeyError(key)


        if Node.key == key:
            return Node
        else:
            while Node is not None:
                if Node.key == key:
                    return Node
                else:
                    Node = Node.next
            raise KeyError(key)

    def hash(self, key):
        result = 0
        for character in key:
            result = result * 32 + ord(character)
        return result % self.size

# table = HashTable(100000)
# songs = open("unique_tracks.txt", "r")
# for song in songs:
#     song = song.strip("\n")
#     song = song.split("<SEP>")
#     key = song[0]
#     data = [song[1], song[2], song[3]]
#     table.put(key, data)

# print("Hanging on the Telephone finns på TRWYAPY128F145BFC5")
# blondie = table.get("TRWYAPY128F145BFC5")
# pprint(blondie.value)