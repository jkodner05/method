import sys, re
from os import listdir, walk, makedirs
from os.path import isfile, join, exists, basename
import statistics

indir = sys.argv[1]
outfname = sys.argv[2]
genres = sys.argv[3:-1]
print(sys.argv[-1].split(","))
nums = [int(num) for num in sys.argv[-1].split(",")]

def get_lexicon(infname):
    lemmas = set([])
    with open(infname, "r") as f:
        for line in f:
            lemma = line.split("\t")[0].strip()
            lemmas.add(lemma)
    return lemmas


def get_lexicons(indir, genreext, num):
    lexicons = {}
    for subdir, dirs, fnames in walk(indir):
        for fname in fnames:
            if genreext in fname and "_top"+str(num)+"." in fname and ".txt" in fname:
                infname = join(indir, fname)                
                lexicon = get_lexicon(infname)
                lexicons[fname] = lexicon
    return lexicons


def get_similarities(lexicons1, lexicons2, jaccard=True):
    similarities = {}
    for fname1, lexicon1 in lexicons1.items():
        for fname2, lexicon2 in lexicons2.items():
            if fname1 == fname2 or (fname1, fname2) in similarities or (fname2, fname1) in similarities:
                continue
            intersection = lexicon1 & lexicon2
            union = lexicon1 | lexicon2
            if jaccard:
                similarities[(fname1,fname2)] = len(intersection)/len(union)
            else:
#                similarities[(fname1,fname2)] = len(intersection)/min(len(lexicon1),len(lexicon2))
                similarities[(fname1,fname2)] = len(intersection)/((len(lexicon1)+len(lexicon2))/2)

    return similarities


def print_stats(genres, num, jaccards):
    overlaps = [list(vals.values()) for vals in jaccards.values()]
    overlaps = [val for vals in overlaps for val in vals]
    meanoverlap = statistics.mean(overlaps)
    medianoverlap = statistics.median(overlaps)
    stdevoverlap = statistics.stdev(overlaps)
    maxoverlap = max(overlaps)
    minoverlap = min(overlaps)
    print("\n"+ genres.upper() + "\ttop " + str(num))
    print("------------------------")
    print("mean:\t" + str(round(meanoverlap*100,2)))
    print("median:\t" + str(round(medianoverlap*100,2)))
    print("stdev:\t" + str(round(stdevoverlap*100,2)))
    print("max:\t" + str(round(maxoverlap*100,2)))
    print("min:\t" + str(round(minoverlap*100,2)))



def get_all_similarities(num, genres, lexicons, jaccard):
    intrasimilarities = {}
    intersimilarities = {}
    intercdssimilarities = {}
    internocdssimilarities = {}
    seen = set()
    all_similarities = {}
    if jaccard:
        print("JACCARD------------")
    else:
        print("OVERLAP------------")
    for genre1 in genres:
        for genre2 in genres:
            if (genre2,genre1) in seen:
                continue
            seen.add((genre1,genre2))
            similarities = get_similarities(lexicons[genre1],lexicons[genre2],jaccard)
            if "cds" in genre1 and "cds" in genre2:
                print_stats(genre1 + " x " + genre2,  num, {"":similarities})
            if genre1 == genre2:
                intrasimilarities[(genre1,genre2)] = similarities
            else:
                intersimilarities[(genre1,genre2)] = similarities
                if "cds" in genre1 or "cds" in genre2:
                    intercdssimilarities[(genre1,genre2)] = similarities
                else:
                    internocdssimilarities[(genre1,genre2)] = similarities
            all_similarities[(genre1,genre2)] = similarities
    print_stats("ALL INTRA", num, intrasimilarities)
    print_stats("INTER +CDS", num, intercdssimilarities)
    print_stats("INTER -CDS", num, internocdssimilarities)
    print_stats("ALL INTER", num, intersimilarities)
    print("\n------------------------\n")
    return all_similarities



def main():
    
    with open(outfname, "w") as fout:
        fout.write("lexsize\tfile1\tfile2\tgenre1\tgenre2\tcomptype\tjaccard\toverlap\n")
        for num in nums:
            lexicons = {}
            for genre in genres:
                lexicons[genre] = get_lexicons(indir, genre, num)
            overlaps = get_all_similarities(num, genres, lexicons, False)
            jaccards = get_all_similarities(num, genres, lexicons, True)


            numname = num
            if num == 12000:
                numname = "All"
            for genrepair, similarities in jaccards.items():
                comparisontype = "inter-non-cds"
                if genrepair[0] == "cds" and genrepair[1] == "cds":
                    comparisontype = "intra-cds"
                elif genrepair[0] == genrepair[1]:
                    comparisontype = "intra-non-cds"
                elif genrepair[0] != genrepair[1] and "cds" in genrepair:
                    comparisontype = "inter-cds"
                for files, jaccard in similarities.items():
                    overlap = overlaps[genrepair][files]
                    fout.write(str(numname) +"\t"+ files[0] +"\t"+ files[1] +"\t"+ genrepair[0] +"\t"+ genrepair[1] +"\t"+ comparisontype +"\t"+ str(jaccard) +"\t"+ str(overlap) + "\n")
#            for files, sim in overlaps.items():
#                fout.write("overlap\t" + str(num) +"\t"+ files[0] +"\t"+ files[1] +"\t"+ str(sim) + "\n")


if __name__ == "__main__":
    main()

