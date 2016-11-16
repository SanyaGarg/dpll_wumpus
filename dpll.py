from collections import Counter,defaultdict

def sign(a):
    if a>0:
        return True
    return False
        
class Solver:
    def __init__(self, cnf):
        self.sentence= cnf
        self.model={}.fromkeys(abs(item) for sublist in cnf for item in sublist)

    def reduce(self, sentence, p):
        newsentence=[]
        for clause in sentence:
            if p in clause:
                continue
            if -p in clause:
                newsentence.append(clause.copy())
                newsentence[-1].remove(-p)
                continue
            newsentence.append(clause.copy())
        return newsentence

    def dpll(self, sentence, unassigned):
        # print("sentence:", sentence)

        for clause in sentence:
            if len(clause)==1:
                (unitlit,)=clause
                # print("unitlit:",unitlit)
                unassigned.remove(abs(unitlit))
                i=0
                while i!=len(sentence):
                    if unitlit in sentence[i]:
                        sentence.pop(i)
                        continue
                    if -unitlit in sentence[i]:
                        sentence[i].remove(-unitlit)
                    i+=1
                return self.dpll(sentence, unassigned.copy())
        
        #pure literal elimination is slow
        # unionlits=set()
        # [unionlits.update(clause) for clause in sentence]
        # for lit in unionlits:
            # if -lit not in unionlits:
                # unassigned.remove(abs(lit))
                # i=0
                # while i!=len(sentence):
                    # if lit in sentence[i]:
                        # sentence.pop(i)
                        # continue
                    # i+=1

        if not sentence:
            return True
        for clause in sentence:
            if len(clause)==0:
                return False

        #Short clause. pick first literal from short clause
        # tmp=[(i,len(clause)) for i,clause in enumerate(sentence)]
        # p=next(iter(sentence[sorted(tmp,key= lambda x:x[1])[0][0]]))

        #Most occuring literal
        cnt=Counter()
        [cnt.update(clause) for clause in sentence]
        p= cnt.most_common(1)[0][0]
        unassigned.remove(abs(p))

        return self.dpll(self.reduce(sentence,p),unassigned.copy()) or \
        self.dpll(self.reduce(sentence, -p),unassigned.copy())

    def solve(self):
        unassigned= set(self.model.keys())
        return self.dpll(self.sentence,unassigned.copy())


alphasat=[{1,2,3},{-1,3},{4},{-4,-3}]
alphaunsat=[{1,2},{-1,2},{-1,-2},{1,-2}]

print(Solver(alphasat).solve())
print(Solver(alphaunsat).solve())

