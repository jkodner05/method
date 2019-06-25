import random
from math import log
import re
from os import listdir
from os.path import isfile, join
import sys

fnames = ["all_IcePaHC_pre1400.txt"]
outfname = sys.argv[1]
infname = "all_IcePaHC_pre1400.txt"

verb_rx = re.compile("\(V\w*\s.*?-(.*?)\)")

strongverbs= {"bíta", "bíða", "dríta", "hníga", "hníta", "rísa", "rísta", "skína", "skíta", "stíga", "svífa", "svíkja", "svíða", "bjóða", "brjóta", "drjúpa", "fjúka", "fljóta", "fljúga", "frjósa", "fyrirbjóða", "gjósa", "gjóta", "hljóta", "hnjósa", "hnjóða", "hrjósa", "hrjóta", "hrjóða", "kjósa", "kljúfa", "krjúpa", "ljósta", "ljúga", "lúka", "lúta", "njóta", "rjóða", "rjúfa", "rjúka", "sjóða", "skjóta", "smjúga", "spýja", "strjúka", "súga", "súpa", "þjóta", "þrjóta", "binda", "bjarga", "bregða", "brenna", "detta", "finna", "gjalda", "hjalpa", "hverfa", "skjalla", "svelga", "svella", "svelta", "svimma", "syngva", "søkkva", "tyggja", "tyggva", "vella", "velta", "verpa", "verða", "vinna", "yfirvinna", "þverra", "bera", "fela", "koma", "nema", "svima", "troða", "vefa", "yfirkoma", "biðja", "eta", "fregna", "gefa", "geta", "kveða", "liggja", "meta", "sitja", "sjá", "vega", "yfirgefa", "þiggja", "aka", "deyja", "draga", "fara", "flá", "gala", "geyja", "hefja", "hlaða", "hlæja", "kala", "klá", "skafa", "skaka", "slá", "standa", "sverja", "taka", "vaxa", "vaða", "yfirtaka", "þvá", "auka", "ausa", "blanda", "blása", "blóta", "búa", "falda", "falla", "fá", "ganga", "gnúa", "gráta", "gróa", "halda", "hanga", "heita", "hlaupa", "hǫggva", "leika", "láta", "ráða", "róa", "snúa", "sveipa", "sá","víkja","gæja","syngja"}
otherja = {"segja","sœkja","eggja","ferja","herja","þjá","synja","netja","virkja","belja","heimsækja","missjá","syfja","grenja","endurnýja","skynja","byrja","sækja", "nýja", "vitja","dysia","brynja","veðja","kynja","kljá",   "svíkja","spýja","sitja","hefja","biðja","sverja","vikja","brytja", "kviðja", "þykkja", "kvíja", "lyfja","sýja",  "tengja", "tortryggja", "heyja"}

shortja_ex = {"segja","ferja","herja","þjá","synja","netja","belja","heimsækja","missjá","syfja","grenja","endurnýja","skynja","byrja","sækja", "nýja", "vitja","dysia","brynja","veðja","kynja","kljá",   "svíkja","spýja","sitja","hefja","biðja","sverja","vikja","brytja", "kviðja", "þykkja", "kvíja", "lyfja","sýja"}
shortja = {"hyggja","leggja","þykja","spyrja","setja","skilja","sækja","vilja","berja","flytja","telja","flýja","selja","verja","kveðja","dvelja","vígja","velja","víkja","semja","þegja","vitja","fremja","tjá","vekja","smyrja","glíkja","krefja","byrja","styðja","ríkja","vefja","lægja","gleðja","hylja","ryðja","bannsetja","ljá","letja","dylja","venja","hrekja","seðja","skynja","knýja","rekja","steðja","vægja","endurnýja","brytja","rækja","samsetja","lemja","flæja","sýkja","þekja","etja","ógleðja","kvelja","týja","þægja","krækja","mægja","líkja","temja","grenja","ryskja","merja","ægja","dysja","drýgja","fresja","hvetja","sýja","nægja","mýkja","svefja","æskja","missjá","stynja","hægja","sannspyrja","átelja","heimsækja","fletja","samkrækja","brynja","kynja","æja","netja","þótja","hrækja","lykja","veðja","hlægja","belja","kvíja","rægja","hugsýkja","gremja","nýja","víðfrægja","klyfja","dynja","spurja","nýsetja","skeðja","kefja","syfja","gæja","skekja","kviðja","kljá","lýja","sekja","sekja", "skekja", "kveykja", "hægja","klyfja", "hnekkja", "víðfrægja", "skeðja", "spurja", "berkja", "ryskja", "þægja", "mægja", "brytja",   "segja","ferja","herja","þjá","synja","netja","belja","heimsækja","missjá","syfja","grenja","endurnýja","skynja","byrja","sækja", "nýja", "vitja","dysia","brynja","veðja","kynja","kljá",   "svíkja","spýja","sitja","hefja","biðja","sverja","vikja","brytja", "kviðja", "þykkja", "kvíja", "lyfja","sýja"}
maybeja = { "nýja","fulltingja","herbergja"}


#weak1shortform = {"þykja", "spyrja", "setja", "skilja", "sækja", "vilja", "berja", "flytja", "telja", "flýja", "selja", "verja", "kveðja", "dvelja", "vígja", "velja", "víkja", "semja", "þegja", "vitja", "fremja", "tjá", "vekja", "smyrja", "glíkja", "krefja", "byrja", "styðja", "ríkja", "vefja", "lægja", "gleðja", "hylja", "ryðja", "bannsetja", "ljá", "letja", "dylja", "venja", "hrekja", "seðja", "skynja", "knýja", "rekja", "steðja", "vægja", "endurnýja", "brytja", "rækja", "samsetja", "lemja", "flæja", "sýkja", "þekja", "etja", "ógleðja", "kvelja", "týja", "þægja", "krækja", "mægja", "líkja", "temja", "grenja", "ryskja", "merja", "ægja", "dysja", "drýgja", "fresja", "hvetja", "sýja", "nægja", "mýkja", "svefja", "æskja", "missjá", "stynja", "hægja", "sannspyrja", "átelja", "heimsækja", "fletja", "samkrækja", "brynja", "kynja", "æja", "netja", "þótja", "hrækja", "lykja", "lyfja", "veðja", "hlægja", "belja", "kvíja", "rægja", "hugsýkja", "gremja", "nýja", "víðfrægja", "klyfja", "dynja", "spurja", "nýsetja", "skeðja", "kefja", "syfja", "gæja", "skekja", "kviðja", "kljá", "lýja", "sekja"}

def add_verbcounts(fname, verbcounts, inflforms):
    print(fname)
    with open(fname, "r") as fin:
        for line in fin:
            match = verb_rx.search(line.strip())
            if match:
#                print(match.group(0), match.group(1))
                verb = match.group(1)
                if verb[-1] != "a" and verb[-1] != "á":
#                    print("excluding: ", verb)
                    continue
                if verb not in verbcounts:
                    verbcounts[verb] = 0
                verbcounts[verb] += 1
                if verb not in inflforms:
                    inflforms[verb] = set()
                inflforms[verb].add(match.group(0))
    return verbcounts, inflforms


def get_verbcounts(fnames):
    verbcounts = {}
    for fname in fnames:
        add_verbcounts(fname, verbcounts)
    return verbcounts

#fnames = [join(dirname,f) for f in listdir(dirname)]

def remove_irreg(sortedverbs, shortonly):
    sortedregulars = []
    for verb, count in sortedverbs:
        if shortonly:
            if verb in shortja and verb not in shortja_ex:
                sortedregulars.append((verb,count))
        else:
            if verb not in strongverbs and verb not in otherja and verb not in shortja_ex:# and verb not in maybeja:
                sortedregulars.append((verb,count))
#            for strongverb in strongverbs:
#                if strongverb in verb:
#                    print(strongverb, verb)
#        else:
#            print(verb)
    return sortedregulars

def remove_nonja(sortedverbs, shortonly):
    sortedja = []
    for verb, count in sortedverbs:
        if shortonly:
            if verb in shortja or verb in shortja_ex:
                sortedja.append((verb,count))
        else:
            if len(verb) > 1 and verb[-2] == "j":
                #        if verb in weak1shortform:
                sortedja.append((verb,count))
    return sortedja


def calc_tp(N,e):
    if N == 1:
        theta = 0
    else:
        theta = N / log(N)
#    print(N, e, round(theta,3), "\t", e < theta)
    return N, e, theta, e < theta


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
                    

verbcounts = {}
inflforms = {}
add_verbcounts(infname, verbcounts, inflforms)
#print(len(verbcounts), verbcounts)
sortedverbs = sorted(verbcounts.items(), key=lambda x: x[1], reverse=True)
print(len(sortedverbs), len(remove_nonja(sortedverbs, False)))


with open(outfname, "w") as fout:
    fout.write("TOTAL" +"\t"+ "SHORTONLY" +"\t"+ "TYPE" +"\t"+ "VAL" +"\t"+ "tolerable" + "\n")
    sumsj = 0
    sumsr = 0

    for samplenum in range(0,1000):
        print("sampling", samplenum)
        sampledverbs = make_sample(sortedverbs,1000)
#        print(sampledverbs)
        sortedsampledverbs = sorted(sampledverbs.items(), key=lambda x: x[1], reverse=True)
#        sortedsampledverbs = sortedverbs[0:1000]
        incr = 50
        for i in range(0,2000+incr,incr):
            sv = sortedsampledverbs[0:min(i,len(sortedsampledverbs))]
            if i > len(sortedsampledverbs):
                break
#            print(len(sv), end="\t")
            for shortonly in (True, False):
                sj = remove_nonja(sv, shortonly)
                sortedregulars = remove_irreg(sj, shortonly)
                if len(sj)-len(sortedregulars):
                    N, e, theta, tolerable = calc_tp(len(sj), len(sj)-len(sortedregulars))
                    fout.write(str(len(sv)) +"\t"+ str(shortonly).upper() +"\t"+str("theta") +"\t"+ str(theta) +"\t"+ str(tolerable).upper() + "\n")
                elif i == 0:
                    fout.write("0" +"\t"+ str(shortonly).upper() +"\t"+ "theta" +"\t"+ "0" +"\t"+ "FALSE" + "\n")
            if i == 1000:
                sumsj += len(sj)/100
                sumsr += len(sortedregulars)/100
    print(sumsj, sumsr, sumsj-sumsr, sumsj/log(sumsj))

#for verb in maybeja:
#    print(verb, inflforms[verb])
