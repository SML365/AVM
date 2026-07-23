# --- AVM --- #

RAM_SIZE = 50 * (1024 * 1024) # 50 MiB
PROGRAM_SIZE = 1 * (1024 * 1024) # 1 MiB

class vCPU:
    def __init__(self):
        self.ram = bytearray(RAM_SIZE) # Allocate RAM for virtual machine
        self.registers = {
            0x01: 0,
            0x02: 0,
            0x03: 0,
            0x04: 0,
            0x05: 0,
            0x06: 0,
            0x07: 0,
            0x08: 0,
            0x09: 0,
            0x10: 0,
            0x11: 0,
            0x12: 0,
            0x13: 0,
            0x14: 0,
            0x15: 0,
            0x16: 0,
        }

        self.program_counter = 0
        self.running = True

    def execute(self, program):
        while self.running and self.program_counter < len(program):
            instruction = program[self.program_counter + 0]
            source_1 = program[self.program_counter + 1]
            source_2 = program[self.program_counter + 2]
            destination = program[self.program_counter + 3]
            immediate = int.from_bytes(program[self.program_counter + 4 : self.program_counter + 8], "big")

            self.program_counter += 8

            self.dispatch(instruction, source_1, source_2, destination, immediate)

    def dispatch(self, instruction, source_1, source_2, destination, immediate):
        if instruction == 0xFF:
            self.running = False

if __name__ == "__main__":
    cpu = vCPU()
    cpu.execute(b'\xFF')