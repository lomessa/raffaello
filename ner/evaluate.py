

import codecs


def evaluate_ner(res,benchmark):
    allcur = []
    allres = []
    for k in benchmark.keys():
        curres = res[k]
        benchres = benchmark[k]
        allcur.extend(curres)
        allres.extend(benchres)
        eres = calc_rec_pre(curres,benchres)
        print("for ner type" + k )
        print( "the precision is %f, the recall is %f" %(eres[0],eres[1]))

    ares = calc_rec_pre(allcur,allres)
    print("the overall precision is %f, the recall is %f" % (ares[0], ares[1]))


def calc_rec_pre(res,ans):
    right = 0
    for r in res:
        if r in ans:
            right = right + 1
    if len(res) == 0:
        return (0,0)
    return (right/len(res),right/len(ans))

if __name__ == '__main__':

    ansdict,curdict ={"STORE":[]
                      ,"DISH":[],"CATEGORY":[],"LOCATION":[]},{"STORE":[]
                      ,"DISH":[],"CATEGORY":[],"LOCATION":[]}
    with codecs.open('/Users/zihe.zhan/Workspace/py_script/ner/ner_benchmark_res11','r','utf-8') as reader:
        number = 1
        for line in reader.readlines():
            if number > 200:
                continue
            terms = line.strip().split("\t")
            ans,res = [],[]
            if len(terms) > 1:
                ans = terms[1].strip().split(",")
            if len(terms) > 2:
                res = terms[2].strip().split(",")
            for a in ans:
                if a!="":
                    typens = a.strip().split("|")[1:]
                    for typen in typens:
                        if typen not in ansdict:
                            continue
                        ansdict[typen ].append(str(number) + a.strip().split("|")[0])
            for a in res:
                if a!="":
                    typens = a.strip().split("|")[1:]
                    for type in typens:
                        if typen not in ansdict:
                            continue
                        curdict[typen].append(str(number) + a.strip().split("|")[0])
            number = number  + 1

    evaluate_ner(curdict,ansdict)


