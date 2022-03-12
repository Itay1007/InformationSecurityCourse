# for each line
# do an f_write
# after this do a read of the first byte and of the second byte.
# check if it equals to the values of "!#"
# if not remain the same
# else do a system() system call to execute the line

# jump to fgets and to deadzone that return here
mov ebx, 0x8048662
jmp ebx

# opcodes of subeng line "#!"
mov dl, [eax]
mov dh, [eax + 1]
# compare the first 2 bytes in the sentence to a subeng line
mov bx, 0x2123
cmp dx, bx
# continue to the unpatched code of the printf
jne 0x6D

# execute command in shell using system
lea eax, [ebp - 0x40C]
# skip the sabeng
add eax, 2
push eax
mov ebx, 0x8048460
call ebx 
add esp, 4
# jmp to the end of the printf
mov ebx, 0x8048651
jmp ebx
