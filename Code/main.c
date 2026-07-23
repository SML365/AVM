#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// Virtual Machine Structure //
typedef struct {
    uint8_t *ram;
    uint64_t registers[32];
    uint64_t program_counter;
    uint64_t sp;
    uint64_t flags;
} virtual_machine;

// Instruction Structure //
typedef struct {
    uint8_t opcode;
    uint8_t source_1;
    uint8_t source_2;
    uint8_t destination;
    uint32_t immediate;
} instruction;

int main() {
    // Define Constants //
    const int ERROR_CODE = 1;
    const size_t RAM_SIZE = 100 * (1024 * 1024); // In Bytes, 100 MiB

    // Allocate Memory //
    uint8_t *ram = calloc(RAM_SIZE, 1);

    if(ram == NULL) {
        printf("RAM Allocation Failure -- Exiting");
        return ERROR_CODE;
    }

    execute(ram);

    // Free Memory ///
    free(ram);
    ram = NULL;

    // End Program //
    return 0;
}

int execute() {
    return 0;
}