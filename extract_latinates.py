import sys, re

infname = sys.argv[1]
outfname = sys.argv[2]

unlink_rename_rx = re.compile(r"\[\[[:#\w\s\(\)]+\|(\w+)\]\]")
unlink_simple_rx = re.compile(r"\[\[(\w+)\]\]")

def clean_deriv(rawderiv):
    deriv = rawderiv.strip()
    ur_match = unlink_rename_rx.match(deriv)
#    if "|" in deriv:
#        print(deriv)
    if ur_match:
        deriv = ur_match.group(1).strip()
    s_match = unlink_simple_rx.match(deriv)
    if s_match:
        deriv = s_match.group(1).strip()
#    if rawderiv.strip() != deriv:
#        print(deriv, rawderiv)
    
    return deriv.lower()


def read_wikifile(infname):
    with open(infname, "r") as f:
        allderivs = []
        for line in f:
            if line and line[0] == "|":
                line = line.replace(" | ", " || ").replace("||", "@")
                rawderivs = line.split("@")[-1].split(",")
                derivs = [clean_deriv(deriv) for deriv in rawderivs]
                derivs = [deriv for deriv in derivs if deriv]
                allderivs.extend(derivs)

#    print(allderivs)
    return set(allderivs)


def get_polysyllables(allderivs):

    contract_rx = re.compile(r"([aeiou])[aeiou]+")
    polyderivs = set()
    for deriv in allderivs:
        pderiv = contract_rx.sub("V", deriv[:-1]).replace("a","V").replace("e","V").replace("i","V").replace("o","V").replace("u","V")
        if pderiv.count("V") >= 2:
            polyderivs.add(deriv)
#        else:
#            print(deriv, pderiv)
    return polyderivs


def main():
    allderivs = read_wikifile(infname)
    polysyllabic = get_polysyllables(allderivs)
    print(polysyllabic)
    with open(outfname, "w") as f:
        for elem in polysyllabic:
            f.write(elem+"\n")
    return

if __name__=="__main__":
    main()
