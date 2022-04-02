from infosec.core import assemble

with open("libc.bin", "rb") as reader:
    opcode = reader.read(2)
    while opcode:
        op = assemble.assemble_data("pop [ebx]")
        if op == opcode:
            print("found")
            break
        print("Not found")
        opcode = reader.read(2)

