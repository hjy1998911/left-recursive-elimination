
from collections import defaultdict

EPSILON = "e"

def eliminateLeftRecursive(file, outputfile = None):
    productionList = decodeProductionList(file)

    productionMap = {production.nonterminal:production for production in productionList}
    productionMap = eliminate(productionList, productionMap)

    encodeProductionList(productionMap, outputfile)


def encodeProductionList(produdctionMap, outputfile= None):
    if outputfile == None:
        outputfile = "./production.out"

    with open(outputfile, "w+") as fd:
        for key, production in produdctionMap.items():
            line =  encodeProduction(production)
            fd.write(line)
            fd.write("\n")


    return

def encodeProduction(production):
    left = production.nonterminal
    right = "|".join(production.rightList)

    return  left +  "->" + right


def decodeProductionList(file):

    ans = []

    with open(file) as fd:
        lines = fd.readlines()

        for line in lines:
            if line != "":
                production = decodeProduction(line)
                ans.append(production)

    return  ans

def decodeProduction(line):
    production_rule = line.split("->")
    left, right_rule = production_rule[0], production_rule[1]

    production = Production().left(left)

    rights = right_rule.split("|")

    production.right([right.strip() for right in rights])

    return production

class Production():
    def __init__(self):
        self.nonterminal = None

        self.rightList = []

    def left(self, nonterminal):
        self.nonterminal = nonterminal
        return self

    def right(self, rightDerivations):
        if isinstance(rightDerivations, list):
            self.rightList.extend(rightDerivations)
        else:
            self.rightList.append(rightDerivations)

        return self

    def isLeftRecursive(self):
        for rightDerive in self.rightList:
            if self.__isLeftRecursive(rightDerive):
                return True

        return False

    def __isLeftRecursive(self, right):
        return right[0] == self.nonterminal


    def getLeftRecursiveProduction(self):
        return [ right for right in self.rightList if self.__isLeftRecursive(right)]

    def getNonLeftRecursiveProduction(self):
        return [right for right in self.rightList if not self.__isLeftRecursive(right)]


def getAllNonterminals(productionList):
    return  [production.nonterminal for production in productionList]



# recording pair of Ai, Aj such that Ai->AjW, where w is a string of symbols
def nonterminalPair(prodcutionList):
    nonterminalPairMap = defaultdict(list)
    nonterminals = getAllNonterminals(prodcutionList)
    for production in prodcutionList:
        for right in production.rightList:
            if len(right) > 0 and right[0] in nonterminals:
                nonterminalPairMap[(production.nonterminal, right[0])].append(right)

    return nonterminalPairMap

def replaceAj(leftNonterminal, rightNonterminal, rights, productionMap):
    replaceProductionList = productionMap[rightNonterminal].rightList

    newProductionList = []
    for right in rights:
        for replaceProduction in replaceProductionList:
            newproduction = replaceProduction + right[1:]
            newProductionList.append(newproduction)

    oldProdcution = productionMap[leftNonterminal]

    new = genNewProduction(oldProdcution, newProductionList, leftNonterminal, rightNonterminal)

    productionMap[new.nonterminal] = new



def genNewProduction(oldProduction , newProducitonList, leftNonterminal, rightNonterminal):
    newrights = newProducitonList

    for right in oldProduction.rightList:
        if right[0] != rightNonterminal:
            newrights.append(right)

    return  Production().left(leftNonterminal).right(newrights)


def eliminate(productionList, productionMap):
    nonterminalList = getAllNonterminals(productionList)

    pairMap = nonterminalPair(productionList)
    for i in range(len(nonterminalList)):
        Ai = nonterminalList[i]
        for j in range(0, i):
            Aj = nonterminalList[j]
            rights = pairMap[(Ai, Aj)]
            if rights != None:
                ## for each Ai->AjW, repace Ai->AjW to Ai->w1W|w2W ... such that Aj->w1|w2.//
                replaceAj(Ai, Aj, rights,  productionMap)

        production = productionMap[Ai]
        if production.isLeftRecursive():
            production1, production2 = eliminateAiRecursive(productionMap[nonterminalList[i]])

            productionMap[production1.nonterminal] = production1
            productionMap[production2.nonterminal] = production2
    return productionMap


## For each Ai->AiW | w1 | w2 |w3 , replace it to equivalent rules
## such that Ai-> w1A'|w2A';  A'->WA' | epsilon
def eliminateAiRecursive(production):
    leftRecursiveList = production.getLeftRecursiveProduction()
    nonLeftRecursiveList = production.getNonLeftRecursiveProduction()

    newProduction1 = Production().left(production.nonterminal)
    newNonterminal = production.nonterminal + "'"

    for nonLeftRecursive in nonLeftRecursiveList:
        newProduction1.right(nonLeftRecursive + newNonterminal)

    newProduction2 = Production().left(newNonterminal).right(EPSILON)

    for leftRecursive in leftRecursiveList:
        newProduction2.right(leftRecursive[1:] + newNonterminal)


    return (newProduction1, newProduction2)



