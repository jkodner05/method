import sys, re, random
from os import listdir, walk, makedirs
from os.path import isfile, join, exists, basename
from read_lemmas_by_pos import read_lemmas

random.seed("falesa")

indir = sys.argv[1]
outdir = sys.argv[2]
numsamples = int(sys.argv[3])
samplesizes = [int(arg) for arg in sys.argv[4:-1]]
outprefix = sys.argv[-1]

def merge_freqs(alllemmafreqs, filelemmafreqs):
    for lemma, freq in filelemmafreqs.items():
        if lemma not in alllemmafreqs:
            alllemmafreqs[lemma] = 0
        alllemmafreqs[lemma] += freq
    return alllemmafreqs
        

def get_sample(lemmalist, samplesize):
    sampleds = {}
    while len(sampleds) < samplesize:
        lemma = random.choice(lemmalist)
        if lemma not in sampleds:
            sampleds[lemma] = 0
        sampleds[lemma] += 1
    return sampleds


def write_samples(lemmafreqs, samplesizes, numsamples, outprefix):

    print("Making samples")
    lemmalist = []
    for lemma, freq in lemmafreqs.items():
        lemmalist.extend([lemma]*freq)

    for samplenum in range(numsamples):
        print("Sample #", samplenum)
        sample = get_sample(lemmalist, max(samplesizes))
        sortedsample = sorted(sample.items(), key=lambda kv : kv[1], reverse=True)
        for samplesize in samplesizes:
            subsample = sortedsample[0:samplesize]
            with open(join(outdir, outprefix + "_" + str(samplenum) + "_top" + str(samplesize) + ".txt"), "w") as fout:
                for lemma, freq in subsample:
                    fout.write(lemma + "\t" + str(freq) + "\n")


def main():

    lemmafreqs = {}
    print("Making lemma token dict")
    for subdir, dirs, fnames in walk(indir):
        i = 0
        for fname in fnames:
            print(str(i) + " of " + str(len(fnames)))
            i += 1
#            if i == 3:
#                break
            infname = join(indir, fname)
            merge_freqs(lemmafreqs, read_lemmas(infname))

    write_samples(lemmafreqs, samplesizes, numsamples, outprefix)

if __name__ == "__main__":
    main()
