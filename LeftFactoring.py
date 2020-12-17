# 3. Write a program to identify does a grammar is left recursive or right recursive
# 4. Write a program to convert left recursive grammar to right recursive grammar

import sys
import re
import time
sys.setrecursionlimit(60)


def isTerm(ter):
    if ter == '#':
        return True

    for t in terms:
        if ter == t:
            return True

    return False


def isNTerm(nT):
    for nt in nonterms:
        if nT == nt:
            return True
    return False


def LeftCheck(nT, search, escape):
    # print("NT:-"+nT+",Search:-"+search)
    # time.sleep(3)
    for prod in production_dict[nT]:
        if search == prod[0]:
            leftcheck_list[search].append(nT)
            return True
        else:
            if isNTerm(prod[0]):
                return LeftCheck(prod[0], search, escape+1)
            else:
                escape = 0
                continue
    return False


def RightCheck(nT, search):
    # print("NT:-"+nT+",Search:-"+search)
    for prod in production_dict[nT]:
        if search == prod[len(prod)-1]:  # Direct
            return True
    return False


def Left_toRight(nT):
    bet = []
    alpha = []
    #expand on indirect relations
    for nont in leftcheck_list[nt]:
        if nont != nT:
            for i in range(0, len(production_dict[nT])):
                prod = production_dict[nT][i]
                if(nont == prod[0]):
                    prod_temp = prod
                    remain = prod[1:]
                    for p in production_dict[nont]:
                        if nT == p[0]:
                            final_prod = p + remain
                            production_dict[nT].pop(i)
                            production_dict[nT].insert(i, final_prod)

    #remove Direct Left recursion
    for prd in production_dict[nT]:
        if nT == prd[0]:
            alpha.append(prd[1:])
        else:
            bet.append(prd)

    gram_dash = ""
    for a in alpha:
        gram_dash = gram_dash + a + nT + '\'' + "/"
    gram_dash = gram_dash[0:-1]
    gram = ""
    for b in bet:
        gram = gram+b+nT+'\''+"/"
    gram = gram[0:-1]
    print(nT+"->"+gram)
    print(nT+"\'->"+gram_dash+"/#")


def Prod_print(nT):
    full_prod = ""
    for pd in production_dict[nT]:
        full_prod = full_prod+pd+"/"
    full_prod = full_prod[0:-1]
    print(nT+"->"+full_prod)


productions = []

n = input("Enter the number of Productions:-")

n = int(n)
print("\nRules:\n--------------------------------------------------------------------------------------\nEpsilon is represented by  # \nProductions are of the form A->B, where ‘A’ is a single Non-Terminal and ‘B’ can be any combination of Terminals and Non - Terminals.\nTerminals with only single characters work\nDO NOT use the same char for terminal and non terminal.\nDo not use # or $ as they are reserved for special purposes.\n\n")

for i in range(n):
    prod = input()
    prod.strip()
    productions.append(prod)

nonterms = []
terms = []

#Since Productions are context free grammaer there is only one nonterminal on the left and then an arrow so we can check for terms after the arrow

#Finding Non Terminals:-
for i in range(n):
    nonterms.append(productions[i][0])

#Finding Terminals:-

for i in productions:
     for j in range(3, len(i)):
          check = True
          for nt in nonterms:
              if i[j] == nt or i[j] == '#' or i[j] == '/':
                  check = False
          if check:
              terms.append(i[j])

print("Non Terminals:-", nonterms)
print("Terminals:-", terms)
print("Productions:-", productions)

#Production Dict
production_dict = {}
for nt in nonterms:
    production_dict[nt] = []

# split the productions into parts to simplify parsing
for production in productions:
    nonterminal_to_production = production.split("->")
    expanded = nonterminal_to_production[1].split(
        "/")  # assumption : single char terminals
    for ex in expanded:
        production_dict[nonterminal_to_production[0]].append(ex)

print("production_dict", production_dict)


leftcheck_dict = {}
leftcheck_list = {}  # Stores the non terminals which have indirect left recursion
for nt in nonterms:
    leftcheck_list[nt] = []
    leftcheck_dict[nt] = LeftCheck(nt, nt, 0)

rightcheck_dict = {}

for nt in nonterms:
    rightcheck_dict[nt] = RightCheck(nt, nt)

print("\n")
for nt in nonterms:
    if leftcheck_dict[nt]:
        print(nt+" contains Left Recursive Grammar")
    if rightcheck_dict[nt]:
        print(nt+" contains Right Recursive Grammar")

print("--------------------------------\nLeft Eliminated Grammer:-")
for nt in nonterms:
    if leftcheck_dict[nt] == True:
        Left_toRight(nt)
    else:
        Prod_print(nt)
