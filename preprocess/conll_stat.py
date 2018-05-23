import os
import codecs
from collections import defaultdict, Counter
from copy import deepcopy

def conll_stat(dpath, cal_dict):
	for data in ["conll2003_train", "conll2003_ta", "conll2003_tb"]:
		tot = 0
		exist = 0
		for doc in os.listdir(os.path.join(dpath, data, "answer_mid")):
			with open(os.path.join(dpath, data, "answer_mid", doc), "r", encoding = "utf-8") as f:
				for line in f:
					entity = line.strip().split("\t")[-2]
					if entity in ["NIL", "--NME--"]:continue
					if entity in cal_dict.keys():
						exist += 1
					# else:
					# 	if redirect_map.get(entity, entity) in name_type_map.keys():
					# 		exist += 1
					tot += 1
		print("[INFO]", data, "\t", tot, "\t", exist)

def get_razor(fname):
	with codecs.open(fname, "r", encoding = "utf-8", errors = 'ignore') as f:
		name_type_map = defaultdict(set)
		for line in f:
			tokens = line.strip().split("\t")
			name_type_map[tokens[0]] = tokens[1:]
	print("[INFO] number of entities:{}".format(len(name_type_map.keys())))
	
	return name_type_map

def get_redirect_map(fname):
	with codecs.open(fname, "r", encoding="utf-8") as f:
		redirect_map = defaultdict(str)

		for line in f:
			tokens = line.strip().split("\t")
			if len(tokens) != 2:continue
			org, red = tokens
			redirect_map[org] = red
	print("[INFO] redirect map key len:{}".format(len(redirect_map.keys())))

	return redirect_map

def redirect_razor(fname, fsave):
	name_type_map = get_razor(fname)
	redirect_map = get_redirect_map("../../wiki_data/redirect_mapping_14.tsv")
	redirect_num = 0
	# repeated = 0
	new_map = defaultdict(list)
	for k, v in name_type_map.items():
		new_map[k] = v
		if k in redirect_map.keys():
			redirect_num += 1
			red = redirect_map[k]
			new_map[red] = list(set(new_map[red] + v))

	with codecs.open(fsave, "w+", encoding = "utf-8") as f:
		for k, v in new_map.items():
			s = [k] + [vv for vv in v]
			f.write("\t".join(s) + "\n")
	
	print("[INFO] number of entities:{}. org number of entities :{}. redirect number:{}.".format(len(new_map.keys()), len(name_type_map.keys()), redirect_num))

def get_figer_type(fname):
	with open(fname, "r", encoding="utf-8") as f:
		figer_map = {}
		for line in f:
			tokens = line.strip().split("\t")
			figer_map[tokens[0]] = tokens[1]

	print("[INFO] number of map entities:{}".format(len(figer_map.keys())))
	return figer_map

def cal_big5(cal_dict):
	big5 = 0
	type_counter = Counter()
	for typ in cal_dict.values():
		for tt in typ:
			type_counter[tt] += 1
	for k, v in type_counter.items():
		if v >= 5:
			big5 += 1
	print("[INFO] {} types contains more than 5 entities".format(big5))

def combine_razor_figer(fsave):
	exist_figer_map = defaultdict(set)
	for entity, typ in name_type_map.items():
		for tt in typ:
			if tt in figer_map.keys():
				exist_figer_map[entity].add(figer_map[tt])
	print("[INFO] {} entities has type in figer map".format(len(exist_figer_map.keys())))

	with codecs.open(fsave, "w+", encoding="utf-8") as f:
		for entity, typ in exist_figer_map.items():
			s = [entity] + [tt for tt in typ]
			f.write("\t".join(s) + "\n")

	return exist_figer_map

def process_query(text, mention, st, ed, win_size, typ, info):
	print(info)
	assert text[st:ed + 1] == mention
	text = text[:st] + "{{ " + text[st:ed + 1] + " }}" + text[ed + 1:]
	tokens = text.split()
	st_ctx = tokens.index("{{")
	ed_ctx = tokens.index("}}")
	ctx = tokens[max(0, st_ctx - win_size):min(len(tokens), ed_ctx + win_size)]
	# print("[INFO] " + str(ctx))
	st_ctx = ctx.index("{{")
	ed_ctx  = ctx.index("}}") - 1
	# print("[INFO] " + str(type(ctx)))
	ctx.remove("{{")
	ctx.remove("}}")

	assert " ".join(ctx[st_ctx:ed_ctx]) == mention
	ctx = " ".join(ctx)

	str_ans = str(st_ctx) + "\t" + str(ed_ctx) + "\t" + ctx + "\t" + typ + "\n"
	return str_ans 

def add_type_to_conll(dpath, cal_dict):
	for data in ["conll2003_train", "conll2003_ta", "conll2003_tb"]:
		tot = 0
		exist = 0
		ftrain = open(os.path.join(dpath, data, "train" +  data + ".tsv"), "w+", encoding = "utf-8")
		
		if not os.path.exists(os.path.join(dpath, data, "answer_type")):
			os.mkdir(os.path.join(dpath, data, "answer_type"))
		for doc in os.listdir(os.path.join(dpath, data, "answer_mid")):
			fin = open(os.path.join(dpath, data, "answer_mid", doc), "r", encoding = "utf-8")
			fquery = open(os.path.join(dpath, data, "query", doc), "r", encoding = "utf-8") 
			fan = open(os.path.join(dpath, data, "answer_type", doc), "w+", encoding = "utf-8")
			text = fquery.read()
			for line in fin:
				tokens = line.strip().split("\t")[:-1]
				tokens.append(" ".join(cal_dict.get(tokens[-1], "")) or "NIL")
				fan.write("\t".join(tokens) + "\n")
				ftrain.write(process_query(text, tokens[0], int(tokens[1]), int(tokens[2]), 10, tokens[-1], data+ "_" + doc)) #tokens -1 are entity types joined by space

			fin.close()
			fquery.close()
			fan.close()
		ftrain.close()

if __name__ == "__main__":
	# redirect_map = get_redirect_map("../../wiki_data/redirect_mapping_14.tsv")
	# name_type_map = get_razor("../data/type/textrazor-freebase-types-en.tsv")
	name_type_map = get_razor("../data/type/razor_figer.tsv")
	add_type_to_conll("../data/conll/", name_type_map)
	# figer_map = get_figer_type("../data/type/types.map")
	# exist_figer_map = combine_razor_figer("../data/type/razor_figer.tsv")
	# cal_big5(name_type_map)
	# cal_big5(exist_figer_map)
	# conll_stat("../data/conll/", name_type_map)
	# redirect_razor("../data/type/combined_razor.tsv", "../data/type/razor_redirect_14.tsv")