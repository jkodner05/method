import sys,re

infname = sys.argv[1]
outfname = sys.argv[2]

def get_lexicon(infname):
    lexicon = {}
    with open(infname, "r") as fin:
        for line in fin:
            lemma = line.split("-")[-1].strip()
            if " " in lemma:
                continue
            if lemma not in lexicon:
                lexicon[lemma] = 0
            lexicon[lemma] += 1
    return lexicon

def write_lexicon(lexicon, outfname):
    sortedlexicon = sorted(lexicon.items(), key=lambda kv : kv[1], reverse=True)

    with open(outfname,"w") as fout:
        for lemma, freq in sortedlexicon:
            fout.write(lemma + "\t" + str(freq) + "\n")

def main():
    lexicon = get_lexicon(infname)
    write_lexicon(lexicon, outfname)

if __name__=="__main__":
    main()

