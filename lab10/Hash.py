class HashNode():
    def __init__(self, node_key, node_data, next_node=None):
        self.node_key = node_key
        self.node_data = node_data
        self.next_node = next_node

class HashTable():
    def __init__(self, sizeOfHashTable):
        self.sizeOfHashTable = 2*sizeOfHashTable                 #Räcker med att ha 50% av "tom luft"
        self.hashlist = [None]*self.sizeOfHashTable

    def set(self, key, data):#för att sätta in någonting i hashtabellen
        NewNode = HashNode(key,data)
        index = self.hash_funct(key)
        print(index)
        node = self.hashlist[index]

        if node == None:
            self.hashlist[index] = NewNode
        else:
            node.next_node = NewNode


    def get(self, key): #för att hämta någonting ut ur hashtabellen, och då behövs bara nyckeln för få ut värdet eftersom värdet är lagrat i nyckeln
        index = self.hash_funct(key)
        node = self.hashlist[index]
        while node != None:
            if node.node_key == key:
                return node.node_data
            else:
                node = node.next_node
        raise KeyError(key)

    def hash_funct(self,key): #returnera ett index baserat på nyckel
        result = 0  # s[0]*32^[n-1] + s[1]*32^[n-2] + ... + s[n-1]
        for c in key:
            result = result * 32 + ord(c)
        return result%self.sizeOfHashTable

'''
with open("unique_tracks.txt", "r", encoding="utf-8") as tracklist:
    hashtable = HashTable(100000)
    for line in tracklist:
        stripped_lines = line.strip('\n')
        line_lists = stripped_lines.split('<SEP>')
        hashtable.set(line_lists[2], (line_lists[0],line_lists[1], line_lists[3]))

print(hashtable.get('Jully'))
'''
