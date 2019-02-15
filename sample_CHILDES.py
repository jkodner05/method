import sys, re, random
from os import listdir, walk, makedirs
from os.path import isfile, join, exists, basename
from read_lemmas_sample import write_samples
random.seed("falesa")

infname = sys.argv[1]
outdir = sys.argv[2]
numsamples = int(sys.argv[3])
samplesizes = [int(arg) for arg in sys.argv[4:-1]]
outprefix = sys.argv[-1]

def main():

    lemmafreqs = {}
    with open(infname, "r") as fin:
        for line in fin:
            lemma = line.split("\t")[0].strip()
            freq = int(line.split("\t")[1].strip())
            lemmafreqs[lemma] = freq

    write_samples(lemmafreqs, samplesizes, numsamples, outprefix)

if __name__ == "__main__":
    main()
