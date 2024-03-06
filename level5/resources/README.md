## Flag5 README: Finding Flag5

After connection on our vm with:
```bash
ssh level5@localhost -p 4242
```
We finded a binary program called level5.

```C
void o(void)

{
  system("/bin/sh");
                    // WARNING: Subroutine does not return
  _exit(1);
}



void n(void)

{
  char local_20c [520];

  fgets(local_20c,0x200,stdin);
  printf(local_20c);
                    // WARNING: Subroutine does not return
  exit(1);
}



void main(void)

{
  n();
  return;
}
```
If we decompile it we understand that one again we have to do a printf exploit. and mananging to modify the value of the adress of the jump inside exit(called a got exploit) and change it to the adress of the function call o with the %n exploit.

See script.py to understand the exploit technically.
