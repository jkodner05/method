import random
from math import log
import re
from os import listdir
from os.path import isfile, join
import sys

infname = "all_IcePaHC_pre1400.txt"

verb_pret_rx = re.compile("\(VBD\w*\s(.*?)-(.*?)\)")

strongverbs= {"bíta", "bíða", "dríta", "hníga", "hníta", "rísa", "rísta", "skína", "skíta", "stíga", "svífa", "svíkja", "svíða", "bjóða", "brjóta", "drjúpa", "fjúka", "fljóta", "fljúga", "frjósa", "fyrirbjóða", "gjósa", "gjóta", "hljóta", "hnjósa", "hnjóða", "hrjósa", "hrjóta", "hrjóða", "kjósa", "kljúfa", "krjúpa", "ljósta", "ljúga", "lúka", "lúta", "njóta", "rjóða", "rjúfa", "rjúka", "sjóða", "skjóta", "smjúga", "spýja", "strjúka", "súga", "súpa", "þjóta", "þrjóta", "binda", "bjarga", "bregða", "brenna", "detta", "finna", "gjalda", "hjalpa", "hverfa", "skjalla", "svelga", "svella", "svelta", "svimma", "syngva", "søkkva", "tyggja", "tyggva", "vella", "velta", "verpa", "verða", "vinna", "yfirvinna", "þverra", "bera", "fela", "koma", "nema", "svima", "troða", "vefa", "yfirkoma", "biðja", "eta", "fregna", "gefa", "geta", "kveða", "liggja", "meta", "sitja", "sjá", "vega", "yfirgefa", "þiggja", "aka", "deyja", "draga", "fara", "flá", "gala", "geyja", "hefja", "hlaða", "hlæja", "kala", "klá", "skafa", "skaka", "slá", "standa", "sverja", "taka", "vaxa", "vaða", "yfirtaka", "þvá", "auka", "ausa", "blanda", "blása", "blóta", "búa", "falda", "falla", "fá", "ganga", "gnúa", "gráta", "gróa", "halda", "hanga", "heita", "hlaupa", "hǫggva", "leika", "láta", "ráða", "róa", "snúa", "sveipa", "sá","víkja","gæja","syngja"}
otherja = {"segja","sœkja","eggja","ferja","herja","þjá","synja","netja","virkja","belja","heimsækja","missjá","syfja","grenja","endurnýja","skynja","byrja","sækja", "nýja", "vitja","dysia","brynja","veðja","kynja","kljá",   "svíkja","spýja","sitja","hefja","biðja","sverja","vikja","brytja", "kviðja", "þykkja", "kvíja", "lyfja","sýja",  "tengja", "tortryggja", "heyja"}

shortja_ex = {"segja","ferja","herja","þjá","synja","netja","belja","heimsækja","missjá","syfja","grenja","endurnýja","skynja","byrja","sækja", "nýja", "vitja","dysia","brynja","veðja","kynja","kljá",   "svíkja","spýja","sitja","hefja","biðja","sverja","vikja","brytja", "kviðja", "þykkja", "kvíja", "lyfja","sýja"}
shortja = {"hyggja","leggja","þykja","spyrja","setja","skilja","sækja","vilja","berja","flytja","telja","flýja","selja","verja","kveðja","dvelja","vígja","velja","víkja","semja","þegja","vitja","fremja","tjá","vekja","smyrja","glíkja","krefja","byrja","styðja","ríkja","vefja","lægja","gleðja","hylja","ryðja","bannsetja","ljá","letja","dylja","venja","hrekja","seðja","skynja","knýja","rekja","steðja","vægja","endurnýja","brytja","rækja","samsetja","lemja","flæja","sýkja","þekja","etja","ógleðja","kvelja","týja","þægja","krækja","mægja","líkja","temja","grenja","ryskja","merja","ægja","dysja","drýgja","fresja","hvetja","sýja","nægja","mýkja","svefja","æskja","missjá","stynja","hægja","sannspyrja","átelja","heimsækja","fletja","samkrækja","brynja","kynja","æja","netja","þótja","hrækja","lykja","veðja","hlægja","belja","kvíja","rægja","hugsýkja","gremja","nýja","víðfrægja","klyfja","dynja","spurja","nýsetja","skeðja","kefja","syfja","gæja","skekja","kviðja","kljá","lýja","sekja","sekja", "skekja", "kveykja", "hægja","klyfja", "hnekkja", "víðfrægja", "skeðja", "spurja", "berkja", "ryskja", "þægja", "mægja", "brytja",   "segja","ferja","herja","þjá","synja","netja","belja","heimsækja","missjá","syfja","grenja","endurnýja","skynja","byrja","sækja", "nýja", "vitja","dysia","brynja","veðja","kynja","kljá",   "svíkja","spýja","sitja","hefja","biðja","sverja","vikja","brytja", "kviðja", "þykkja", "kvíja", "lyfja","sýja"}
maybeja = { "nýja","fulltingja","herbergja"}


#weak1shortform = {"þykja", "spyrja", "setja", "skilja", "sækja", "vilja", "berja", "flytja", "telja", "flýja", "selja", "verja", "kveðja", "dvelja", "vígja", "velja", "víkja", "semja", "þegja", "vitja", "fremja", "tjá", "vekja", "smyrja", "glíkja", "krefja", "byrja", "styðja", "ríkja", "vefja", "lægja", "gleðja", "hylja", "ryðja", "bannsetja", "ljá", "letja", "dylja", "venja", "hrekja", "seðja", "skynja", "knýja", "rekja", "steðja", "vægja", "endurnýja", "brytja", "rækja", "samsetja", "lemja", "flæja", "sýkja", "þekja", "etja", "ógleðja", "kvelja", "týja", "þægja", "krækja", "mægja", "líkja", "temja", "grenja", "ryskja", "merja", "ægja", "dysja", "drýgja", "fresja", "hvetja", "sýja", "nægja", "mýkja", "svefja", "æskja", "missjá", "stynja", "hægja", "sannspyrja", "átelja", "heimsækja", "fletja", "samkrækja", "brynja", "kynja", "æja", "netja", "þótja", "hrækja", "lykja", "lyfja", "veðja", "hlægja", "belja", "kvíja", "rægja", "hugsýkja", "gremja", "nýja", "víðfrægja", "klyfja", "dynja", "spurja", "nýsetja", "skeðja", "kefja", "syfja", "gæja", "skekja", "kviðja", "kljá", "lýja", "sekja"}


def create_dataset(fname):
    vowelset1 = {"a","au","á","o","ó","u","ú","ö"}
    vowelset2 = {"e","é","ei","ey","i","í","y","ý","æ"}
    vowelset3 = {"ey","æ"}
    vowelset4 = {"e","i","y"}

    verbcounts = {}
    inflforms = {}
    with open(fname, "r") as fin:
        for line in fin:
            match = verb_pret_rx.search(line.strip())
            if match:
#                print(match.group(0), match.group(1), match.group(2))
                verb = match.group(2).lower()
                if verb[-1] != "a" and verb[-1] != "á":
#                    print("excluding: ", verb)
                    continue
                if verb not in verbcounts:
                    verbcounts[verb] = 0
                verbcounts[verb] += 1
                if verb not in inflforms:
                    inflforms[verb] = set()
                inflforms[verb].add(match.group(1).lower())

    sortedverbs = sorted(verbcounts.items(), key=lambda x: x[1], reverse=True)[0:500]
    for verb, count in sortedverbs:
        forms = inflforms[verb]
        vtype = ""
        classes = set()
        if verb in strongverbs:
            vtype = "S"
#        elif verb in shortja_ex:
#            vtype = "2"
#        elif verb in shortja:
#            vtype = "1"
        for v in vowelset1:
            if v in verb[:-1]:
                classes.add("1")
        for v in vowelset2:
            if v in verb[:-1]:
                classes.add("2")
        for v in vowelset3:
            if v in verb[:-1]:
                classes.add("3")
        for v in vowelset4:
            if v in verb[:-1]:
                classes.add("4")
        if not classes: #monosyllabic
            classes.add("0")
        if verb[-2] == "j":
            classes.add("j")
        print(vtype + "\t", verb + "\t", "".join(classes), "\t", inflforms[verb])



def merge_vtypes(labfname, unlabfname):
    lemmas_to_vtypes = {}

    with open(labfname, "r") as f:
        for line in f:
            components = line.split("\t")
            vtype = components[0].strip()
            lemma = components[-2].strip()
            generalizations = components[-1].strip()
            lemmas_to_vtypes[lemma] = vtype

    with open(unlabfname, "r") as f:
        for line in f:
            components = line.split("\t")
            vtype = ""
            if len(components) == 4:
                vtype = components[0].strip()
                if len(vtype) > 1:
                    vtype = ""
            lemma = components[-3].strip()
            generalizations = components[-2].strip()
            infls = components[-1].strip()
            if lemma in lemmas_to_vtypes:
                vtype = lemmas_to_vtypes[lemma]
#                print("\t\tgot ", lemma, vtype)
#            else:
#                if vtype:
#                    print("\tdun got ", lemma, vtype)
#                else:
#                    print("never got ", lemma)
            print(vtype + "\t", lemma + "\t", "".join(generalizations), "\t", infls)

#create_dataset(sys.argv[1])
merge_vtypes("oldis_input.txt", "unlabmodis.txt")
