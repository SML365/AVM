# --- AVM --- #

RAM_SIZE = 50 * (1024 * 1024) # 50 MiB
PROGRAM_SIZE = 1 * (1024 * 1024) # 1 MiB

class vCPU:
    def __init__(self):
        self.ram = bytearray(RAM_SIZE) # Allocate RAM for virtual machine
        self.registers = {
            0x00: 0,
            0x01: 0,
            0x02: 0,
            0x03: 0,
            0x04: 0,
            0x05: 0,
            0x06: 0,
            0x07: 0,
            0x08: 0,
            0x09: 0,
            0x0A: 0,
            0x0B: 0,
            0x0C: 0,
            0x0D: 0,
            0x0E: 0,
            0x0F: 0,
        }

        self.program_counter = 0
        self.running = True

    def execute(self, program):
        while self.running and self.program_counter < len(program):
            instruction = program[self.program_counter + 0]
            source_1 = program[self.program_counter + 1]
            source_2 = program[self.program_counter + 2]
            destination = program[self.program_counter + 3]
            immediate = int.from_bytes(program[self.program_counter + 4 : self.program_counter + 8], "big", signed=True)

            self.program_counter += 8

            self.dispatch(instruction, source_1, source_2, destination, immediate)

    def dispatch(self, instruction, source_1, source_2, destination, immediate):
        if instruction == 0xFF:
            self.running = False

        elif instruction == 0x01:
            self.registers[destination] = immediate

        elif instruction == 0x02:
            self.registers[destination] = self.registers[source_1]

        elif instruction == 0x03:
            self.registers[destination] = int.from_bytes(self.ram[immediate * 8 : immediate * 8 + 8], "big", signed=False)
            print(destination)

        elif instruction == 0x04:
            self.ram[immediate * 8: immediate * 8 + 8] = (self.registers[source_1]).to_bytes(8, "big", signed=False)

        elif instruction == 0x11:
            self.registers[destination] = self.registers[source_1] + self.registers[source_2]

        elif instruction == 0x12:
            self.registers[destination] = self.registers[source_1] - self.registers[source_2]

        elif instruction == 0x13:
            self.registers[destination] = self.registers[source_1] * self.registers[source_2]

        elif instruction == 0x14:
            self.registers[destination] = self.registers[source_1] // self.registers[source_2]
        

class Assembler:
    def __init__(self):
        pass

    def assemble(self, program):
        self.assembled = bytearray()
        self.program_lines = program.split(";")

        for index in range(len(self.program_lines)):
            split_line = self.program_lines[index].strip().split(" ")
            command = split_line[0].strip()

            try:
                if command == "STOP":
                    self.assembled += self.encode(0xff)

                elif command == "REG":
                    self.assembled += self.encode(instruction=0x01, destination=int(split_line[1], 0), immediate=int(split_line[2]))

                elif command == "COPY":
                    self.assembled += self.encode(instruction=0x02, source_1=int(split_line[1], 0), destination=int(split_line[2], 0))

                elif command == "LOAD":
                    self.assembled += self.encode(instruction=0x03, immediate=int(split_line[1], 0), destination=int(split_line[2], 0))

                elif command == "STORE":
                    self.assembled += self.encode(instruction=0x04, source_1=int(split_line[1], 0), immediate=int(split_line[2], 0))

                elif command == "ADD":
                    self.assembled += self.encode(instruction=0x11, source_1=int(split_line[1], 0), source_2=int(split_line[2], 0), destination=int(split_line[3], 0))

                elif command == "SUB":
                    self.assembled += self.encode(instruction=0x12, source_1=int(split_line[1], 0), source_2=int(split_line[2], 0), destination=int(split_line[3], 0))

                elif command == "MUL":
                    self.assembled += self.encode(instruction=0x13, source_1=int(split_line[1], 0), source_2=int(split_line[2], 0), destination=int(split_line[3], 0))

                elif command == "DIV":
                    self.assembled += self.encode(instruction=0x14, source_1=int(split_line[1], 0), source_2=int(split_line[2], 0), destination=int(split_line[3], 0))

            except Exception as e:
                print("Error assembling: ", e)
                return

        return self.assembled

    def encode(self, instruction, source_1=0, source_2=0, destination=0, immediate=0):
        return (
            bytes([instruction, source_1, source_2, destination]) + immediate.to_bytes(4, "big", signed=True)
        )


if __name__ == "__main__":
    assembler = Assembler()
    code = assembler.assemble("""
        REG 0x00 100000;
        STORE 0x00 1;
        STORE 0x00 8;
        LOAD 1 0x02;
        STOP;
        """)
    
    cpu = vCPU()
    cpu.execute(code)
    print(cpu.registers)