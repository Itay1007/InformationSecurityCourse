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

    mov ebx, dword ptr [ebp + 8]
    
    # small cases
    cmp ebx, 1
    je fibo_1
    cmp ebx, 0
    je fibo_0
    jl fibo_neg


    # setup values for loop
    mov edx, 0
    mov eax, 1
    mov ecx, 1

    # loop ot find the ebx number
    find_fibo_ebx:
        # store values
        push eax
        inc ecx
        push ecx
        push edx
        # make the power 2
        mul eax
        mov ecx, eax
        pop edx
        # make the power 2
        mov eax, edx
        mul eax
        # sum the powers of 2
        add eax, ecx
        # restore values
        pop ecx
        # compares for finish or iterate over again
        cmp ecx, ebx
        pop edx
        jne find_fibo_ebx
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
    # restore values
     mov esp, ebp
     pop ebp
     ret

