.globl relu

.text
# ==============================================================================
# FUNCTION: Performs an inplace element-wise ReLU on an array of ints
# Arguments:
# 	a0 (int*) is the pointer to the array
#	a1 (int)  is the # of elements in the array
# Returns:
#	None
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 78.
# ==============================================================================
relu:
	li, t1, 1 # For comparison with a1
	blt a1, t1, error_case # Check the error case

    # Prologue
    addi sp, sp, -4
    sw ra, 0(sp)

    li t0, 0 # Initialize counter to 0

loop_start:
    beq t0, a1, loop_end # If counter reaches a1, the length, go to the loop_end

    lw t1, 0(a0) # Get the value and load into t1
    blt t1, x0, set_zero # Go to set_zero if the value is smaller than 0

loop_continue:
    sw t1, 0(a0) # Assume t1 has been set to the correct value, store it into the correct position

    addi t0, t0, 1 # t0 = t0 + 1
    addi a0, a0, 4 # a0 goes to the next index
    j loop_start

loop_end:

    # Epilogue
    lw ra, 0(sp)
    addi sp, sp, 4

	ret

set_zero:
	mv t1, x0
    j loop_continue

error_case:
	li a1, 78
    j exit2
