assume cs:code, ds:data

data segment
    ; 密码相关
    password       db '12345$'         ; 预设密码
    prompt_pass    db 'Enter password: $'
    error_msg      db 0Dh,0Ah,'Invalid password!$'
    input_pass     db 6               ; 密码输入缓冲区
                  db ?
                  db 6 dup(0)
    
    ; 成绩输入相关
    prompt_score   db 0Dh,0Ah,'Enter score (0-100): $'
    score_input    db 4               ; 成绩输入缓冲区
                  db ?
                  db 4 dup(0)
    
    ; 数据存储
    scores         dw 35 dup(0)       ; 存储成绩
    fail_count     dw 0               ; 不及格人数
    average        dw 0               ; 平均分
    
    ; 显示信息
    rank_header    db 0Dh,0Ah,'Ranking:',0Dh,0Ah,'$'
    fail_header    db 0Dh,0Ah,'Failures: $'
    avg_header     db 0Dh,0Ah,'Average: $'
    newline        db 0Dh,0Ah,'$'
data ends

code segment
start:
    mov ax, data
    mov ds, ax
    
    ; 功能一：密码验证
    call check_password
    
    ; 功能二：输入成绩
    call input_scores
    
    ; 功能三：排序并显示
    call sort_scores
    call display_ranking
    
    ; 功能四：统计并显示不及格人数
    call count_failures
    call display_failures
    
    ; 功能五：计算并显示平均分
    call calculate_average
    call display_average
    
    ; 退出程序
    mov ax, 4c00h
    int 21h

; ----------------------------
; 检查密码
; ----------------------------
check_password proc
    ; 显示提示
    mov ah, 09h
    lea dx, prompt_pass
    int 21h
    
    ; 读取输入
    mov ah, 0Ah
    lea dx, input_pass
    int 21h
    
    ; 检查长度
    cmp byte ptr [input_pass+1], 5
    jne invalid
    
    ; 逐个字符比较
    mov cx, 5
    lea si, password
    lea di, input_pass+2
check_loop:
    mov al, [si]
    cmp al, [di]
    jne invalid
    inc si
    inc di
    loop check_loop
    ret
    
invalid:
    mov ah, 09h
    lea dx, error_msg
    int 21h
    mov ax, 4c00h
    int 21h
check_password endp

; ----------------------------
; 输入所有成绩
; ----------------------------
input_scores proc
    mov cx, 35
    mov si, 0
input_loop:
    call read_score    ; 读取单个成绩
    mov scores[si], ax
    add si, 2
    loop input_loop
    ret
input_scores endp

; ----------------------------
; 读取单个成绩（返回AX）
; ----------------------------
read_score proc
    push bx
    push cx
    
    ; 显示提示
    mov ah, 09h
    lea dx, prompt_score
    int 21h
    
    ; 读取输入
    mov ah, 0Ah
    lea dx, score_input
    int 21h
    
    ; 转换为数字
    xor ax, ax
    mov cl, [score_input+1]
    lea si, score_input+2
convert:
    imul ax, 10
    mov bl, [si]
    sub bl, '0'
    add ax, bx
    inc si
    loop convert
    
    pop cx
    pop bx
    
    ; 换行
    mov ah, 09h
    lea dx, newline
    int 21h
    ret
read_score endp

; ----------------------------
; 冒泡排序（从高到低）
; ----------------------------
sort_scores proc
    mov cx, 34
outer:
    push cx
    mov si, 0
inner:
    mov ax, scores[si]
    cmp ax, scores[si+2]
    jge no_swap
    xchg ax, scores[si+2]
    mov scores[si], ax
no_swap:
    add si, 2
    loop inner
    pop cx
    loop outer
    ret
sort_scores endp

; ----------------------------
; 显示排名
; ----------------------------
display_ranking proc
    mov ah, 09h
    lea dx, rank_header
    int 21h
    
    mov cx, 35
    mov si, 0
disp_loop:
    mov ax, scores[si]
    call print_number
    add si, 2
    loop disp_loop
    ret
display_ranking endp

; ----------------------------
; 统计不及格人数
; ----------------------------
count_failures proc
    mov cx, 35
    mov si, 0
    mov dx, 0
fail_loop:
    cmp scores[si], 60
    jge pass
    inc dx
pass:
    add si, 2
    loop fail_loop
    mov fail_count, dx
    ret
count_failures endp

; ----------------------------
; 显示不及格人数
; ----------------------------
display_failures proc
    mov ah, 09h
    lea dx, fail_header
    int 21h
    mov ax, fail_count
    call print_number
    ret
display_failures endp

; ----------------------------
; 计算平均分
; ----------------------------
calculate_average proc
    mov cx, 35
    mov si, 0
    xor ax, ax
sum_loop:
    add ax, scores[si]
    add si, 2
    loop sum_loop
    xor dx, dx
    mov bx, 35
    div bx
    mov average, ax
    ret
calculate_average endp

; ----------------------------
; 显示平均分
; ----------------------------
display_average proc
    mov ah, 09h
    lea dx, avg_header
    int 21h
    mov ax, average
    call print_number
    ret
display_average endp

; ----------------------------
; 打印数字（AX中的数值）
; ----------------------------
print_number proc
    push ax
    push bx
    push cx
    push dx
    
    ; 处理0的特殊情况
    cmp ax, 0
    jne convert
    mov dl, '0'
    mov ah, 02h
    int 21h
    jmp end_print
    
convert:
    mov bx, 10
    xor cx, cx
    
divide:
    xor dx, dx
    div bx
    push dx
    inc cx
    test ax, ax
    jnz divide
    
print:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop print
    
end_print:
    ; 换行
    mov ah, 09h
    lea dx, newline
    int 21h
    
    pop dx
    pop cx
    pop bx
    pop ax
    ret
print_number endp

code ends
end start
