import pprint

def playlist_transformation(s,t,compareType = "song"):
    print("Comparing playlist similarity by ", end="")
    if compareType == "song":
        print(compareType)
        offset = 0
    elif compareType == "artist":
        print(compareType)
        offset = 1
    elif compareType == "genre":
        print(compareType)
        offet = 2
    lt = [[-1] * (len(a)+1) for i in range(len(b)+1)] #lookup table
    sourcelt = dict() #0 for horizontal, 1 for diagonal, 2 for vertical

    for i in range(0, len(lt[0])):
        lt[0][i] = i
        sourcelt[(i, 0)] = (2, True)
    for i in range(0, len(lt)):
        lt[i][0] = i
        sourcelt[(0, i)] = (0, True)

    for i in range(1, len(lt)):
        for x in range(1, len(lt[i])):
            if (a[x-1][offset] != b[i-1][offset]):
                lt[i][x] = min(lt[i-1][x], lt[i-1][x-1], lt[i][x-1]) + 1
                if lt[i][x]-1 == lt[i-1][x-1]:
                    sourcelt[(i,x)] = (1, True)
                elif lt[i][x]-1 == lt[i][x-1]:
                    sourcelt[(i,x)] = (2, True)
                elif lt[i][x]-1 == lt[i-1][x]:
                    sourcelt[(i,x)] = (0, True)
            else:
                lt[i][x] = lt[i-1][x-1]
                sourcelt[(i,x)] = (1, False)
    return lt, sourcelt

def findPath(x,y,lt,sourcelt, a, b):
    ret = []
    while(x >= 0 and y >= 0 and not (y == 0 and x == 0)):
        val = sourcelt[(int(y),int(x))]
     #   print(x, " ", y)
        if val[0] == 0:
            ret.append("Delete " + str(a[x]))
            x = x-1
        elif val[0] == 1:
            if val[1]:
                ret.append("Replace " + str(a[x]) + " with " + str(b[y]))
            else:
                ret.append("Leave " + str(a[x]) + " unchanged")
            x = x - 1
            y = y - 1
        elif val[0] == 2:
            ret.append("Insert " + str(a[x]))
            y = y - 1
    return ret

p1Name = input("Enter playlist 1 filename:")
p2Name = input("Enter playlist 2 filename:")
    
p1Stream = open(p1Name, 'r')

a = []
i = 0
for line in p1Stream:
    a.append(line.split(','))
    a[i][2] = a[i][2].rstrip()
    i = i + 1
p1Stream.close()

p2Stream = open(p2Name, 'r')
b = []
i = 0
for line in p2Stream:
    b.append(line.split(','))
    b[i][2] = b[i][2].rstrip()
    i = i + 1
p2Stream.close()


compBy = input("Enter basis of comparison (song, artist, genre):")

while(compBy != "song" and compBy != "artist" and compBy != "genre"):
    compBy = input("Enter basis of comparison (song, artist, genre):")

transformed = playlist_transformation(a,b,compBy)

#pprint.pprint(transformed[0])

pth = findPath(len(a)-1, len(b)-1, transformed[0], transformed[1], a, b)

for i in range (0, len(pth)):
    x = len(pth)-1 - i
    print(pth[x], "\n")
