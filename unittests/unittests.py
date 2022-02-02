from unittest import TestCase
from framework import AssemblyTest, print_coverage


class TestAbs(TestCase):
    def test_zero(self):
        t = AssemblyTest(self, "abs.s")
        # load 0 into register a0
        t.input_scalar("a0", 0)
        # call the abs function
        t.call("abs")
        # check that after calling abs, a0 is equal to 0 (abs(0) = 0)
        t.check_scalar("a0", 0)
        # generate the `assembly/TestAbs_test_zero.s` file and run it through venus
        t.execute()


    def test_one(self):
        # same as test_zero, but with input 1
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", 1)
        t.call("abs")
        t.check_scalar("a0", 1)
        t.execute()

    def test_minus_one(self):
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", -1)
        t.call("abs")
        t.check_scalar("a0", 1)
        t.execute()

    @classmethod
    def tearDownClass(cls):
        print_coverage("abs.s", verbose=False)


class TestRelu(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([1, -2, 3, -4, 5, -6, 7, -8, 9])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the relu function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [1, 0, 3, 0, 5, 0, 7, 0, 9])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()

    def test_zero(self):
        t = AssemblyTest(self, "relu.s")
        array0 = t.array([0, 0, 0, 0, 0])
        t.input_array("a0", array0)
        t.input_scalar("a1", len(array0))
        t.call("relu")
        t.check_array(array0, [0, 0, 0, 0, 0])
        t.execute()

    def test_none(self):
        t = AssemblyTest(self, "relu.s")
        array0 = t.array([])
        t.input_array("a0", array0)
        t.input_scalar("a1", len(array0))
        t.call("relu")
        t.execute(78)


    @classmethod
    def tearDownClass(cls):
        print_coverage("relu.s", verbose=False)


class TestArgmax(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([1, -2, 3, -4, 5, -6, 7, -8, 9])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of the array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 8)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()

    def test_single(self):
        t = AssemblyTest(self, "argmax.s")
        array0 = t.array([1])
        t.input_array("a0", array0)
        t.input_scalar("a1", len(array0))
        t.call("argmax")
        t.check_scalar("a0", 0)
        t.execute()

    def test_single_neg(self):
        t = AssemblyTest(self, "argmax.s")
        array0 = t.array([-1])
        t.input_array("a0", array0)
        t.input_scalar("a1", len(array0))
        t.call("argmax")
        t.check_scalar("a0", 0)
        t.execute()

    def test_very_simple(self):
        t = AssemblyTest(self, "argmax.s")
        array0 = t.array([3, 2, 1])
        t.input_array("a0", array0)
        t.input_scalar("a1", len(array0))
        t.call("argmax")
        t.check_scalar("a0", 0)
        t.execute()

    def test_zero(self):
        t = AssemblyTest(self, "argmax.s")
        array0 = t.array([0, 0, 0, 0, 0, 0])
        t.input_array("a0", array0)
        t.input_scalar("a1", len(array0))
        t.call("argmax")
        t.check_scalar("a0", 0)
        t.execute()

    def test_twofold(self):
        t = AssemblyTest(self, "argmax.s")
        array0 = t.array([1, 1, 1, 2, 2, 2])
        t.input_array("a0", array0)
        t.input_scalar("a1", len(array0))
        t.call("argmax")
        t.check_scalar("a0", 3)
        t.execute()

    def test_alternate(self):
        t = AssemblyTest(self, "argmax.s")
        array0 = t.array([1, 2, 3, 1, 2, 3])
        t.input_array("a0", array0)
        t.input_scalar("a1", len(array0))
        t.call("argmax")
        t.check_scalar("a0", 2)
        t.execute()

    def test_neg(self):
        t = AssemblyTest(self, "argmax.s")
        array0 = t.array([-9, -8, -7, -6, -5, -3, -2, -1])
        t.input_array("a0", array0)
        t.input_scalar("a1", len(array0))
        t.call("argmax")
        t.check_scalar("a0", 7)
        t.execute()

    def test_none(self):
        t = AssemblyTest(self, "argmax.s")
        array0 = t.array([])
        t.input_array("a0", array0)
        t.input_scalar("a1", len(array0))
        t.call("argmax")
        t.execute(77)

    @classmethod
    def tearDownClass(cls):
        print_coverage("argmax.s", verbose=False)


class TestDot(TestCase):
    def test_simple(self):
        """
        Both arrays have 9 elements and the returned vector have one element.
        """
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        # load array attributes into argument registers
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 285)
        t.execute()

    def test_zero(self):
        t = AssemblyTest(self, "dot.s")
        array0 = t.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", 5)
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        t.call("dot")
        t.check_scalar("a0", 0)
        t.execute()

    def test_1D(self):
        """
        When a0 contains only one element, and a1 contains 9 elements, with the length
        of vector returned being 1.
        """
        t = AssemblyTest(self, "dot.s")
        array0 = t.array([1])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        t.call("dot")
        t.check_scalar("a0", 1)
        t.execute()

    def test_2D(self):
        """
        a0 contains a vector length 2, a1 contains vector length 5, and the returned
        vector has length 2.
        """
        t = AssemblyTest(self, "dot.s")
        array0 = t.array([1, 5])
        array1 = t.array([1, 3, 5, 7, 9])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        t.call("dot")
        t.check_scalar("a0", 16)
        t.execute()

    def test_3D(self):
        """
        a0 and a1 both are vectors of length 3, the returned vector is length 3.
        """
        t = AssemblyTest(self, "dot.s")
        array0 = t.array([1, 5, 9])
        array1 = t.array([1, 5, 9])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        t.call("dot")
        t.check_scalar("a0", 107)
        t.execute()

    def test_neg(self):
        t = AssemblyTest(self, "dot.s")
        array0 = t.array([1, -1, 1, -2, 1, -3])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        t.call("dot")
        t.check_scalar("a0", -19)
        t.execute()

    def test_stride_v0(self):
        t = AssemblyTest(self, "dot.s")
        array0 = t.array([1, 3, 5, 7, 9])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 2)
        t.input_scalar("a4", 1)
        t.call("dot")
        t.check_scalar("a0", 38)
        t.execute()

    def test_stride_v1(self):
        t = AssemblyTest(self, "dot.s")
        array0 = t.array([1, 3, 5])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 3)
        t.call("dot")
        t.check_scalar("a0", 48)
        t.execute()

    def test_stride_v0_v1(self):
        t = AssemblyTest(self, "dot.s")
        array0 = t.array([1, 2, 3, 4, 5])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", 2)
        t.input_scalar("a3", 3)
        t.input_scalar("a4", 2)
        t.call("dot")
        t.check_scalar("a0", 13)
        t.execute()

    def test_stride_v0_v1_2(self):
        t = AssemblyTest(self, "dot.s")
        array0 = t.array([1, 3, 5, 7, 9])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 2)
        t.input_scalar("a4", 5)
        t.call("dot")
        t.check_scalar("a0", 130)
        t.execute()

    def test_length_error(self):
        t = AssemblyTest(self, "dot.s")
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", 0)
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        t.call("dot")
        t.execute(75)

    def test_length_error_with_zero(self):
        t = AssemblyTest(self, "dot.s")
        array0 = t.array([])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        t.call("dot")
        t.execute(75)

    def test_stride_error_v0(self):
        t = AssemblyTest(self, "dot.s")
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", 1)
        t.input_scalar("a3", 0)
        t.input_scalar("a4", 1)
        t.call("dot")
        t.execute(76)

    def test_stride_error_v1(self):
        t = AssemblyTest(self, "dot.s")
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", 1)
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 0)
        t.call("dot")
        t.execute(76)

    def test_stride_error_v0_v1(self):
        t = AssemblyTest(self, "dot.s")
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", 1)
        t.input_scalar("a3", 0)
        t.input_scalar("a4", 0)
        t.call("dot")
        t.execute(76)

    def test_length_stride_error(self):
        t = AssemblyTest(self, "dot.s")
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        t.input_array("a0", array0)
        t.input_array("a1", array1)
        t.input_scalar("a2", 0)
        t.input_scalar("a3", 0)
        t.input_scalar("a4", 0)
        t.call("dot")
        t.execute(75)

    @classmethod
    def tearDownClass(cls):
        print_coverage("dot.s", verbose=False)


class TestMatmul(TestCase):

    def do_matmul(self, m0, m0_rows, m0_cols, m1, m1_rows, m1_cols, result, code=0):
        t = AssemblyTest(self, "matmul.s")
        # we need to include (aka import) the dot.s file since it is used by matmul.s
        t.include("dot.s")

        # create arrays for the arguments and to store the result
        array0 = t.array(m0)
        array1 = t.array(m1)
        array_out = t.array([0] * len(result))

        # load address of input matrices and set their dimensions
        t.input_array("a0", array0)
        t.input_scalar("a1", m0_rows)
        t.input_scalar("a2", m0_cols)

        t.input_array("a3", array1)
        t.input_scalar("a4", m1_rows)
        t.input_scalar("a5", m1_cols)
        # load address of output array
        t.input_array("a6", array_out)

        # call the matmul function
        t.call("matmul")

        # check the content of the output array
        if code == 0:
            t.check_array(array_out, result)

        # generate the assembly file and run it through venus, we expect the simulation to exit with code `code`
        t.execute(code=code)


    def test_simple(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [30, 36, 42, 66, 81, 96, 102, 126, 150]
        )

    def test_zero(self):
        self.do_matmul(
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 3, 3,
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 3, 3,
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        )

    def test_identity(self):
        self.do_matmul(
            [1, 0, 0, 0, 1, 0, 0, 0, 1], 3, 3,
            [1, 0, 0, 0, 1, 0, 0, 0, 1], 3, 3,
            [1, 0, 0, 0, 1, 0, 0, 0, 1]
        )

    def test_get_back(self):
        """
        The multiplication between a matrix and identity matrix should get back the matrix.
        """
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 0, 0, 0, 1, 0, 0, 0, 1], 3, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9]
        )

    ## All sorts of legal multiplication ##

    def test_13_31(self):
        self.do_matmul(
            [1, 2, 3], 1, 3,
            [1, 2, 3], 3, 1,
            [14]
        )

    def test_31_13(self):
        self.do_matmul(
            [1, 2, 3], 3, 1,
            [1, 2, 3], 1, 3,
            [1, 2, 3, 2, 4, 6, 3, 6, 9]
        )

    def test_22_22(self):
        self.do_matmul(
            [3, 5, 6, 8], 2, 2,
            [3, 5, 6, 8], 2, 2,
            [39, 55, 66, 94]
        )

    def test_23_32(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6], 2, 3,
            [1, 2, 4, 5, 7, 8], 3, 2,
            [30, 36, 66, 81]
        )

    def test_32_23(self):
        self.do_matmul(
            [1, 2, 4, 5, 7, 8], 3, 2,
            [1, 2, 3, 4, 5, 6], 2, 3,
            [9, 12, 15, 24, 33, 42, 39, 54, 69]
        )

    def test_34_43(self):
        self.do_matmul(
            [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4], 3, 4,
            [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3], 4, 3,
            [10, 20, 30, 10, 20, 30, 10, 20, 30]
        )

    def test_43_34(self):
        self.do_matmul(
            [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3], 4, 3,
            [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4], 3, 4,
            [6, 12, 18, 24, 6, 12, 18, 24, 6, 12, 18, 24, 6, 12, 18, 24]
        )

    ## Error cases ##

    def test_nonsense_m0_0(self):
        self.do_matmul(
            [], 0, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [30, 36, 42, 66, 81, 96, 102, 126, 150], 72
        )

    def test_nonsense_m0_1(self):
        self.do_matmul(
            [], 3, 0,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [30, 36, 42, 66, 81, 96, 102, 126, 150], 72
        )

    def test_nonsense_m1_0(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [], 0, 3,
            [30, 36, 42, 66, 81, 96, 102, 126, 150], 73
        )

    def test_nonsense_m1_1(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [], 3, 0,
            [30, 36, 42, 66, 81, 96, 102, 126, 150], 73
        )

    def test_not_match(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 2, 3, 4, 5, 6], 2, 3,
            [30, 36, 42, 66, 81, 96, 102, 126, 150], 74
        )


    @classmethod
    def tearDownClass(cls):
        print_coverage("matmul.s", verbose=False)


class TestReadMatrix(TestCase):

    def do_read_matrix(self, fail='', code=0, num="", row=3, col=3, ref_array=[1,2,3,4,5,6,7,8,9]):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", "inputs/test_read_matrix/test_input" + num + ".bin")

        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])

        # load the addresses to the output parameters into the argument registers
        # TODO
        t.input_array("a1", rows)
        t.input_array("a2", cols)

        # call the read_matrix function
        t.call("read_matrix")

        # check the output from the function
        t.check_array(rows, [row])
        t.check_array(cols, [col])
        t.check_array_pointer("a0", ref_array)

        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)

    def test_simple(self):
        self.do_read_matrix()

    def test_simple2(self):
        self.do_read_matrix(num="2", row=3, col=1, ref_array=[3, -1, 2])

    def test_simple3(self):
        self.do_read_matrix(num="3", row=2, col=5, ref_array=[6, 7, 894, -235, 65, 4, 64, -324, 643, 8])

    def test_simple4(self):
        self.do_read_matrix(num="4", row=2, col=3, ref_array=[6, 4, 2, 5, 3, 1])

    def test_simple5(self):
        self.do_read_matrix(num="5", row=4, col=2, ref_array=[7, 8, 352, 86, -3, 0, 0, -92])

    def test_error_malloc(self):
        self.do_read_matrix(fail= "malloc", code = 88)
    def test_error_fopen(self):
        self.do_read_matrix(fail= "fopen", code = 90)
    def test_error_fread(self):
        self.do_read_matrix(fail= "fread", code = 91)
    def test_error_fclose(self):
        self.do_read_matrix(fail= "fclose", code = 92)


    @classmethod
    def tearDownClass(cls):
        print_coverage("read_matrix.s", verbose=False)


class TestWriteMatrix(TestCase):

    def do_write_matrix(self, fail='', code=0, out_path="student1.bin", ref_path="reference1.bin"):
        t = AssemblyTest(self, "write_matrix.s")
        outfile = "outputs/test_write_matrix/" + out_path
        # load output file name into a0 register
        t.input_write_filename("a0", outfile)
        # load input array and other arguments
        t.input_array("a1", t.array([1,2,3,4,5,6,7,8,9]))
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 3)

        # call `write_matrix` function
        t.call("write_matrix")
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        # compare the output file against the reference
        if code == 0:
            t.check_file_output(outfile, "outputs/test_write_matrix/" + ref_path)

    def test_simple(self):
        self.do_write_matrix()

    def test_error_fopen(self):
        self.do_write_matrix(fail= "fopen", code = 93)

    def test_error_fwrite(self):
        self.do_write_matrix(fail= "fwrite", code = 94)

    def test_error_fclose(self):
        self.do_write_matrix(fail= "fclose", code = 95)


    @classmethod
    def tearDownClass(cls):
        print_coverage("write_matrix.s", verbose=False)


class TestClassify(TestCase):

    def make_test(self):
        t = AssemblyTest(self, "classify.s")
        t.include("argmax.s")
        t.include("dot.s")
        t.include("matmul.s")
        t.include("read_matrix.s")
        t.include("relu.s")
        t.include("write_matrix.s")
        return t

    # def test_simple0_input0(self):
    #     t = self.make_test()
    #     # Load 0 into a2 to indicate we want to print the classification
    #     t.input_scalar("a2", 0)
    #     out_file = "outputs/test_basic_main/student0.bin"
    #     ref_file = "outputs/test_basic_main/reference0.bin"
    #     args = ["inputs/simple0/bin/m0.bin", "inputs/simple0/bin/m1.bin",
    #             "inputs/simple0/bin/inputs/input0.bin", out_file]
    #     # call classify function
    #     t.call("classify")
    #     # generate assembly and pass program arguments directly to venus
    #     t.execute(args=args)
    #
    #     # compare the output file and
    #     t.check_file_output(out_file, )
    #     # compare the classification output with `check_stdout`


    def test_simple_input(self, simple, input, out_path, ref_path, label):
        t = self.make_test()
        t.input_scalar("a2", 0)
        out_file = "outputs/test_basic_main/output/" + simple + "/" + out_path + ".bin"
        ref_file = "outputs/test_basic_main/reference/" + simple + "/" + ref_path + ".bin"
        args = ["inputs/" + simple + "/bin/m0.bin", "inputs/" + simple + "/bin/m1.bin",
                "inputs/" + simple +  "/bin/inputs/" + input + ".bin", out_file]
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args)

        # compare the output file and
        t.check_file_output(out_file, ref_file)
        # compare the classification output with `check_stdout`
        t.check_stdout(label)

    def test_simple0_input0(self):
        self.test_simple_input("simple0", "input0", "output0", "reference0", "2")

    def test_simple0_input1(self):
        self.test_simple_input("simple0", "input1", "output1", "reference1", "2")

    def test_simple0_input2(self):
        self.test_simple_input("simple0", "input2", "output2", "reference2", "2")

    def test_simple1_input0(self):
        self.test_simple_input("simple1", "input0", "output0", "reference0", "1")

    def test_simple1_input1(self):
        self.test_simple_input("simple1", "input1", "output1", "reference1", "4")

    def test_simple1_input2(self):
        self.test_simple_input("simple1", "input2", "output2", "reference2", "1")

    def test_simple2_input0(self):
        self.test_simple_input("simple2", "input0", "output0", "reference0", "7")

    def test_simple2_input1(self):
        self.test_simple_input("simple2", "input1", "output1", "reference1", "4")

    def test_simple2_input2(self):
        self.test_simple_input("simple2", "input2", "output2", "reference2", "10")



    @classmethod
    def tearDownClass(cls):
        print_coverage("classify.s", verbose=False)


class TestMain(TestCase):

    def run_main(self, inputs, output_id, label):
        args = [f"{inputs}/m0.bin", f"{inputs}/m1.bin", f"{inputs}/inputs/input0.bin",
                f"outputs/test_basic_main/student{output_id}.bin"]
        reference = f"outputs/test_basic_main/reference{output_id}.bin"
        t = AssemblyTest(self, "main.s", no_utils=True)
        t.call("main")
        t.execute(args=args, verbose=False)
        t.check_stdout(label)
        t.check_file_output(args[-1], reference)

    def test0(self):
        self.run_main("inputs/simple0/bin", "0", "2")

    def test1(self):
        self.run_main("inputs/simple1/bin", "1", "1")
