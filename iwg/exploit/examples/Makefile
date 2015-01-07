all: calc hw

calc: calc.o
	gcc -m32 calc.o -o calc

calc.o: calc.asm
	nasm -felf calc.asm -o calc.o

hw: hw.o
	gcc -m32 hw.o -o hw

hw.o: hw.asm
	nasm -felf hw.asm -o hw.o

clean:
	rm *.o calc hw
