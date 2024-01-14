// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

    // i = SCREEN
    @SCREEN
    D=A
    @i
    M=D
    // n = SCREEN + 8191
    @8191
    D=D+A
    @n
    M=D
(LOOP)
    // if (KBD = 0) goto ERASE
    @KBD
    D=M
    @ERASE
    D;JEQ
    // goto PAINT
    @PAINT
    0;JMP
(PAINT)
    // if (i > n) goto LOOP
    @i
    D=M
    @n
    D=D-M
    @LOOP
    D;JGT
    // *i = -1
    @i
    A=M
    M=-1
    // i = i + 1
    @i
    M=M+1
    // goto LOOP
    @LOOP
    0;JMP
(ERASE)
    // if (i == SCREEN) goto LOOP
    @i
    D=M
    @SCREEN
    D=D-A
    @LOOP
    D;JEQ
    // i = i - 1
    @i
    M=M-1
    // *i = 0
    A=M
    M=0
    // goto LOOP
    @LOOP
    0;JMP
(END)
    @END
    0;JMP