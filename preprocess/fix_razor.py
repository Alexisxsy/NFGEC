from collections import defaultdict, Counter
import codecs
import re

def combine_razor(fname, fsave):
	with codecs.open(fname, "r", encoding = "utf-8", errors = 'ignore') as f:
		name_type_map = defaultdict(set)
		for line in f:
			tokens = line.strip().split("\t")
			if len(tokens) != 3:continue
			name_type_map[tokens[0]].add(tokens[1])

	with codecs.open(fsave, "w+", encoding = "utf-8") as f:
		for entity in sorted(name_type_map):
			typ = name_type_map[entity]
			s = [entity]
			for t in typ:
				s.append(t)
			f.write("\t".join(s) + "\n")

	print("[INFO] number of entities:{}".format(len(name_type_map.keys())))
	return name_type_map

# def get_razor(fname):
# 	with codecs.open(fname, "r", encoding = "utf-8", errors = 'ignore') as f:
# 		name_type_map = defaultdict(set)
# 		need_mode = defaultdict(set)
# 		for line in f:
# 			tokens = line.strip().split("\t")
# 			if tokens[0][0] in list("ZXCVBNMASDFGHJKLQWERTYUIOP"):
# 				name_type_map[tokens[0]] = tokens[1:]
# 			else:
# 				need_mode[tokens[0]] = tokens[1:]
# 	print("[INFO] number of entities that is correct:{}".format(len(name_type_map.keys())))
# 	print("[INFO] number of entities that needs modification:{}".format(len(need_mode.keys())))
# 	return name_type_map, need_mode

def get_razor(fname):
	with codecs.open(fname, "r", encoding = "utf-8", errors = 'ignore') as f:
		name_type_map = defaultdict(set)
		for line in f:
			tokens = line.strip().split("\t")
			name_type_map[tokens[0]] = tokens[1:]
	print("[INFO] number of entities:{}".format(len(name_type_map.keys())))
	
	return name_type_map

def get_all_entity_name(fname):
	all_entity = Counter()
	with codecs.open(fname, "r", encoding = "utf-8") as f:
		for line in f:
			tokens = line.strip().split("\t")
			if len(tokens) != 2:continue
			# all_entity.append(tokens[0])
			all_entity[tokens[0]] += 1
	print("[INFO] " + str(len(all_entity.keys())) + " entities")

	return all_entity


def fix_character(fsave):
	processed = 0
	change_num = 0
	new_map = {}
	more_than_one = 0
	for entity in need_mode.keys():
		flag = 0
		for s in "zxcvbnmasdfghjklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP1234567890":
			if all_entity[s + entity] != 0:
				# print(entity +  "\t" +  s + entity)
				new_map[s+entity] = need_mode[entity]
				flag += 1
				#change_num += 1
		if flag == 0:
			new_map[entity] = need_mode[entity]
		elif flag > 1:
			more_than_one += 1

		processed += 1
		# if processed % 10000 == 0:
		# 	print("[INFO] processed {} entities".format(processed))

	# print("[INFO] number of new entity map:{}".format(len(new_map.keys())))
	# print("[INFO] number of org entity map:{}".format(len(need_mode.keys())))
	#print("[INFO] number of modified entity:{}".format(change_num))
	print("[INFO] modify more than once:{}".format(more_than_one))

	repeated_num = 0
	for k, v in name_type_map.items():
		if k in new_map.keys():
			# print("[INFO] repeated! " + k)
			repeated_num += 1
			new_map[k] += v
		else:
			new_map[k] = v
	
	print("[INFO] number of entities:{}".format(len(new_map.keys())))
	print("[INFO] number of repeated:{}".format(repeated_num))
	with codecs.open(fsave, "w+", encoding="utf-8") as f:
		for entity, typ in new_map.items():
			s = [entity] + [t for t in typ]
			f.write("\t".join(s) + "\n")

	print("")

if __name__ == "__main__":
	# name_type_map, need_mode = combine_razor("../data/type/textrazor-freebase-types-en.tsv", "../data/type/razor_new.tsv")
	# name_type_map = get_razor("../data/type/razor_new.tsv")
	# all_entity = get_all_entity_name("../data/freebase/title_id_map.tsv")
	# fix_character("../data/type/fixed_razor.tsv")
	combine_razor("../data/type/textrazor-freebase-types-en.tsv", "../data/type/combined_razor.tsv")


