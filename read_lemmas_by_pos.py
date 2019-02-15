import sys, re

infname = sys.argv[1]
outfname = sys.argv[2]
#posset = set(sys.argv[3].split(","))
maxsetsize = int(sys.argv[3])

def is_valid(lemma):
    notletter_rx = re.compile(r"[^a-z-]")
    triples_rx = re.compile(r"(aaa|bbb|ccc|ddd|eee|fff|ggg|hhh|iii|jjj|kkk|lll|mmm|nnn|ooo|ppp|qqq|rrr|sss|ttt|uuu|vvv|www|xxx|yyy|zzz)")
    if lemma == "'s":
        return lemma
    elif lemma == "'ve":
        return "have"
    elif lemma == "n't":
        return "not"


    if not lemma:
        return False
    elif notletter_rx.search(lemma):
#        if len(lemma) > 1:
#            print(lemma)
        return False
    elif triples_rx.search(lemma):
#        if len(lemma) > 1:
#            print(lemma)
        return False
    elif lemma[0] == "-" or lemma[-1] == "-" or (len(lemma) > 1 and lemma[-2] == "-") or lemma.count("-") > 1:
        if "-and-" in lemma or "-to-" in lemma or "-the-" in lemma or "-of-" in lemma:
            return lemma
#        if len(lemma) > 1:
#            print(lemma)
        return False
    elif len(lemma) > 7 and lemma[-3:] == "ing": #gets rid of spurious VVG
        return False    

    return lemma

def read_lemmas(infname):
    lemmafreqs = {}
    # COCA word lemma POS format
    # http://ucrel.lancs.ac.uk/claws7tags.html
    with open(infname, "rb") as f:
        for line in f:
            components = [comp.strip() for comp in line.decode("utf-8", "ignore").split("\t")]
            if len(components) < 3:
                continue
            word = components[0]
            pos = components[2]
            if not pos or pos[0] != "v":
                continue
            lemma = is_valid(components[1].lower())
            if not lemma:
                continue
#            if pos not in posset:
#                continue
            if lemma not in lemmafreqs:
                lemmafreqs[lemma] = 0
            lemmafreqs[lemma] += 1
    return lemmafreqs


def get_freqset(lemmafreqs, maxsetsize):
    setsize = maxsetsize+1
    freqcutoff = 0
    while setsize > maxsetsize:
        freqset = {lemma:freq for lemma, freq in lemmafreqs.items() if freq >= freqcutoff}
        if len(freqset) <= maxsetsize:
            break
        freqcutoff += 1
    
    print("Frequency cutoff:\t", freqcutoff)
    print("Set size:\t\t", len(freqset))
    return freqset
          

def process_file(infname, outfname, maxsetsize):
    lemmafreqs = read_lemmas(infname)
    sortedlemmas = sorted(lemmafreqs.items(), key=lambda kv : kv[1], reverse=True)[0:min(len(lemmafreqs),maxsetsize)]
    print(len(sortedlemmas))
#    freqset = get_freqset(lemmafreqs, maxsetsize)
#    sortedlemmas = sorted(freqset.items(), key=lambda kv : kv[1], reverse=True)
    with open(outfname, "w") as fout:
        for lemma, freq in sortedlemmas:
            fout.write(lemma + "\t" + str(freq) + "\n")

def main():
    process_file(infname, outfname, maxsetsize)

if __name__ == "__main__":
    main()

