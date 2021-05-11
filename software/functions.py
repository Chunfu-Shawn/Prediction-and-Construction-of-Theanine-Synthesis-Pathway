import datetime
import json
import pprint
import time
from itertools import islice
import matplotlib.pyplot as plt
import networkx as nx


def k_shortest_paths(G, source, target, k, weight=None):
    return list(
        islice(nx.shortest_simple_paths(G, source, target, weight=weight), k)
    )


class PathwaySearch:
    """
    Using graph algorithms to search pathway.
    """

    def __init__(self, init_json):
        """init_json should be formatted in a special style. An example is provided. e_coli_core.json"""
        assert (type(init_json) == str)
        self.net_dict = json.loads(init_json)
        self.reac_num_dict = {self.net_dict['reactions'][i]['id']: self.net_dict['reactions'][i]['metabolites'] for i in
                              range(len(self.net_dict['reactions']))}
        self.metabolites = [self.net_dict['metabolites'][i]['id'] for i in range(len(self.net_dict['metabolites']))]
        self.metabolite_count = len(self.metabolites)
        self.reaction_count = len(self.reac_num_dict.items())
        self.id2name_dict = {}
        metalist = [i['id'] for i in self.net_dict['metabolites']]
        for meta in self.net_dict['metabolites']:
            self.id2name_dict[meta['id']] = meta['name']
        for reac in self.net_dict['reactions']:
            self.id2name_dict[reac['id']] = reac['id']
        self.G = nx.DiGraph()
        for meta in self.net_dict['metabolites']:
            self.G.add_node(meta['id'])
        key_ex = ["C00001", "C00002", "C00003", "C00004", "C00005",
                  "C00006", "C00007", "C00008", "C00009", "C00011", "C00080",
                  "C00030", "C00020", "C00021", "C00014", "C00027", "C00013",
                  "C00042", "C03024", "C03161", "C00399", "C00390", "C00472",
                  "C15602", "C00024"]
        for reac in self.net_dict['reactions']:
            self.G.add_node(reac['id'])
            for k, v in reac['metabolites'].items():
                if k in key_ex:
                    continue
                else:
                    if v < 0:
                        try:
                            self.G.add_edge(reac['id'], k, weight=float(reac['energy']['mean']) / 2 + 1336)
                            self.G.add_edge(k, reac['id'], weight=float(reac['energy']['mean']) / 2 + 1336)

                        except:
                            pass
                    else:
                        try:
                            self.G.add_edge(k, reac['id'], weight=float(reac['energy']['mean']) / 2 + 1336)
                            self.G.add_edge(reac['id'], k, weight=float(reac['energy']['mean']) / 2 + 1336)

                        except:
                            pass

    def SimpleSaerch(self, start, end, pathway_nums=10):
        """
        Given start compound and end compound to search pathways.
        start and end must be cid string
        pathway_nums must be an int and >0 (default is 5)
        """
        assert (type(start) == str)
        assert (type(end) == str)
        assert (type(pathway_nums) == int and 0 < pathway_nums < 2000)
        ret = []
        for path in k_shortest_paths(self.G, start, end, pathway_nums):
            res = [self.id2name_dict[i] for i in path]
            if 'water' in res:
                continue
            length = sum([self.G.edges[path[i], path[i + 1]]['weight'] for i in range(len(path) - 1)])
            ret.append((res, length))

        return ret
        # return json.dumps(ret)

    def ReverseSaerch(self, target, nums=5):
        """
        Given target compound to reverse search the starting ones.
        tartget must be cid string
        num must be integer and >0
        """
        ret = []
        for k, v in nx.single_target_shortest_path(self.G, target, cutoff=nums).items():
            if 'C' in k:
                pth = [self.id2name_dict[i] for i in v]
                ret.append((self.id2name_dict[k], pth))
        if len(ret) >= 20:
            l = 20
        else:
            l = len(ret)
        return ret[0:l]
        # return json.dumps(ret)

    def stat(self):
        print(len(self.G.nodes))
        print(len(self.G.edges))
        degree = nx.degree_histogram(self.G)  # 返回图中所有节点的度分布序列
        x = range(len(degree))  # 生成x轴序列，从1到最大度
        y = [z / float(sum(degree)) for z in degree]
        # 将频次转换为频率
        plt.loglog(x, y, color="blue", linewidth=5)  # 在双对数坐标轴上绘制度分布曲线
        plt.xlabel("degree of nodes")
        plt.ylabel("frequency of degrees")
        plt.show()

    def Draw(self):
        colors = range(20)
        plt.title('metabolisom network of tea')
        nx.draw(self.G, pos=nx.random_layout(self.G), node_size=40, with_labels=True,
                width=1, font_size=6, edge_color="black", node_color="blue")
        plt.savefig("path.png")
        return plt.show()


if __name__ == '__main__':
    '''
    '''
    json_txt = ''
    with open("./complex_data.json", 'r') as load_f:
        json_txt = load_f.read()
    metabolic_info = json.loads(json_txt)
    print(str(time.time()).replace('.', ''))
    print(str(datetime.date.today()).replace('-', '_'))
    # 通路搜索测试
    Sear = PathwaySearch(json_txt)
    # 茶氨酸：C01047 L-谷氨酸：C00025 乙胺：C00797 葡萄糖：C00031
    # 铵盐NH4+：C01342 α-酮戊二酸：C00026 丙氨酸：C00041 丙酮酸：C00022
    # 柠檬酸：C00158 乙酰辅酶A：C00024

    # 咖啡因：C07481 黄嘌呤核苷xanthosine：C01762 可可碱theobromine：C07480 7-甲基黄嘌呤：C16353
    # 茶叶碱：C07130 黄嘌呤：C00385 IMP：C00130 鸟嘌呤：C00242 次黄嘌呤：C00262

    # EGCG:C09731 (-)-表儿茶素:C09727 (+)-儿茶酸:C06562 无色花青素:C05906 圣草酚：C05631
    # 柚皮素naringenin:C00509 花旗松素taxifolin:C01617 茶尔酮chalcone：C01484
    pprint.pprint(Sear.ReverseSaerch("C16765"), sort_dicts=True)
