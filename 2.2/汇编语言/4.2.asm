data segment
    string db 20 dup('adaavceagdataaaaqaza') 
data ends
code segment
    assume cs:code, ds:data
start:
    mov ax, data
    mov ds, ax          
    mov si, offset string 
    mov cx, 20          
    xor bx, bx          
;统计a的数量
process_char:
    mov al, [si]        
    cmp al, 'a'         
    jne check_lower     
    inc bl              
;小写字母转大写
check_lower:
    cmp al, 'a'         
    jb next_char        
    cmp al, 'z'         
    ja next_char        
    sub al, 20h      
    mov [si], al        
next_char:
    inc si              
    loop process_char   
;输出
display_string:
    mov si, offset string
    mov cx, 20         
    mov ah, 02h         
print_char:
    mov dl, [si]
    int 21h             
    inc si
    loop print_char
    mov dl, 0Dh         
    int 21h
    mov dl, 0Ah        
    int 21h
;输出a的数量
display_count:
    mov al, bl       
    xor ah, ah     
    mov cl, 10
    div cl            
    test al, al        
    jz  show_unit     
    add al, '0'     
    mov dl, al
    mov ah, 02h
    int 21h             
show_unit:
    mov dl, ah
    add dl, '0'        
    mov ah, 02h
    int 21h            
exit:
    mov ax, 4c00h      
    int 21h
code ends
end start



