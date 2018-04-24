kattis = open('input.txt')

for line in iter(kattis):
    kattis2 = line.split()
    kattis2[0] = int(kattis2[0])
    kattis2[1] = int(kattis2[1])
    absol = abs(kattis2[0]-kattis2[1])
    print(absol)

