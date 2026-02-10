// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

// R1 = max address of SCREEM range 8192
@KBD
D=A-1
@R1
M=D

// R0 = the loop variable; iterates over the SCREEN range
(INITIATE_LOOP)
@SCREEN
D=A
@R0
M=D

// Loop
(LOOP)
    // check if R0 == SCREEN_MAX. if so, reinitiate
    @R0
    D=M
    @R1
    D=D-M
    @INITIATE_LOOP
    D;JEQ
    // listen to keyboard. if zero, erase. if not, draw
    @KBD
    D=M
    @ERASE
    D;JEQ
    // draw
    @R0
    A=M
    M=-1
    @INCREMENT
    0;JMP
    // erase
    (ERASE)
    @R0
    A=M
    M=0
    (INCREMENT)
    @R0
    M=M+1
    // loop
    @LOOP
    0;JMP

(END)
    @END
    0;JMP