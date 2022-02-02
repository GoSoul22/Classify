.globl argmax

.text
# =================================================================
# FUNCTION: Given a int vector, return the index of the largest
#	element. If there are multiple, return the one
#	with the smallest index.
# Arguments:
# 	a0 (int*) is the pointer to the start of the vector
#	a1 (int)  is the # of elements in the vector
# Returns:
#	a0 (int)  is the first index of the largest element
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 77.
# =================================================================
argmax:
    li t1, 1 # To compare with a1
    blt a1, t1, error_case # Check the error case

    # Prologue
    addi sp, sp, -4
    sw ra, 0(sp)

    li t0, 1 # Initialize counter to 1, the second value in the array
    li t1, 0 # the index for the largest value till now
    lw t2, 0(a0) # the largest value till now
    addi a0, a0, 4 # The index starts from the second value in the array


loop_start:
    beq t0, a1, loop_end # If counter reaches a1, the length, go to the loop_end

    lw t3, 0(a0)  # Get the value at the index we want to check
    blt t2, t3, update # If the largest value till now is strictly smaller than the current testing value, we update it;
                        # otherwise, we don't

loop_continue:

    addi t0, t0, 1 # t0 = t0 + 1
    addi a0, a0, 4 # a0 goes to the next index
    j loop_start


loop_end:


    # Epilogue
    lw ra, 0(sp)
    addi sp, sp, 4
    mv a0, t1 # Move the register containing the index for the largest value to a0

    ret

update:
    mv t2, t3 # Update the current largest value
    mv t1, t0 # Update the target index to the current index
    j loop_continue


error_case:
    li a1, 77
    j exit2
