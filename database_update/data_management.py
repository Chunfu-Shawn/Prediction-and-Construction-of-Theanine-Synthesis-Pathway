import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def deletejson(file_json_path):
    with open(file_json_path, 'r', encoding='utf-8') as load_f:
        metabolic_info = json.load(load_f)
    l = len(metabolic_info["reactions"])
    print(l)
    n = 0
    while n < l:
        rid = metabolic_info["reactions"][n]["id"]
        print(metabolic_info["reactions"][n])
        flag = False
        with open("RN3.txt") as f:
            for line in f.readlines():
                if rid in str(line):
                    flag = True
        if not flag:
            del metabolic_info["reactions"][n]
            n = n - 1
            l = l - 1
        else:
            n = n + 1
    with open(file_json_path, 'w+', encoding='utf-8') as load_f:
        load_f.write(json.dumps(metabolic_info, indent=4, separators=(',', ': ')))


def addjson(file_json_path):
    with open(file_json_path, 'r', encoding='utf-8') as load_f:
        metabolic_info = json.load(load_f)
    l = len(metabolic_info["reactions"])
    print(l)

    with open("RN3.txt") as f:
        f_list = [i for i in f]
        for m in range(len(f_list)):
            flag = False
            n = 0
            while n < l:
                rid = metabolic_info["reactions"][n]["id"]
                if str(rid) in str(f_list[m]):
                    flag = True
                n = n + 1
            if not flag:
                print(f_list[m])
                metabolic_info["reactions"].append({"id": f_list[m].replace("\n", ""),
                                                    "energy": {"mean": energy_median, "sd": energy_sd_median},
                                                    "lower_bound": 0.0,
                                                    "upper_bound": 999999.0,
                                                    "metabolites": {}
                                                    })

    with open(file_json_path, 'w+', encoding='utf-8') as load_f:
        load_f.write(json.dumps(metabolic_info, indent=4, separators=(',', ': ')))


def energystat(file_json_path):
    with open(file_json_path, 'r', encoding='utf-8') as load_f:
        metabolic_info = json.load(load_f)
    l = len(metabolic_info["reactions"])
    n = 0
    energy_mean_list = []
    energy_sd_list = []
    while n < l:
        if metabolic_info["reactions"][n]['energy']['mean']:
            energy_mean_list.append(metabolic_info["reactions"][n]['energy']['mean'])
            energy_sd_list.append(metabolic_info["reactions"][n]['energy']['sd'])
        n = n + 1
    energy_mean_mean = np.mean(energy_mean_list)
    energy_mean_median = np.median(energy_mean_list)
    energy_sd_median = np.median(energy_sd_list)
    fig = plt.figure()
    plt.xlim(-500, 200)
    plt.ylim(0, 400)
    plt.xlabel("Energy for reaction")
    plt.ylabel("Number")
    ax = fig.add_subplot()
    ax.hist(energy_mean_list, bins=1000, color='blue', alpha=0.7)
    plt.savefig('./data_energy_diversity.jpg')
    return energy_mean_mean, energy_mean_median, energy_sd_median


def addEandE(file_json_path, file_csv_path):
    with open(file_json_path, 'r', encoding='utf-8') as load_f:
        metabolic_info = json.load(load_f)
    csv_e_e = pd.read_csv(file_csv_path, usecols=['%RID', 'ECnum', 'ReactionClass'])
    flag = False
    for n in range(len(metabolic_info["reactions"])):
        if metabolic_info["reactions"][n]['id'] == "R00018":
            flag = True
        if flag:
            for m in range(len(csv_e_e)):
                if metabolic_info["reactions"][n]['id'] == csv_e_e.iloc[m]["%RID"]:
                    metabolic_info["reactions"][n]["ecnum"] = [csv_e_e.iloc[m]["ECnum"]]
                    metabolic_info["reactions"][n]["reaction_class"] = [csv_e_e.iloc[m]["ReactionClass"]]
                    print(metabolic_info["reactions"][n]['id'])
    with open(file_json_path, 'w+', encoding='utf-8') as load_f:
        load_f.write(json.dumps(metabolic_info, indent=4, separators=(',', ': ')))


def addmetabolites(file_json_path, file_csv_path):
    with open(file_json_path, 'r', encoding='utf-8') as load_f:
        metabolic_info = json.load(load_f)
    flag = False
    f = False
    m = 0

    for n in range(5139, len(metabolic_info["reactions"])):
        cid0 = []
        meta = open(file_csv_path, encoding='utf-8')
        for line in meta:
            if ">" in str(line):
                rid = line.split(",")
                if metabolic_info["reactions"][n]['id'] in rid[0]:
                    f = True
            else:
                if "C" in str(line):
                    if f:
                        cid = line.replace("\n", "")
                        cid = cid.split(",")
                        cid0 = cid
                elif "G" in str(line):
                    f = False
                else:
                    if f:
                        cnum = line.replace("\n", "")
                        cnum = cnum.split(",")
                        for k in range(len(cnum)):
                            if '(n-1)' in cnum[k]:
                                cnum[k] = cnum[k].replace('(n-1)', '99')
                            if '(n-2)' in cnum[k]:
                                cnum[k] = cnum[k].replace('(n-2)', '98')
                            if 'n' in cnum[k]:
                                cnum[k] = cnum[k].replace('n', '100')
                        for i in range(len(cid0)):
                            metabolic_info["reactions"][n]["metabolites"][cid0[i].strip()] = int(cnum[i])
                        f = False
                        print(metabolic_info["reactions"][n]["metabolites"])
    meta.close()
    with open(file_json_path, 'w+', encoding='utf-8') as load_f:
        load_f.write(json.dumps(metabolic_info, indent=4, separators=(',', ': ')))


def delete_edge_water(file_json_path):
    with open(file_json_path, 'r', encoding='utf-8') as load_f:
        metabolic_info = json.load(load_f)
    keylist = ["C00001", "C00002", "C00008"]
    for i in range(len(metabolic_info["reactions"])):
        for k in metabolic_info["reactions"][i]["metabolites"]:
            if k == "C00001" or k == "C00002" or k == "C00008" or k == "C00009":
                print(metabolic_info["reactions"][i]["metabolites"][k])
                del metabolic_info["reactions"][i]["metabolites"][k]
    with open(file_json_path, 'w+', encoding='utf-8') as load_f:
        load_f.write(json.dumps(metabolic_info, indent=4, separators=(',', ': ')))


def addareac(file_json_path, id, metabolites, ecnum, reaction_class, e1=-59.4797, e2=8.0264):
    with open(file_json_path, 'r', encoding='utf-8') as load_f:
        metabolic_info = json.load(load_f)

    metabolic_info["reactions"].append({"id": id,
                                        "energy": {"mean": e1, "sd": e2},
                                        "lower_bound": 0.0,
                                        "upper_bound": 999999.0,
                                        "metabolites": metabolites,
                                        "ecnum": [ecnum],
                                        "reaction_class": [reaction_class],
                                        })
    with open(file_json_path, 'w+', encoding='utf-8') as load_f:
        load_f.write(json.dumps(metabolic_info, indent=4, separators=(',', ': ')))


def delcom(file_json_path):
    with open(file_json_path, 'r', encoding='utf-8') as load_f:
        metabolic_info = json.load(load_f)
    compounds = []
    for i in range(len(metabolic_info["reactions"])):
        for key in metabolic_info["reactions"][i]["metabolites"].keys():
            compounds.append(key)
            compounds = list(set(compounds))
    print(compounds)
    l = len(metabolic_info["metabolites"])
    n = 0
    while n < l:
        print(metabolic_info["reactions"][n])
        if metabolic_info["metabolites"][n]["id"] in compounds:
            n = n+1
        else:
            del metabolic_info["metabolites"][n]
            l = l - 1
            n = n - 1

    print(len(metabolic_info["metabolites"]))
    print(len(metabolic_info["reactions"]))
    with open(file_json_path, 'w+', encoding='utf-8') as load_f:
        load_f.write(json.dumps(metabolic_info, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    energy_mean = 0
    energy_median = 0
    energy_sd_median = 0
    # 统计原有数据库中反应的平均能量和方差，用作无数据时的默认值
    energy_mean, energy_median, energy_sd_median = energystat("./complex_data_tea.json")
    with open("./complex_data.json", 'r', encoding='utf-8') as load_f:
        metabolic_info = json.load(load_f)
    print(len(metabolic_info["metabolites"]))
    print(len(metabolic_info["reactions"]))

"""
    # 删除在RN3.txt不存在的反应
    deletejson("./complex_data_tea.json")
    # 删除不在茶树中的化合物
    delcom("./complex_data_tea.json")
    # 寻找在RN3.txt中不存在的反应，并添加进json
    addjson("./complex_data_tea.json")
    # 为新增反应添加反应的酶序号、反应类型
    addEandE("./complex_data_tea.json", "./reaction_chart.csv")
    # 为新增反应添加反应的详细信息
    addmetabolites("./complex_data_tea.json", "./Reaction2AnalysisSimple.csv")
    #delete_edge_water("./complex_data_tea_copy.json")
"""
