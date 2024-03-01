from sys import argv
def litteEndian(line):
    n = 2
    newstr = []
    little =""
    for i in range(2, len(line), n):
        newstr.append(line[i:i +n])
    for string in newstr[::-1]:
        little += "\\x" + string
    print(little)


print("Wich adress would you like to transform?: ", end="")
line = input()
litteEndian(line)