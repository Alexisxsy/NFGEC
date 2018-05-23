#get types mapping for entities
import pickle
import codecs
from collections import defaultdict, Counter

def get_name_type_map(fname, fsave, ffiger):
	with codecs.open(fname, "r", encoding="utf-8", errors='ignore') as f:
		name_type_map = defaultdict(set)
		skip_num = 0
		type_set = set()
		processed = 0
		type_counter = Counter()
		for line in f:
			tokens = line.strip().split("\t")
			if len(tokens) != 3 or tokens[-1] != '0':
				skip_num += 1
				continue
			name_type_map[tokens[0]].add(tokens[1])
			type_set.add(tokens[1])
			type_counter[tokens[1]] += 1

			processed += 1
			if processed % 1000000 == 0:
				print("[INFO] processed {} lines".format(processed))

	print("[INFO] total number of entities:{}".format(len(name_type_map.keys())))
	print("[INFO] total number of unique types:{}".format(len(type_set)))
	print("[INFO] total number of skip:{}".format(skip_num))

	new_type_set = set([])
	figer_name_type_map = defaultdict(set)
	trigger_type_set =set([])
	le5_type = set([])
	for name, typ in name_type_map.items():
		for t in typ:
			if type_counter[t] < 5:
				le5_type.add(t)
				continue
			# new_type = type_map.get(t, t)
			# figer_name_type_map[name].add(new_type)
			# new_type_set.add(new_type)
			if t in type_map.keys():
				trigger_type_set.add(t)
				figer_name_type_map[name].add(type_map[t])
				# new_type_set.add(new_type)

	print("[INFO] total number of entities:{}".format(len(figer_name_type_map.keys())))
	print("[INFO] total number of new entity type:{}".format(len(new_type_set)))
	print("[INFO] triggered figger type map:{}".format(len(trigger_type_set)))
	print("[INFO] total number of entity type that contains less than 5 entities:{}".format(len(le5_type)))

	with open(fsave + ".pkl", "wb") as f:
		pickle.dump(name_type_map, f)

	with open(ffiger + ".pkl", "wb") as f:
		pickle.dump(figer_name_type_map, f)



	print("DONE!")

def get_mid_wiki_map(fname):
	with open(fname, "r", encoding="utf-8") as f:
		name_mid_map = {}
		mid_name_map = {}

		for line in f:
			tokens = line.strip().split("\t")
			if len(tokens) != 2:continue
			name_mid_map[tokens[0]] = tokens[1]
			mid_name_map[tokens[1]] = tokens[0]

		print("[INFO] number of entities:{}".format(len(name_mid_map.keys())))
	
	return name_mid_map, mid_name_map


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

if __name__ == "__main__":
	type_map = get_type_map("../data/type/types.map")
	get_name_type_map("../data/type/textrazor-freebase-types-en.tsv", "../data/type/name_type", "../data/type/name_figer")