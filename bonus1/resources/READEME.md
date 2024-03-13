## Flag Bonus1 README: Finding Flag Bonus1


After connection on our vm with:
```bash
ssh bonus1@localhost -p 4343
```

We found a binary named bonus1. When we run it we obtain:
```sh
bonus1@RainFall:~$ ./bonus1 
Segmentation fault (core dumped)
bonus1@RainFall:~$
```

Okay next step, decompile this program in order to understand what's the purpose and how to exploit it.

As you can see in our file [source](../source), the program takes two arguments.
It copies len_to_copy * 4 byte of second arguments into dest. If the len_to_copy is equal to 1464814662, it will run a shell. But the problem is if len_to_copy is bigger then 9, program will exit. So we need to bypass this condition.

Okay, we have our receipe, now let's cook.

The idea is to do an `overflow` of int with atoi to have something smaller then 9 but with overflow it help us to write enought for a `bufferoverflow` on dest.

After few tries, we find our number `-2147483628`. 

Since we need len_to_copy equal to `1464814662`, we will rewrite his value (with our bufferoverflow) to `574F4C46`.

We all saw that we needed to write `40 bytes` to rewrite the value of len_to_copy.

Let build our payload then.

```sh
./bonus1 `python -c 'print("-2147483628" + " " + "\x90"*40 + "\x46\x4C\x4F\x57")'`
```
