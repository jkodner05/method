import sys, re

infnames = sys.argv[1:-2]
outfname = sys.argv[-2]
filterfname = sys.argv[-1]


def readlexicon(infname):
    lexicon = {}
    with open(infname, "r") as fin:
        for line in fin:
            lemma, freq = line.strip().split("\t")
            lexicon[lemma] = int(freq)
    return lexicon


def mergelexicons(lexiconlist):
    merged = {}
    for lexicon in lexiconlist:
        for lemma, freq in lexicon.items():
            if lemma not in merged:
                merged[lemma] = 0
            merged[lemma] += freq
    return merged


def write_lexicon(lexicon, outfname):
    sortedlexicon = sorted(lexicon.items(), key=lambda kv : kv[1], reverse=True)

    with open(outfname,"w") as fout:
        for lemma, freq in sortedlexicon:
            fout.write(lemma + "\t" + str(freq) + "\n")


def get_filterset(filterfname):
    filterset = set()
    try:
        with open(filterfname, "r") as fin:
            filterset = set([line.strip() for line in fin])
    except:
        return None
    return filterset
    

def filterlexicon(lexicon, filterset):
    filtered = {}
    for lemma, freq in lexicon.items():
        if lemma in filterset or not filterset:
            filtered[lemma] = freq
    return filtered


def main():
    filterset = get_filterset(filterfname)
    lexicons = [readlexicon(infname) for infname in infnames]
    lexicon = mergelexicons(lexicons)
    filtered = filterlexicon(lexicon, filterset)
    write_lexicon(filtered, outfname)

if __name__=="__main__":
    main()

