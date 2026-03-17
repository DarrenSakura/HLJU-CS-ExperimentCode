DATAS SEGMENT
	X   dw -13         
	Y   dw 30          
	Z   dw 24         
	W	dw 50          
	result	dw 0           
DATAS ENDS

CODES SEGMENT
    ASSUME CS:CODES,DS:DATAS
START:
    MOV AX,DATAS
    MOV DS,AX
    
    mov ax, Y		;Y
    mov bx, Z       ;Z
    imul bx         ;Y*Z
    sub ax, 100     ;Y*Z-100
    mov bx, X       ;X
    add ax, bx      ;X+(Y*Z-100)
    mov bx, W       ;W
    cwd              
    idiv bx         ;(X+(Y*Z-100))/W
    mov result, ax   
    
    MOV AH,4CH
    INT 21H
CODES ENDS
    END START
