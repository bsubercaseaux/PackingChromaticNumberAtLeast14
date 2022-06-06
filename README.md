# In order to generate the direct encoding of an RxR grid with K colors do

`python3 direct.py <resulting filename> <R> <K> <Toroidal (Boolean)> <Force checkerboard of 1s (Boolean)> <Central forcing>`

Parameters about toroidal constraints and the checkerboard of 1s are not explained in the current submission and thus can be ignored (set to 0).

# In order to generate the encoding of the R-radius ball with K colors do

`python3 direct_diamond.py <resulting filename> <R> <K> <symmetry breaking at encoding level (Boolean)> <Central forcing>`

(Symmetry breaking at encoding level is not explained in the paper, and thus can be set to 0).

Examples:

`python3 direct.py s-7-8.cnf 7 8 0 0 0` should generate the instance `S_{7, 8}`, which is UNSAT.
`python3 direct.py s-8-9.cnf 8 9 0 0 1` should generate the instance `S^+_{8, 9}` which is also UNSAT.

`python3 direct_diamond.py d-5-11.cnf 5 11 0 1` should generate the instance `D^+_{5, 11}` which is SAT.

In order to visualize this, one can then do

`yalsat -v d-5-11.cnf | grep "^v " > sol`
followed by

`python3 sol_to_color_diamond.py sol 5 11`

# In order to generate cubes for l-1 ball (diamond) use

`python3 cube_gen.py <cnf file> <R> <K> <F> <symmetry breaking (Boolean)> <d>`

# In order to generate cubes for an RxR grid use

`python3 cube_s_gen.py <cnf file> <R> <K> <F> <symmetry breaking (Boolean)>`


For example:
`python3 direct_diamond.py d-5-9.cnf 5 9 0 1` to generate instance `D^+_{5, 10}`.
`python3 cube_gen.py d-5-9.cnf 5. 9 2 1 2` will generate the file `split-d-5-9.cnf-2-2-SB-0.icnf`.
This file can then be process with Lingeling (see references) by running

`lingeling split-d-5-9.cnf-2-2-SB-0.icnf -v <cores>`. With 4 cores this job should terminate in a couple of seconds, showing a lower-bound of 11.

Some files for generating visualizations of the colorings are also included, as the one exemplified above.
