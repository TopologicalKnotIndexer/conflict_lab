from reader import get_prime_knot_set

def get_dict_by_crossing():
    dic = {}
    for item in get_prime_knot_set():
        mcr = item
        while mcr[0] in ['k', 'K', 'm', 'M']:
            mcr = mcr[1:]
        mcr = int(mcr.split("n")[0].split("a")[0])
        if dic.get(mcr) is None:
            dic[mcr] = []
        dic[mcr].append(item)
    return dic

if __name__ == "__main__":
    dic = get_dict_by_crossing()
    for mcr in range(3, 12):
        print("minimal crossing number: %2d => %3d knot(s)" % (mcr, len(dic[mcr])))