.globl classify

.text
classify:
    # =====================================
    # COMMAND LINE ARGUMENTS
    # =====================================
    # Args:
    #   a0 (int)    argc
    #   a1 (char**) argv
    #   a2 (int)    print_classification, if this is zero, 
    #               you should print the classification. Otherwise,
    #               this function should not print ANYTHING.
    # Returns:
    #   a0 (int)    Classification
    # Exceptions:
    # - If there are an incorrect number of command line args,
    #   this function terminates the program with exit code 89.
    # - If malloc fails, this function terminats the program with exit code 88.
    #
    # Usage:
    #   main.s <M0_PATH> <M1_PATH> <INPUT_PATH> <OUTPUT_PATH>

    # =====================================
    # PROLOGUE
    # =====================================
    addi sp, sp, -60
    sw ra, 0(sp)
    sw s1, 4(sp)                # argv
    sw s2, 8(sp)                # print_classification
    sw s3, 12(sp)               # s3 will be used as a pointer to matrix M0 in memory
    sw s4, 16(sp)               # s4 will be used as a pointer to matrix M1 in memory
    sw s5, 20(sp)               # s5 will be used as a pointer to matrix INPUT in memory
    sw s6, 24(sp)               # s6 will be used as a pointer to (m0 * input) in memory
    sw s7, 28(sp)               # s7 will be used as a pointer to (m1 * ReLU(m0 * input)) in memory

    mv s1, a1                   # argv
    mv s2, a2                   # print_classification



    # =====================================
    # COMMAND LINE ARGS
    # =====================================
    li t0, 5
    bne a0, t0, error_arguments





	# =====================================
    # LOAD MATRICES
    # =====================================

    # Load pretrained m0
    lw a0, 4(s1)
    addi a1, sp, 32             # Pointer to #rows of M0
    addi a2, sp, 36             # Pointer to #rows of M0
    jal read_matrix
    mv s3, a0                   # s3 is a pointer to matrix M0 in memory

    # Load pretrained m1
    lw a0, 8(s1)
    addi a1, sp, 40             # Pointer to #rows of M1
    addi a2, sp, 44             # Pointer to #rows of M1
    jal read_matrix
    mv s4, a0                   # s4 is a pointer to matrix M1 in memory


    # Load input matrix
    lw a0, 12(s1)
    addi a1, sp, 48             # Pointer to #rows of INPUT
    addi a2, sp, 52             # Pointer to #rows of INPUT
    jal read_matrix
    mv s5, a0                   # s5 is a pointer to matrix INPUT in memory



    # =====================================
    # RUN LAYERS
    # =====================================
    # 1. LINEAR LAYER:    m0 * input
    # 2. NONLINEAR LAYER: ReLU(m0 * input)
    # 3. LINEAR LAYER:    m1 * ReLU(m0 * input)

    # 1. LINEAR LAYER:    m0 * input
    lw t0, 32(sp)
    lw t1, 52(sp)
    mul a0, t0, t1
    slli a0, a0, 2
    jal malloc
    mv s6, a0

    mv a0, s3
    lw a1, 32(sp)
    lw a2, 36(sp)
    mv a3, s5
    lw a4, 48(sp)
    lw a5, 52(sp)
    mv a6, s6                    # s6 is a pointer to (m0 * input) in memory
    jal matmul


    # 2. NONLINEAR LAYER: ReLU(m0 * input)
    mv a0, s6
    lw t0, 32(sp)
    lw t1, 52(sp)
    mul a1, t0, t1
    jal relu                    # s6 is a pointer to ReLU(m0 * input) in memory


    # 3. LINEAR LAYER:    m1 * ReLU(m0 * input)
    lw t0, 40(sp)
    lw t1, 52(sp)
    mul a0, t0, t1
    slli a0, a0, 2
    jal malloc
    mv s7, a0

    mv a0, s4
    lw a1, 40(sp)
    lw a2, 44(sp)
    mv a3, s6
    lw a4, 32(sp)
    lw a5, 52(sp)
    mv a6, s7
    jal matmul                  # s7 is a pointer to (m1 * ReLU(m0 * input)) in memory





    # =====================================
    # WRITE OUTPUT
    # =====================================
    # Write output matrix
    lw a0, 16(s1)
    mv a1, s7
    lw a2, 40(sp)
    lw a3, 52(sp)
    jal write_matrix





    # =====================================
    # CALCULATE CLASSIFICATION/LABEL
    # =====================================
    # Call argmax
    mv a0, s7
    lw t0, 40(sp)
    lw t1, 52(sp)
    mul a1, t0, t1
    jal argmax
    sw a0, 56(sp)                         # store the return value on stack


    # Print classification
    bne s2, x0, exit
    mv a1, a0
    jal print_int

    # Print newline afterwards for clarity
    li a1, '\n'
    jal print_char


exit:
    # Remember to always free all data allocated at the end of this process.
    mv a0, s3
    jal free

    mv a0, s4
    jal free

    mv a0, s5
    jal free

    mv a0, s6
    jal free

    mv a0, s7
    jal free

    lw a0, 56(sp)                         # set up return value

    # Epilogue
    lw ra, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    lw s3, 12(sp)
    lw s4, 16(sp)
    lw s5, 20(sp)
    lw s6, 24(sp)
    lw s7, 28(sp)
    addi sp, sp, 60
    ret

error_malloc:
    li a1, 88
    j exit2

error_arguments:
    li a1, 89
    j exit2

