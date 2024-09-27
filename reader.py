import os
import functools
dirnow = os.path.dirname(os.path.abspath(__file__))
os.chdir(dirnow)

def load_database(filepath: str, l_is_name: bool): # 加载数据
    info = {}
    for line in open(filepath):
        line = line.strip()[1:-1]
        lpart, rpart = line.split("|")
        if l_is_name:
            info[lpart] = rpart
        else:
            info[rpart] = lpart
    return info

@functools.cache
def get_combined_data(): # 获得联合数据信息
    hom = load_database("HOMFLY-PT-reg.txt", False)
    kho = load_database("khovanov-reg.txt", False)
    vol = load_database("volume_info_list-reg.txt", True)
    combined = {}
    for knotname in hom:
        combined[knotname] = {
            "hom": hom[knotname],
            "kho": kho[knotname],
            "vol": vol[knotname]
        }
    assert len(combined) == 1783
    return combined

def get_kho_stat(): # 仅仅使用 kho 作为区分时的统计信息
    kho_to_name = {}
    for knotname in get_combined_data():
        kho_val = get_combined_data().get(knotname).get("kho")
        if kho_to_name.get(kho_val) is None:
            kho_to_name[kho_val] = []
        kho_to_name[kho_val].append(knotname)
    cnt_stat = {}
    for kho_val in kho_to_name:
        name_list = kho_to_name[kho_val]
        len_now = len(name_list)
        if cnt_stat.get(len_now) is None:
            cnt_stat[len_now] = 0
        cnt_stat[len_now] += 1
    print("get_kho_stat", len(kho_to_name), cnt_stat)

def get_hom_stat(): # 仅仅使用 hom 作为区分时的统计信息
    hom_to_name = {}
    for knotname in get_combined_data():
        hom_val = get_combined_data().get(knotname).get("hom")
        if hom_to_name.get(hom_val) is None:
            hom_to_name[hom_val] = []
        hom_to_name[hom_val].append(knotname)
    cnt_stat = {}
    for hom_val in hom_to_name:
        name_list = hom_to_name[hom_val]
        len_now = len(name_list)
        if cnt_stat.get(len_now) is None:
            cnt_stat[len_now] = 0
        cnt_stat[len_now] += 1
    print("get_hom_stat", len(hom_to_name), cnt_stat)

def get_kho_hom_stat(): # 联合使用 hom 和 kho 作为区分时的统计信息
    com_to_name = {}
    for knotname in get_combined_data():
        hom_val = get_combined_data().get(knotname).get("hom")
        kho_val = get_combined_data().get(knotname).get("kho")
        com_val = "[%s@%s]" % (hom_val, kho_val)
        if com_to_name.get(com_val) is None:
            com_to_name[com_val] = []
        com_to_name[com_val].append(knotname)
    cnt_stat = {}
    for com_val in com_to_name:
        name_list = com_to_name[com_val]
        len_now = len(name_list)
        if cnt_stat.get(len_now) is None:
            cnt_stat[len_now] = 0
        cnt_stat[len_now] += 1
    print("get_kho_hom_stat", len(com_to_name), cnt_stat)

def get_prime_knot_set(): # 返回不考虑手性意义下的素扭结序列, 801 种
    arr = []
    for knotname in get_combined_data():
        if knotname.find(",") == -1 and knotname[0] != "m" and knotname != "K0a1":
            arr.append(knotname)
    return sorted(arr) 

EPS = 1e-4
def get_vol_stat1(): # 基于 volume 的第一种区分方式
    ps = get_prime_knot_set()
    total_cnt = 0
    wrong_cnt = 0
    for i in range(len(ps)):
        for j in range(i):
            vol_i = float(get_combined_data().get(ps[i]).get("vol"))
            vol_j = float(get_combined_data().get(ps[j]).get("vol"))
            if abs(vol_i - vol_j) < EPS:
                wrong_cnt += 1
            total_cnt += 1
    print("get_vol_stat1", "total_cnt:", total_cnt, " wrong_cnt:", wrong_cnt)

def get_col_stat2(): # 基于 volume 的第二种区分方式
    ps = get_prime_knot_set()
    vol_to_name = {}
    for i in range(len(ps)):
        knotname = ps[i]
        vol_val  = float(get_combined_data().get(knotname).get("vol"))
        assert vol_val >= 0
        vol_val  = "%.3f" % vol_val
        if vol_to_name.get(vol_val) is None:
            vol_to_name[vol_val] = []
        vol_to_name[vol_val].append(knotname)
    cnt_stat = {}
    for vol_val in vol_to_name:
        cnt_now = len(vol_to_name[vol_val])
        if cnt_stat.get(cnt_now) is None:
            cnt_stat[cnt_now] = 0
        cnt_stat[cnt_now] += 1
        if cnt_now >= 7:
            assert vol_val == "0.000" # 确实是零等价类
    print("get_col_stat2", len(vol_to_name), cnt_stat)

def main():
    get_kho_stat()
    get_hom_stat()
    get_kho_hom_stat()
    get_vol_stat1()
    get_col_stat2()

if __name__ == "__main__":
    main()