import random
from math import log
import re
from os import listdir
from os.path import isfile, join
import sys

infnames = ["oldis_input.txt", "modis_input.txt"]
outfname = sys.argv[1]

def get_vtypecnts_by_gen(verbgens, verbtypes):
    vtypecnts_by_gen = {}
    for verb, gens in verbgens.items():
        for gen in gens:
            if gen not in vtypecnts_by_gen:
                vtypecnts_by_gen[gen] = {}
            vtype = verbtypes[verb]
            if vtype not in vtypecnts_by_gen[gen]:
                vtypecnts_by_gen[gen][vtype] = 0
            vtypecnts_by_gen[gen][vtype] += 1
    return vtypecnts_by_gen


def read_verbfile(infname, maxverbs=100000):
    verbcounts = {}
    verbtypes = {}
    verbgens = {}
    with open(infname, "r") as fin:
        for i, line in enumerate(fin):
            if i == maxverbs:
                break
            components = line.split()
            count = int(components[0].strip())
            vtype = components[1].strip()
            lemma = components[2].strip()
            generalizations = set(components[3].strip())
            verbcounts[lemma] = count
            verbtypes[lemma] = vtype
            verbgens[lemma] = generalizations
    return verbcounts, verbtypes, verbgens


def calc_tp(N,e):
    if N == 1:
        theta = 0
    else:
        theta = N / log(N)
#    print(N, e, round(theta,3), "\t", e < theta)
    return N, e, theta, e < theta


def do_nonsample_calcs(vtypecnts_by_gen):
    for gen, cnts in vtypecnts_by_gen.items():
        print("Generalization: ", gen)
        for vtype, cnt in cnts.items():
            N, e, theta, tolerable = calc_tp(cnt, sum(cnts.values())-cnt)
#            if tolerable:
            print("\t", vtype, N, e, round(theta,2), "\t", tolerable)
    print("")

#for i in range(50,750,50):
#    print()
#    print()
#    print(i)
#    verbcounts, verbtypes, verbgens = read_verbfile(infname, i)
#    vtypecnts_by_gen = get_vtypecnts_by_gen(verbgens)
#    do_nonsample_calcs(vtypecnts_by_gen)
#exit()


def get_sample(lemmalist, samplesize):
    sampleds = {}
    while len(sampleds) < samplesize:
        lemma = random.choice(lemmalist)
        if lemma not in sampleds:
            sampleds[lemma] = 0
        sampleds[lemma] += 1
    return sampleds


def make_sample(lemmafreqs, samplesize):
    samplinglist = []
    for lemma, freq in lemmafreqs:
        samplinglist.extend([lemma]*freq)
    sample = get_sample(samplinglist, samplesize)
    return sample
    

def write_samples(lemmafreqs, samplesizes, numsamples, outprefix):

    print("Making samples")
    lemmalist = []
    sortedlemmafreqs = sorted(lemmafreqs.items(), key=lambda kv : kv[1], reverse=True)[0:min(len(lemmafreqs), 1500)]
    for lemma, freq in sortedlemmafreqs:
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
                    



with open(outfname, "w") as fout:
    fout.write("ERA" + "\t" + "TOTAL" +"\t"+ "GEN" +"\t"+ "TYPE" +"\t"+ "VAL" +"\t"+ "tolerable" + "\n")
    for infname in infnames:
        verbcounts, verbtypes, verbgens = read_verbfile(infname)
        sortedverbs = sorted(verbcounts.items(), key=lambda x: x[1], reverse=True)
        types = set()
        gens = set()
        for verb, vgens in verbgens.items():
            for gen in vgens:
                gens.add(gen)
        for verb, vtype in verbtypes.items():
            types.add(vtype)

        print(len(sortedverbs))#, len(remove_nonja(sortedverbs, False)))
        print(types)
        print(gens)

        for samplenum in range(0,1000):
            print("sampling", samplenum)
            sampledverbs = make_sample(sortedverbs,700)
    #        print(sampledverbs)
            sortedsampledverbs = sorted(sampledverbs.items(), key=lambda x: x[1], reverse=True)
    #        sortedsampledverbs = sortedverbs[0:1000]
            incr = 50
            for i in range(0,700+incr,incr):
                sv = dict(sortedsampledverbs[0:min(i,len(sortedsampledverbs))])
                if i > len(sortedsampledverbs):
                    break
                svgens = {}
                for verb in sv:
                    svgens[verb] = verbgens[verb]
                vtbyg = get_vtypecnts_by_gen(svgens,verbtypes)
                for gen, tcnts in vtbyg.items():
                    for t, tcnt in tcnts.items():
                        N, e, theta, tolerable = calc_tp(tcnt, sum(tcnts.values())-tcnt)
                        fout.write(infname + "\t" + str(len(sv)) +"\t"+ gen +"\t"+ t +"\t"+ str(theta) +"\t"+ str(tolerable).upper() + "\n")
    #            for shortonly in (True, False):
    #                sj = remove_nonja(sv, shortonly)
    #                sortedregulars = remove_irreg(sj, shortonly)
    #                if len(sj)-len(sortedregulars):
    #                    N, e, theta, tolerable = calc_tp(len(sj), len(sj)-len(sortedregulars))
    #                    fout.write(str(len(sv)) +"\t"+ str(shortonly).upper() +"\t"+str("theta") +"\t"+ str(theta) +"\t"+ str(tolerable).upper() + "\n")
    #                elif i == 0:
    #                    fout.write("0" +"\t"+ str(shortonly).upper() +"\t"+ "theta" +"\t"+ "0" +"\t"+ "FALSE" + "\n")
    #            if i == 1000:
    #                sumsj += len(sj)/100
    #                sumsr += len(sortedregulars)/100
    #    print(sumsj, sumsr, sumsj-sumsr, sumsj/log(sumsj))

    #for verb in maybeja:
    #    print(verb, inflforms[verb])
