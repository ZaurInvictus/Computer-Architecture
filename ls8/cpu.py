"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8 
        self.pc = 0
        self.running = False
        self.HLT = 0b00000001 # Running is false
        self.LDI = 0b10000010 # Save 
        self.PRN = 0b01000111 # Print
        self.MUL = 0b10100010 # Multiply

    def load(self):
        """Load a program into memory."""
        address = 0
        # print(sys.argv)
        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        if len(sys.argv) != 2:
            print("Not correct filename passed in")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                container = []
                for line in f:
                    # ignore comments
                    comment_split = line.split("#")

                    num = comment_split[0].strip()
                    if num == '':
                        continue
                    container.append(num)
                    program = [int(c, 2) for c in container]

        except FileNotFoundError:
            print(f"{sys.argv[0]}! {sys.argv[1]} not found")
            sys.exit(2)

        for instruction in program:
            self.ram[address] = instruction
            address += 1

        # print(program)
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.load()
        self.run_start()
        
        while self.running:
            command = self.ram_read(self.pc)

            if command == self.HLT:
                self.run_HLT()

            elif command == self.LDI:
                self.run_LDI()

            elif command == self.PRN:
                self.run_PRN()

            elif command == self.MUL:
                self.run_MUL()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
        return

    def run_start(self):
        print("Program Started")
        self.running = True

    def run_HLT(self):
        # print(self.register)
        print("Program Ended")
        self.running = False
        self.pc = 0

    def run_LDI(self):
        self.register[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)
        self.pc += 3

    def run_PRN(self):
        print(self.register[self.ram_read(self.pc+1)])
        self.pc += 2

    def run_MUL(self):
        #print(self.register)
        self.register[self.ram_read(self.pc+1)] = self.register[
            self.ram_read(self.pc+1)] * self.register[self.ram_read(self.pc+2)]
        self.pc += 3





