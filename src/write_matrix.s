.globl write_matrix

.text
# ==============================================================================
# FUNCTION: Writes a matrix of integers into a binary file
# FILE FORMAT:
#   The first 8 bytes of the file will be two 4 byte ints representing the
#   numbers of rows and columns respectively. Every 4 bytes thereafter is an
#   element of the matrix in row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is the pointer to the start of the matrix in memory
#   a2 (int)   is the number of rows in the matrix
#   a3 (int)   is the number of columns in the matrix
# Returns:
#   None
# Exceptions:
# - If you receive an fopen error or eof,
#   this function terminates the program with error code 93.
# - If you receive an fwrite error or eof,
#   this function terminates the program with error code 94.
# - If you receive an fclose error or eof,
#   this function terminates the program with error code 95.
# ==============================================================================
write_matrix:

    # Prologue
    addi sp, sp, -32
    sw ra, 0(sp)
    sw s8, 4(sp)
    sw s1, 8(sp)
    sw s2, 12(sp)
    sw s3, 16(sp)
    sw s9, 20(sp)       # s9 will be used to store a file descriptor
    sw a2, 24(sp)       # We need this address for fwrite
    sw a3, 28(sp)       # We need this address for fwrite

    mv s1, a1           # s1 is the pointer to the start of the matrix in memory
    mv s2, a2           # s2 is the number of rows in the matrix
    mv s3, a3           # s3 is the number of columns in the matrix
    mv s8, a0           # s8 is the pointer to string representing the filename


# open file
    mv a1, s8           # a1 is a pointer to a string containing the filename of the file to open
    li a2, 1            # a2 for write only permission
    jal fopen
    li t0, -1
    beq a0, t0, error_fopen
    mv s9, a0           # s9 stores a file descriptor

# write row and col
    mv a1, s9               # a1 stores a file descriptor
    addi a2, sp, 24         # a2 should be a pointer
    addi a3, x0, 1
    addi a4, x0, 4
    jal fwrite
    li t0, 1
    bne a0, t0, error_fwrite

    mv a1, s9
    addi a2, sp, 28
    addi a3, x0, 1
    addi a4, x0, 4
    jal fwrite
    li t0, 1
    bne a0, t0, error_fwrite


# write file: No loop needed
    mv a1, s9
    mv a2, s1
    mul a3, s2, s3
    addi a4, x0, 4
    jal fwrite
    mul t0, s2, s3
    bne a0, t0, error_fwrite



# close file
    mv a1, s9             # set up the parameter a1 = file descriptor
    jal fclose
    bne a0, x0, error_fclose

# Epilogue
    lw ra, 0(sp)
    lw s8, 4(sp)
    lw s1, 8(sp)
    lw s2, 12(sp)
    lw s3, 16(sp)
    lw s9, 20(sp)
    addi sp, sp, 32
# return None
    ret


error_fopen:
    li a1, 93
    j exit2

error_fwrite:
    li a1, 94
    j exit2

error_fclose:
    li a1, 95
    j exit2
