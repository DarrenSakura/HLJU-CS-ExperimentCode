DATAS SEGMENT
    ARRAY DW 23, 58, 14, 67, 89, 10, 98, 35, 72, 41          
    MAX   DW 0        
    MIN   DW 0FFFFh     
    msgMax DB 'Max: $'
    msgMin DB 0DH, 0AH, 'Min: $'  
    newline DB 0DH, 0AH, '$'      
DATAS ENDS
STACKS SEGMENT STACK
    DW 128 DUP(0)     
STACKS ENDS
CODES SEGMENT
    ASSUME CS:CODES, DS:DATAS, SS:STACKS
START:  
    MOV AX, DATAS
    MOV DS, AX         
    MOV AX, STACKS
    MOV SS, AX         
    MOV SP, 128            
    LEA SI, ARRAY     
    MOV CX, 10         
    MOV AX, [SI]      
    MOV MAX, AX        
    MOV MIN, AX        
NEXT_ELEMENT:
    MOV AX, [SI]       
    CMP AX, MAX
    JLE NOT_GREATER    
    MOV MAX, AX        
NOT_GREATER:
    CMP AX, MIN
    JGE NOT_LESS       
    MOV MIN, AX        
NOT_LESS:
    
    ADD SI, 2          
    LOOP NEXT_ELEMENT  
    LEA DX, msgMax     
    CALL PRINT_STRING  
    MOV AX, MAX        
    CALL PRINT_DECIMAL 
    LEA DX, msgMin     
    CALL PRINT_STRING
    MOV AX, MIN        
    CALL PRINT_DECIMAL
    LEA DX, newline
    CALL PRINT_STRING
    MOV AH, 4CH
    INT 21H
PRINT_STRING PROC
    PUSH AX           
    MOV AH, 09H      
    INT 21H           
    POP AX             
    RET
PRINT_STRING ENDP
PRINT_DECIMAL PROC
    PUSH AX           
    PUSH BX
    PUSH CX
    PUSH DX
    CMP AX, 0
    JNE NON_ZERO
    MOV DL, '0'        
    MOV AH, 02H
    INT 21H
    JMP DECIMAL_END
NON_ZERO:
    XOR CX, CX         
    MOV BX, 10         
DIVIDE_LOOP:
    XOR DX, DX         
    DIV BX             
    PUSH DX           
    INC CX             
    CMP AX, 0          
    JNE DIVIDE_LOOP       
PRINT_LOOP:
    POP DX             
    ADD DL, '0'       
    MOV AH, 02H        
    INT 21H
    LOOP PRINT_LOOP       
DECIMAL_END:
    POP DX           
    POP CX
    POP BX
    POP AX
    RET
PRINT_DECIMAL ENDP
CODES ENDS
END START  
