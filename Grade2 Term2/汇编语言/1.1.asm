DATA   SEGMENT
           VAR1  DW  35,24,0451H       ;定义源操作数
           VAR2  DW  3 DUP(?)          ;定义目的操作数
DATA   ENDS

CODE   SEGMENT
           ASSUME  DS:DATA,CS:CODE
     START:MOV  AX, DATA                ;数据段初始化
           MOV  DS, AX
           LEA  SI, VAR1
           LEA  DI, VAR2
           MOV  AX, [SI]                ;传送第一个数
           MOV  [DI],AX
           ADD  SI, 2                   ;修改SI，DI数值
           ADD  DI, 2
           MOV  AX, [SI]                ;传送第二个数
           MOV  [DI], AX
           ADD  SI, 2
           ADD  DI, 2
           MOV  AX, [SI]                ;传送第三个数
           MOV  [DI], AX
           MOV  AH, 4CH                 ;程序返回
           INT  21H
CODE   ENDS
           END  START

