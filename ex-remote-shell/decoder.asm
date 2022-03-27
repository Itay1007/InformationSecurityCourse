push 0x100
pop ebx
dec ebx
xor byte ptr [eax + 0], bl
push 0x100
pop ebx
dec ebx
xor byte ptr [eax + 1], bl
push 0x100
pop ebx
dec ebx
xor byte ptr [eax + 6], bl
push 0x100
pop ebx
dec ebx
xor byte ptr [eax + 127], bl
