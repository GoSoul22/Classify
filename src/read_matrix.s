.globl read_matrix

.text
# ==============================================================================
# FUNCTION: Allocates memory and reads in a binary file as a matrix of integers
#
# FILE FORMAT:
#   The first 8 bytes are two 4 byte ints representing the # of rows and columns
#   in the matrix. Every 4 bytes afterwards is an element of the matrix in
#   row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is a pointer to an integer, we will set it to the number of rows
#   a2 (int*)  is a pointer to an integer, we will set it to the number of columns
# Returns:
#   a0 (int*)  is the pointer to the matrix in memory
# Exceptions:
# - If malloc returns an error,
#   this function terminates the program with error code 88.
# - If you receive an fopen error or eof, 
#   this function terminates the program with error code 90.
# - If you receive an fread error or eof,
#   this function terminates the program with error code 91.
# - If you receive an fclose error or eof,
#   this function terminates the program with error code 92.
# ==============================================================================
read_matrix:

# Prologue
    addi sp, sp, -32
    sw ra, 0(sp)        # store return address
    sw s1, 4(sp)        # s1 will be used as a pointer to an integer (row)
    sw s2, 8(sp)        # s2 will be used as a pointer to an integer (col)
    sw s3, 12(sp)
    sw s10, 16(sp)      # s10 will be used as a pointer to heap memory
    sw s11, 20(sp)      # s11 will be used to store a file descriptor


    mv s1, a1           # s1 will be used as a pointer to an integer (row)
    mv s2, a2           # s2 will be used as a pointer to an integer (col)
    mv s3, a0           # s3 is the pointer to string representing the filename


# open file
    mv a1, s3           # set up the parameter a1 (the pointer to the filename)
    mv a2, x0           # set up the parameter a2. Read Only
    jal fopen           # opens file with name a1 with permissions a2
    li t0, -1
    beq a0, t0, error_fopen   # check for exceptions
    mv s11, a0          # s11 stores a file descriptor

# set up a1 and a2
    mv a1, s11          # set up a1
    mv a2, s1           # set up a2
    addi a3, x0, 4      # set up a3
    jal fread           # read #row
    addi t0, x0, 4
    bne a0, t0, error_fread

    mv a1, s11          # set up a1
    mv a2, s2           # set up a2
    addi a3, x0, 4      # set up a3
    jal fread           # read #col
    addi t0, x0, 4
    bne a0, t0, error_fread


# malloc memory space
    lw t1, 0(s1)    #  Load the row number into t1
    lw t2, 0(s2)    #  Load the col number into t2
    mul t0, t1, t2      # the number of elements of the matrix
    slli t0, t0 , 2     # one word = four bytes
    add a0, x0, t0      # set up the parameter a0
    jal malloc          # malloc memory space
    beq a0, x0 error_malloc   # check for exceptions
    mv s10, a0          # s10 points to heap memory




# read file
    lw t1, 0(s1)     #  Load the row number into t1
    lw t2, 0(s2)     #  Load the col number into t2
    mul  t0, t1, t2      # set up number of iterations t0 = ( #row * #col)
    add  t1, x0, x0      # set up counter t1 = 0

read_file_loop:
    bge t1, t0, loop_exit

    mv a1, s11          # set up the parameter a1 = file descriptor
    slli t2, t1, 2      
    add a2, s10, t2     # set up the parameter a2 = s10 + 4 * t1
    addi a3, x0, 4      # set up the parameter a3 = Number of bytes to be read

    sw t0, 24(sp)
    sw t1, 28(sp)
    jal fread
    lw t0, 24(sp)
    lw t1, 28(sp)

    addi t3, x0, 4
    bne a0, t3, error_fread   # check for exceptions

    addi t1, t1, 1      # t1 += 1
    j read_file_loop

loop_exit:

# close file
    mv a1, s11
    jal fclose
    bne a0, x0, error_fclose


# Epilogue
    mv a0, s10          # Load the pointer into the return argument
    lw ra,  0(sp)
    lw s1,  4(sp)
    lw s2,  8(sp)
    lw s3,  12(sp)
    lw s10, 16(sp)
    lw s11, 20(sp)
    addi sp, sp, 32
    ret



error_malloc:
    li a1, 88
    j exit2

error_fopen:
    li a1, 90
    j exit2     # ra is not needed.

error_fread:
    li a1, 91
    j exit2     # ra is not needed.

error_fclose:
    li a1, 92
    j exit2     # ra is not needed.
