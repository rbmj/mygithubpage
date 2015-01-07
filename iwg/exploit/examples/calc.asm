BITS 32

section .data:

instr: db `%i %i\0`
outstr: db `%i + %i = %i\n\0`

section .text:

extern printf
extern scanf

global add:
add:
    push ebp
    mov ebp, esp
    mov eax, [ebp+0x8]
    add eax, [ebp+0xc]
    mov esp, ebp
    pop ebp
    ret

global main
main:
    push ebp
    mov ebp, esp
    ; reserve space for local variables
    sub esp, 0x8
    ; we'll put int a at [ebp-0x4] and int b at [ebp-0x8]
    ; call scanf(instr, &a, &b)
    lea eax, [ebp-0x8]
    push eax
    lea eax, [ebp-0x4]
    push eax
    push instr
    call scanf
    add esp, 0xc
    ; call add(a, b)
    mov eax, [ebp-0x8]
    push eax
    mov eax, [ebp-0x4]
    push eax
    call add
    add esp, 0x8
    ; call printf(outstr, a, b, [return value of add])
    push eax
    mov eax, [ebp-0x8]
    push eax
    mov eax, [ebp-0x4]
    push eax
    push outstr
    call printf
    add esp, 0x10
    ; return
    mov eax, 0
    mov esp, ebp
    pop ebp
    ret

