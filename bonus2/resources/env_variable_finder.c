#include <stdlib.h>

int main()
{
	printf("Address of our env-variable: %p\n", getenv("shellcode"));
}