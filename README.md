# left-recursive-elimination
Implement an algorithm to eliminate the left recursive production. The left recursive production can not be used to LL algorithm, so it is necessary to eliminate the left recursive beforing applying the LL algorithm.

# How to use
```
from leftrecursiveelimination import eliminateLeftRecursive

eliminateLeftRecursive("./expression", "./expression.out")
```

# Example

Expression as follows

```
E->E+T|E-T|T
T->T*F|T/F|F
F->(E)|id
```
Eliminating the left recursive productions as follows

```
T'->e|*FT'|/FT'
E'->e|+TE'|-TE'
E->TE'
T->FT'
F->(E)|id
```






