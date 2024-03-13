## Flag5 README: Finding Flag5

After connection on our vm with:
```bash
ssh level5@localhost -p 4242
```
We finded a binary program called level5.

If we decompile it we understand that one again we have to do a printf exploit. and mananging to modify the value of the adress of the jump inside exit(called a got exploit) and change it to the adress of the function call o with the %n exploit.

See script.py to understand the exploit technically.
