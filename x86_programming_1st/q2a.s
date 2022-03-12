# Declare the assembly flavor to use the intel syntax.
.intel_syntax noprefix

# Define a symbol to be exported from this file.
.global my_function

# Declare symbol type to be a function.
.type my_function, @function

# Code follows below.

my_function:
    # store values
    push ebp
    mov ebp, esp
    
    push ebx
    push edx
    
    mov ebx, dword ptr [ebp + 8]
    # small cases
    cmp ebx, 1
    je fibo_1
    
    cmp ebx, 0
    je fibo_0
    jl fibo_neg
    
    # recursion step
    dec ebx
    push ebx
    call my_function
    add esp, 4

    # power 2
    mul eax
    mov edx, eax
    
    # recursion step
    dec ebx
    push ebx
    call my_function
    add esp, 4
   
    # power 2
    push edx
    mul eax
    pop edx
    # sum the powers of 2
    add eax, edx
    jmp end    

# small cases
fibo_1:
    mov eax, 1
    jmp end
fibo_0:
    mov eax, 0
    jmp end
fibo_neg:
    mov eax, 0

end:
    # restore values and return
    pop edx
    pop ebx
    mov esp, ebp
    pop ebp
    ret

