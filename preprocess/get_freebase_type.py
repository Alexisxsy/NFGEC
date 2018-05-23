import re
from collections import defaultdict, Counter
def get_type_map(fname):
    with open(fname, "r", encoding="utf-8") as f:
        type_map = {}
        type_set =set()
        for line in f:
            org, figer = line.strip().split("\t")
            type_map[org] = figer
            type_set.add(figer)
    print("[INFO] number of Freebase type:{}, number of figer type:{}".format(len(type_map.keys()), len(type_set)))

    return type_map

def get_ftype_map(fname, fsave):
    with open(fname, "r", encoding="utf-8") as f:
        name_ftype_map = defaultdict(set)
        ftype_counter = Counter()
        figer_counter = Counter()
        for line in f:
            tokens = line.strip().split("\t")
            if len(tokens) < 3:
                continue
            sub, prd, obj = tokens[:3]

            #some of this string occur in sub or obj
            if "type.object.type" not in prd:
                continue

            m = re.match(r"m.*", sub.split("/")[-1][:-1])
            if not m: 
                continue
            sub = "/" + m.group().replace(".", "/")
            
            obj = "/" + obj.split("/")[-1][:-1].replace(".","/")

            name_ftype_map[sub].add(obj)
            ftype_counter[obj] += 1

            if obj in type_map.keys():
                figer_counter[obj] += 1

    print("[INFO] number of entities:{}".format(len(name_ftype_map.keys())))
    print("[INFO] number of unique type:{}".format(len(ftype_counter)))
    print("[INFO] number of unique type in figer map:{}".format(len(figer_counter)))

    ft_sum = 0
    fi_sum = 0
    for v in ftype_counter.values():
        if v >= 5:ft_sum += 1
    for v in figer_counter.values():
        if v >= 5: fi_sum += 1
    print("[INFO] {}, {}".format(ft_sum, fi_sum))

    with open(fsave, "w+", encoding="utf-8") as f:
        for mid, typ in name_ftype_map.items():
            s_list = [mid]
            for t in typ:
                s_list.append(t)
            f.write("\t".join(s_list) + "\n")

if __name__ == "__main__":
    type_map = get_type_map("../data/type/types.map")
    get_ftype_map("../data/freebase/freebase-types", "../data/freebase/name_type.map")


