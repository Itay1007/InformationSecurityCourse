# Declare the assembly flavor to use the intel syntax.
.intel_syntax noprefix

# Define a symbol to be exported from this file.
.global my_function

# Declare symbol type to be a function.
.type my_function, @function

# Code follows below.

my_function:
    # This code reads the first argument from the stack into EBX.
    # (If you need, feel free to edit/remove this line).
    MOV EBX, DWORD PTR [ESP + 4]

    # initialize
    mov ecx, 0
    cmp ebx, 1
    # jump of than 1 as said in the algorithm
    jl finished_without_finding

    # looping until we reach in ecx the bigger root number of a 32 bit signed integer
    repeat:
        mov eax, ecx
        mul ecx
        # check if we found the root
        cmp eax, ebx
        je finished_found
        # check to finish the looping for too big counter
        cmp ecx, ebx
        je finished_without_finding
        cmp ecx, 46340
        je finished_without_finding
        # increment the counter and loop again
        inc ecx
        jmp repeat

finished_found:
    mov eax, ecx
    jmp end
finished_without_finding:
    mov eax, 0
end:
    RET

