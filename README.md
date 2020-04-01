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
Eliminating the left recursive productions as follows, where e denoting the epsilon

```
E->TE'
E'->+TE'|-TE'|e
T->FT'
T'->*FT'|/FT'|e
F->(E)|id
```






