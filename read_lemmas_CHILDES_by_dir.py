import argparse, re, os
from os.path import basename
from collections import defaultdict
import statistics
import numpy as np
import matplotlib.pyplot as plt

exclude_speakers = set(["CHI", "ROS", "DAV", "ARR", "DAN", "JEN"])
exclude_lemmas = set(["be","not","me","us","you","dog","house","eye","bowl","nose","finger","boot","boat","bicycle","toy","station","zipper","channel","lunch","case","arm","clock","key","spoon","crayon","sock","glove","chicken","shadow","powder","pot","head","market","diaper","toast"])


def plot_lemmas_by_numtypes(numtypes_by_lemma, outfname, language):
    numtypes_by_lemma = sorted(numtypes_by_lemma.items(), key=lambda kv: kv[1], reverse=True)

    y = [float(numtypes) for lemma, numtypes in numtypes_by_lemma if numtypes > 0]
    fig, ax = plt.subplots(figsize=(12,12))
    fig.set_dpi(300)
    ax.bar(range(0,len(y)), y, width=1.0, color="goldenrod")

    fontsize = 40
    fig.suptitle("CHILDES " + language + " PS", fontsize=50)
    ax.tick_params(labelsize=25)
    ax.set_xlabel('Ranked Lemmas', fontsize=fontsize)
    ax.set_ylabel('Infl. Form Type Count', fontsize=fontsize)
    plt.savefig("outputs/" + outfname)
    plt.close(fig)


def plot_infls_by_numlemmas(numlemmas_by_infl, outfname, language):
    numlemmas_by_infl = sorted(numlemmas_by_infl.items(), key=lambda kv: kv[1], reverse=True)

    y = [float(numlemmas) for infl, numlemmas in numlemmas_by_infl if numlemmas > 0]
    fig, ax = plt.subplots(figsize=(12,12))
    fig.set_dpi(300)
    ax.bar(range(0,len(y)), y, width=1.0, color="goldenrod")

    fontsize = 40
    fig.suptitle("CHILDES " + language + " IPS", fontsize=50)
    ax.tick_params(labelsize=25)
    ax.set_xlabel('Ranked Infl. Categories', fontsize=fontsize)
    ax.set_ylabel('Lemma Count', fontsize=fontsize)
    plt.savefig("outputs/" + outfname)
    plt.close(fig)


def parse_file(fname, freqsbymorph, morphsbytype, lemmasbyfeat, POSset, language):

    textlineregex = re.compile(r"^\*[A-Z][A-Z][A-Z]:")
    morphlineregex = re.compile(r"^%mor:")

    poses = set([])

    with open(fname, "r") as f:
        speaker = ""
        for line in f:
            if textlineregex.match(line.strip()):
                textline = line.strip()
                speaker = textline[0:4]
            for excl in exclude_speakers:
                if excl in speaker:
                    continue
            if morphlineregex.match(line.strip()):
                rawwords = line.strip()[6:].split(" ")
                for word in rawwords:
                    parts = word.split("~")
                    for part in parts:
                        lemma = word.split("|")[-1].split("&")[0].split("-")[0]
                        feats = "."
                        try:
                            feats = word.split("|")[-1].split("-")[1]
                            if "=" in feats:
                                feats = feats.split("=")[0]
                        except:
                            pass
                        if lemma in exclude_lemmas:
                            continue
                        POS = part.split("|")[0]
                        if not POSset or POS in POSset:
#                            if "english" in language.lower() and "pl" in feats.lower():
#                                continue
#                                print(part, lemma, feats)

#                            print lemma, POS, POSset
                            freqsbymorph[part] += 1
                            morphsbytype[lemma].add(part)
                            lemmasbyfeat[feats].add(lemma)
#                            morphsbytype[lemma+"_"+POS].add(part)


def count_types(basedir, POSset, language):

    freqsbymorph = defaultdict(int)
    morphsbytype = defaultdict(lambda : set([]))
    lemmasbyfeat = defaultdict(lambda : set([]))

    for subdir, dirs, files in os.walk(basedir):
        for fname in files:
            if ".cha" in fname:
                parse_file(os.path.join(subdir, fname), freqsbymorph, morphsbytype, lemmasbyfeat, POSset, language)
                
    return dict(freqsbymorph), dict(morphsbytype), dict(lemmasbyfeat)


def combine_freqs_bytype(freqsbymorph, morphsbytype, infl):
    freqsbytype = {}
    for word, morphs in morphsbytype.items():
        freqsbytype[word] = 0
        for morph in morphs:
            freqsbytype[word] += freqsbymorph[morph]

    freqsbytypefiltered = {}
    if infl:
        for word, morphs in morphsbytype.items():
            hasinfl = False
            for morph in morphs:
                if infl in morph.lower():
                    hasinfl = True
            if hasinfl:
                freqsbytypefiltered[word] = freqsbytype[word]
    else:
        freqsbytypefiltered = freqsbytype            
                
    return freqsbytypefiltered


def sort_types(freqsbymorph, minfreq):

    filtered_types = {}
    for word, freq in freqsbymorph.items():
        if freq >= minfreq:
            filtered_types[word] = freq

    return sorted(filtered_types.items(), key=lambda kv: kv[1], reverse=True)
    

def writeout(outfname, sortedtypes):
    with open(outfname, "w") as f:
        for word, freq in sortedtypes:
            f.write("%s\t%s\n" % (word, freq))


def invert(morphsbytype):
    numbyinfl = {}
    for lemma, morphs in morphsbytype.items():
        for morph in morphs:
            infl = "-".join(morph.split("=")[0].split("-")[1:])
            if infl not in numbyinfl:
                numbyinfl[infl] = 0
            numbyinfl[infl] += 1
    return numbyinfl

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Get type frequencies from Brown Corpus")

    parser.add_argument("inputdir", nargs="?", help="Brown base directory or subdirectory")
    parser.add_argument("outfile", nargs="?", help="file to write output to")
    parser.add_argument("--pos", nargs="+", help="pos list", type=str)
    parser.add_argument("--minfreq", nargs="?", help="min frquency", type=int, default=0)
    parser.add_argument("--rankcutoff", nargs="?", help="rank cutoff", type=int, default=1000000)
    parser.add_argument("--infl", nargs="?", help="all lemmas must attest this inflectional category", type=str, default="")
    parser.add_argument("--language", nargs="?", type=str, default ="")
    
    args = parser.parse_args()

        
    POSset = None
    if args.pos:
        POSset = set(args.pos)

    freqsbymorph, morphsbytype, lemmasbyfeat = count_types(args.inputdir, POSset, args.language)
    freqsbytype = combine_freqs_bytype(freqsbymorph, morphsbytype, args.infl.lower())

    sortedtypes = sort_types(freqsbytype, args.minfreq)
    sortedtypes = sortedtypes[0:min(len(sortedtypes),args.rankcutoff)]

    writeout(args.outfile, sortedtypes)

    print("# Tokens", sum(freqsbymorph.values()))
    print("# Types", len(sortedtypes))
    morphsbytype_noPOS = {lemma:set([morph.split("|")[1].replace("&","-") for morph in morphs]) for lemma, morphs in morphsbytype.items()}
#    numbyinfl = invert(morphsbytype_noPOS)
    nummorphsbytype = {lemma:len(morphs) for lemma, morphs in morphsbytype_noPOS.items()}
    print("Max PS", max(nummorphsbytype.values()))
    print("Mean PS", statistics.mean(nummorphsbytype.values()))
    print("Median PS", statistics.median(nummorphsbytype.values()))
    plot_lemmas_by_numtypes(nummorphsbytype,basename(args.outfile).replace(".txt",".png"), args.language)
    


    print("# Feats", len(lemmasbyfeat))
    numlemmasbyfeat = {feat:len(lemmas) for feat, lemmas in lemmasbyfeat.items()}
#    print( {feat:lemmas for feat, lemmas in lemmasbyfeat.items()})
    print("Num lemmas", len(nummorphsbytype))
    print("Max IPS", max(numlemmasbyfeat.values()), max(numlemmasbyfeat.values())/len(nummorphsbytype))
    print("Mean IPS", statistics.mean(numlemmasbyfeat.values())/len(nummorphsbytype))
    print("Median IPS", statistics.median(numlemmasbyfeat.values())/len(nummorphsbytype))
    plot_infls_by_numlemmas(numlemmasbyfeat,basename(args.outfile).replace(".txt","_IPS.png"), args.language)
