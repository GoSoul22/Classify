.globl matmul

.text
# =======================================================
# FUNCTION: Matrix Multiplication of 2 integer matrices
# 	d = matmul(m0, m1)
# Arguments:
# 	a0 (int*)  is the pointer to the start of m0 
#	a1 (int)   is the # of rows (height) of m0
#	a2 (int)   is the # of columns (width) of m0
#	a3 (int*)  is the pointer to the start of m1
# 	a4 (int)   is the # of rows (height) of m1
#	a5 (int)   is the # of columns (width) of m1
#	a6 (int*)  is the pointer to the the start of d
# Returns:
#	None (void), sets d = matmul(m0, m1)
# Exceptions:
#   Make sure to check in top to bottom order!
#   - If the dimensions of m0 do not make sense,
#     this function terminates the program with exit code 72.
#   - If the dimensions of m1 do not make sense,
#     this function terminates the program with exit code 73.
#   - If the dimensions of m0 and m1 don't match,
#     this function terminates the program with exit code 74.
# =======================================================
matmul:

    # Error checks
    li t1, 1 # Load t1 to 1 for further comparison
    blt a1, t1, error_m0_nonsense # If rows of m0 < 1, go to error
    blt a2, t1, error_m0_nonsense # If columns of m0 < 1, go to error

	blt a4, t1, error_m1_nonsense # If rows of m1 < 1, go to error
    blt a5, t1, error_m1_nonsense # If columns of m1 < 1, go to error
    
    bne a2, a4, error_not_match # If the column of m0 does not match the row of m1, go to the error
    
    # Prologue
    addi sp, sp, -36
    sw ra, 0(sp)
    sw s1, 4(sp)
    sw s2, 8(sp)
    sw s3, 12(sp)
    sw s4, 16(sp)
    sw s5, 20(sp)
    sw s6, 24(sp)

    mv s1, a0       # (int*)  is the pointer to the start of m0
    mv s2, a3       # (int*)  is the pointer to the start of m1
    mv s3, a1       # (int)   is the # of rows (height) of m0
    mv s4, a5       # (int)   is the # of columns (width) of m1
    mv s5, a6       # (int*)  is the pointer to the the start of d
    mv s6, a2       # (int)   is the # of columns (width) of m0

    li t0, 0 # Initialize the row counter to 0
    li t1, 0 # Initialize the col counter to 0

loop_outer_start:
    bge t0, s3, loop_outer_end

loop_inner_start:
    bge t1, s4, loop_inner_end
# call dot function with the following arguments:
#   a0 (int*) is the pointer to the start of v0
#   a1 (int*) is the pointer to the start of v1
#   a2 (int)  is the length of the vectors
#   a3 (int)  is the stride of v0
#   a4 (int)  is the stride of v1

    slli t2, t0, 2
    mul t2, t2, s6
    add a0, s1, t2   # set up a0

    slli t2, t1, 2
    add a1, s2, t2   # set up a1

    mv a2, s6        # set up a2

    addi a3, x0, 1   # set up a3

    add a4, x0, s4   # set up a4

    sw t0, 28(sp)
    sw t1, 32(sp)
    jal dot
    lw t0, 28(sp)
    lw t1, 32(sp)

    mul t3, s4, t0
    add t3, t3, t1
    slli t3, t3, 2
    add t3, t3, s5
    sw a0, 0(t3)      # set up matrix

    addi t1, t1, 1                  # Increment col counter t1.
    j loop_inner_start

loop_inner_end:
    li t1, 0
    addi t0 ,t0, 1  # Increment row counter t0.
    j loop_outer_start


loop_outer_end:
    # Epilogue
    lw ra, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    lw s3, 12(sp)
    lw s4, 16(sp)
    lw s5, 20(sp)
    lw s6, 24(sp)

    addi sp, sp, 36
    ret


error_m0_nonsense:
	li a1, 72
    j exit2
    
error_m1_nonsense:
	li a1, 73
    j exit2
    
error_not_match:
	li a1, 74
    j exit2
