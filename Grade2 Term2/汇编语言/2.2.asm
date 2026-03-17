DATAS SEGMENT
X    dw 1111h, 2222h  
Y    dw 8888h, 9999h  
Z    dw 6666h, 7777h  
W    dw 2 dup(0)      
DATAS ENDS

CODES SEGMENT
    ASSUME CS:CODES,DS:DATAS
START:
	MOV AX,DATAS
	MOV DS,AX

    mov ax, [Y]    ;8888
    mov dx, [Y+2]  ;9999
    sub ax, [Z]    ;8888-6666
    sub dx, [Z+2]  ;9999-7777
    add ax, [X]    ;2222+1111
    add dx, [X+2]  ;2222+2222
    mov [W], ax    ;3333
    mov [W+2], dx  ;4444

    MOV AH,4CH
    INT 21H
CODES ENDS
    END START
