a ='abcdefghijklmnopqrstuvwxyz'
A = a.upper()
s = ''
print("Enter a nomber of rep: ", end="")
len = int(input())
count = 0
index_a = 0
index_A = 0
for i in range(0, len):
	s+= a[index_a] + A[index_A] + ('0' if count < 10 else '') + str(count)
	count +=1
	if (index_A > 25 and count == 10):
		break
	if (count == 10):
		count = 0
		index_a += 1
	if (index_a > 25):
		print('index_a =', index_a)
		index_a = 0
		index_A += 1
print(s)