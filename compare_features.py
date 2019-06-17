import sys, re
from os import listdir, walk, makedirs
from os.path import isfile, join, exists, basename
import statistics
from compare_lexicons import get_lexicons
from math import log

indir = sys.argv[1]
outfname = sys.argv[2]
featfname = sys.argv[3]
genres = sys.argv[4:-1]
nums = [int(num) for num in sys.argv[-1].split(",")]

def read_featured(featfname):
    featureds = set()
    with open(featfname, "r") as f:
        for line in f:
            featureds.add(line.lower().strip())
    return featureds


def get_featuredcounts(lexicons, featureds):
    featuredcounts = {}
    for fname, lexicon in lexicons.items():
        print(featureds)
        numfeatured = len(lexicon & featureds)
        featuredcounts[fname] = (numfeatured, len(lexicon)-numfeatured)
    return featuredcounts


def main():
    featuredlist = read_featured(featfname)
    with open(outfname, "w") as fout:
        fout.write("lexsize\tfname\tgenre\ttypecount\tallcount\tis_adult\tis_nonacad\ttheta\tprod\n")
        for num in nums:
            intrajaccards = {}
            interjaccards = {}
            lexicons = {}
            featuredcounts = {}
            print("top"+str(num))
            for genre in genres:
                genrelexicons = get_lexicons(indir, genre, num)
                lexicons[genre] = genrelexicons
                featuredcounts[genre] = get_featuredcounts(genrelexicons, featuredlist)
    #            print(featuredcounts[genre])
                positives = [numfeat for numfeat, numnot in featuredcounts[genre].values()]
                mean = statistics.mean(positives)
                stdev = statistics.stdev(positives)
                print(genre + "\tmean " + str(round(mean,4)) + "\tstdev " + str(round(stdev,4))  + "\t" + str(min(positives)) + "\t" + str(max(positives)))
            allfeaturedcounts = set()
            for genre, vals in featuredcounts.items():
                numfeats = set([first for first, second in vals.values()])
                allfeaturedcounts = allfeaturedcounts | numfeats
            mean = statistics.mean(allfeaturedcounts)
            stdev = statistics.stdev(allfeaturedcounts)
            print("ALL" + "\tmean " + str(round(mean,4)) + "\tstdev " + str(round(stdev,4)) + "\t" + str(min(allfeaturedcounts)) + "\t" + str(max(allfeaturedcounts)) + "\n")

            numname = num
            if num == 12000:
                numname = "All"
            for genre, featcounts in featuredcounts.items():
                for fname, featcount in featcounts.items(): 
                    e = featcount[0]
                    N = len(lexicons[genre][fname])
                    theta = 1
                    if N > 1:
                        theta = N/log(N)
                    prod = str(e < theta).upper()
                    fout.write(str(numname) + "\t" + fname + "\t" + genre + "\t" + str(featcount[0]) + "\t" + str(len(lexicons[genre][fname])) + "\t" + str(genre != "cds") + "\t" + str(genre != "acad") + "\t" + str(theta) + "\t" + prod + "\n")

if __name__ == "__main__":
    main()
