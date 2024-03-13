## Flag Bonus3 README: Finding Flag Bonus3

Ok this is the last one of this terrible rainfall.
And the good news is the easiest one.
We can see 2 ways of having the flag first one is to have the bash by having strcmp to return 0 (so the sentence be the same)
```C
if ( !strcmp(ptr, argv[1]) )
		execl("/bin/sh", "sh", 0);
```
the second is to try to puts the str that have the .pass save in it :
```C
else
	puts(&ptr[66]);
```

so if we put something a \n is display. so we can believe that we enter in the else because it's the only place something is print to stdout. The reason he is not printing the string we want is that there is not \0 inside our string and puts only the \n.

So let's try to enter in the if now.
```C
ptr[atoi(argv[1])] = 0;
```
here he is adding 0 at the position we give as parametter.
so let's try to put 0. so the strcmp will compare 0 and 0. But it's not true bc argv[1] is a string and 0 in a string is 48.
But if put nothing as the string the \0 and \0 is equal 0 in ascii. let s try this :

```Bash
bonus3@RainFall:~$ ./bonus3 ""
$whoami
end
```
