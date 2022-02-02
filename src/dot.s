.globl dot

.text
# =======================================================
# FUNCTION: Dot product of 2 int vectors
# Arguments:
#   a0 (int*) is the pointer to the start of v0
#   a1 (int*) is the pointer to the start of v1
#   a2 (int)  is the length of the vectors
#   a3 (int)  is the stride of v0
#   a4 (int)  is the stride of v1
# Returns:
#   a0 (int)  is the dot product of v0 and v1
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 75.
# - If the stride of either vector is less than 1,
#   this function terminates the program with error code 76.
# =======================================================
dot:
		
    li t1, 1 # To compare with the length and stride
    blt a2, t1, error_length # Test if length < 1
    blt a3, t1, error_stride # Test if stride of v0 < 1
    blt a4, t1, error_stride # Test if stride of v1 < 1

    # Prologue


    li t0, 0 # Initialize the counter to 0
    li t1, 0, # Initialize the sum of the products to 0
    slli t2, a3, 2 # Set t2 to the offset of v0 for each iteration
    slli t3, a4, 2 # Set t3 to the offset of v1 for each iteration

loop_start:
	beq t0, a2, loop_end # If the counter reaches a2, go to the loop_end

    lw t4, 0(a0) # Load the next scalar from v0
	lw t5, 0(a1) # Load the next scalar from v1

    mul t6, t4, t5 # Multiply the two scalar
	add t1, t1, t6 # Add the product to the sum

    addi t0, t0, 1 # t0 = t0 + 1, update the counter
	add a0, a0, t2 # Update the a0 pointer to the scalar taking into account the offset of stride
    add a1, a1, t3 # Update the a1 pointer to the scalar taking into account the offset of stride
	j loop_start


loop_end:
	mv a0, t1

    # Epilogue
    ret

error_length:
	li a1, 75
    j exit2

error_stride:
	li a1, 76
    j exit2
