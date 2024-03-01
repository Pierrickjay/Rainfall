A ='abcdefghijklmnopqrstuvwxyz'
s = ''
for i in range(0, len(A)*2):
	s += (A[i%26] if i < 26 else A[i%26].upper()) + ('0' if i < 10 else '') + str((i%26+1))
print(s)