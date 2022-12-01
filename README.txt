---------READ ME------------

Ben Malkin - 1214616377
Noah Wilmot - 1219599511
------------------------------------------

Our program takes in input as command line args and accepts the following commands with appropriate parameters; add, remove, checkin, checkout, log, init, and verify.
For example, "./bchoc add -c ca8b10ca-4741-4031-8a89-62a42494f2c6 -i 3989277403" will add an evidence item with case id = ca8b10ca-4741-4031-8a89-62a42494f2c6 and item id = 3989277403
to the blockchain. Our implementation stores the blockchain in memory during execution and in a binary file when the program stops running. At the beginning of execution,
the program reads the blockchain from the binary file and at the end of execution, writes the blockchain to a binary file. This ensures not only that the blockchain is safely stored but
that it also exists beyond the execution of our program. Any error in input results in a printed error message as well as a termination in the execution of the program