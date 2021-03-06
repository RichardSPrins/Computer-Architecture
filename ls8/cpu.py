"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    instructions = {
        0b10000010: 'LDI',
        0b01000111: 'PRN',
        0b00000001: 'HLT',
        0b10100010: 'MUL'
    }

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.dispatch = {
            'LDI': self.LDI,
            'PRN': self.PRN,
            'HLT':self.HLT,
            'MUL': self.MUL
        }


    def load(self):
        """Load a program into memory."""
        address = 0

        # For now, we've just hardcoded a program:

        with open(sys.argv[1]) as program:
            for line in program:
                data = line.split('#')[0].strip()
                if data == '':
                    continue
                value = int(data, 2)

                self.ram_write(address, value)
                address += 1
                # print(value)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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
            print(" %02X" % self.reg[i], end='')

        print()


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def LDI(self):
        self.pc += 1
        op_1 = self.ram_read(self.pc)
        self.pc += 1
        op_2 = self.ram_read(self.pc)
        self.reg[op_1] = op_2


    def PRN(self):
        self.pc += 1
        op_1 = self.ram_read(self.pc)
        value = self.reg[op_1]
        print(value)
        

    def HLT(self):
        self.running = False

    def MUL(self):
        self.pc += 1
        op_1 = self.ram_read(self.pc)
        self.pc += 1
        op_2 = self.ram_read(self.pc)
        math = self.reg[op_1] * self.reg[op_2]
        self.reg[op_1] = math

    def run(self):
        """Run the CPU."""
        
        # print(self.ram)
        while self.running:
            instruction_register = self.ram[self.pc]

            # print(instruction_register)
            if instruction_register in self.instructions:
                command = self.instructions[instruction_register]
                self.dispatch[command]()
            
            self.pc += 1


