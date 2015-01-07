BITS 32

section .data:

msg: db `Hello, World!\n\0`

section .text:

extern printf

global main
main:
    ; prologue
    push ebp
    mov ebp, esp
    ; call printf
    push msg
    call printf
    add esp, 4
    ; return 0
    mov eax, 0
    ; epilogue
    mov esp, ebp
    pop ebp
    ret

