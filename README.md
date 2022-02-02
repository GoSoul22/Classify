# Classify


At the end of this project we written all RISC-V assembly code necessary to run a simple Artificial Neural Network (ANN) on the Venus RISC-V simulator. 


```
.
├── inputs (test inputs)
├── outputs (some test outputs)
├── README.md
├── src
│   ├── argmax.s (partA)
│   ├── classify.s (partB)
│   ├── dot.s (partA)
│   ├── main.s (do not modify)
│   ├── matmul.s (partA)
│   ├── read_matrix.s (partB)
│   ├── relu.s (partA)
│   ├── utils.s (do not modify)
│   └── write_matrix.s (partB)
├── tools
│   ├── convert.py (convert matrix files for partB)
│   └── venus.jar (RISC-V simulator)
└── unittests
    ├── assembly (contains outputs from unittests.py)
    ├── framework.py (do not modify)
    └── unittests.py (partA + partB)
```


## Here's what I did in project 2:
We usually went through reading the instructions and code together, and after fully understanding what we need to do and dividing the work among us, go on to write code.

At the second half of project2A (dot product and matmul), Rixiao got busier, having to deal with two midterms a day, so switched to more of brainstorming and proofreading, while Justin wrote most of the implementation.


### Part A:  
Justin:  
&nbsp; &nbsp; &nbsp; &nbsp; implemented the relu function and tests  
&nbsp; &nbsp; &nbsp; &nbsp; reviewed argmax  
&nbsp; &nbsp; &nbsp; &nbsp; implemented the dot product function and tests  
&nbsp; &nbsp; &nbsp; &nbsp; implemented the matmul function  

Rixiao:  
&nbsp; &nbsp; &nbsp; &nbsp; reviewed relu  
&nbsp; &nbsp; &nbsp; &nbsp; implemented the argmax function and tests  
&nbsp; &nbsp; &nbsp; &nbsp; reviewed the dot product function and proofread to make sure all the calling conventions are met  
&nbsp; &nbsp; &nbsp; &nbsp; wrote the tests for matmul  
&nbsp; &nbsp; &nbsp; &nbsp; debugged matmul to find out the caller convention errors  


### Part B:  
Justin:  
&nbsp; &nbsp; &nbsp; &nbsp; wrote the unittets for read_matrix and write_matrix  
&nbsp; &nbsp; &nbsp; &nbsp; Checked through read_matrix and write_matrix, and classify to debug any error we have  
&nbsp; &nbsp; &nbsp; &nbsp; Provided Main Tests and Classify Tests  


Rixiao:  
&nbsp; &nbsp; &nbsp; &nbsp; implemented read_matrix and some of the tests  
&nbsp; &nbsp; &nbsp; &nbsp; implemented wrtie_matrix and the tests  
&nbsp; &nbsp; &nbsp; &nbsp; implemeneted the classify function  
