## Flag0 README: Finding Flag0

After connection on our vm with:
```bash
ssh level0@localhost -p 4242
```
We finded a binary program called level0.
First thing we decide to do is decompile it with GDB.
In doing so we saw there was a comparason between our argument and a number in hex : **0x1a7** (cf: [disas line 10](disas.a)).

**0x1a7** is 423 in decimal. So we tryed to run **./level0** with 423 as argument. It worked. We are now in `/bin/sh` runned with level1 rights. We going into `/home/user/level1`.

We cat the `.pass` file and obtain our first flag !!
