## Flag4 README: Finding Flag4

We are now into `/home/user/level4`.

After downloading the binary with:
```sh
scp -P 4343 level1@localhost:/home/user/level4/level4 ~
```
and decompile it with [Dogbolt](https://dogbolt.org/).

In doing so, we realized there a function p which calling printf. So we understood that we need to use a `format string bug`. 

What is it ? Simple, we are exploiting printf(s)