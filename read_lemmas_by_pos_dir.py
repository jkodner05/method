import sys, re
from os import listdir, walk, makedirs
from os.path import isfile, join, exists, basename
from read_lemmas_by_pos import process_file


indir = sys.argv[1]
outdir = sys.argv[2]
maxsetsize = int(sys.argv[3])

def main():
    for subdir, dirs, fnames in walk(indir):
        for fname in fnames:
            infname = join(indir, fname)
            outfname = join(outdir, fname.replace(".txt", "_top" + str(maxsetsize) + ".txt"))
            process_file(infname, outfname, maxsetsize)


if __name__ == "__main__":
    main()
