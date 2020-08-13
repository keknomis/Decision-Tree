import math
import pygraphviz as pgv
import os
import pickle


class Tree:
    # magic func.
    # konstruktor, za vsak objekt
    # tree je dictionary dictionarijev, hrani node
    # endpoits je seznam, ki hrani indekse listov drevesa
    # size, je index za naslednje, se ne narejen list : lastindex
    # draw_tree_in_progress, klic metode za izris po indeksima

    def __init__(self):
        self.tree = {}
        self.endpoints = []
        self.size = 0
        self.draw_tree_in_progress()

    """
        Funkcija, params:
            * self, dodamo zato da lahko klicemo
            * parent: Index noda, oce
            * external_label, ime noda
            * probability (float), nosi vrednost za odločitve z verjetnostjo, procent
            * weight je utez
            * parent, external_label, weight, probability so opcijski parametri, default vrednost je none ali 0
    """

    def create_node(self, parent=None, external_label="", weight=0, probability=None):
        # nodu damo index
        index = self.size
        # inkrement indexa
        self.size += 1
        # napolnimo dictionary z novim nodem in mu dodamo vrednosti
        # internal label
        # type- po defaultu, se vsak node naredi na zacetku kot koncni in nima sinov
        # visited, se uporablja za traversanje, da ne gremo cez isti node 2x
        # best child- je lahko max/min za odločitev (zelena črta)
        self.tree[index] = {
                        'parent': parent, 'internal_label': 0, 'external_label': external_label, 'weight': weight,
                        'type': 'end', 'children': [], 'visited': False, 'best_child': None, 'probability': probability
                        }
        # dodamo node v seznam endpointov
        self.endpoints.append(index)

        # if stavek, ki se pozene vsakic, ko zgradimo novo vejo, gremo za stopnjo globlje
        # kak ve da je to parent? v funkcijo poslemo index parenta, if potem pogleda, ce imamo v seznamu to stevilko
        # ce je not jo odstranimo

        if parent in self.endpoints:
            self.endpoints.remove(parent)
        # preverjamo ali je node koren, ce ni root
        if parent is not None:
            # potem ga razdelimo glede na tip
            # ce ima node definirano verjetnost, torej ce je input field poln
            # potem damo ocetu flag probabilitistic
            if probability is not None:
                self.tree[parent]['type'] = 'probabilistic'
            else:
                # v primeru, ko ni verjetnosti
                self.tree[parent]['type'] = 'decision'
                # ko dodamo novi node, moramo v ocetu updejtat seznam otrok.
            self.tree[parent]['children'].append(index)
        # klicemo funkcjio za risanje
        self.draw_tree_in_progress()

    def remove_node(self, node):
        # zacasne spremenljivke
        parent = self.tree[node]['parent']
        children = self.tree[node]['children']
        probability = self.tree[node]['probability']

        # edge case, node je sam sebi sin
        if node in children:
            # ce je ga zbrisemo
            children.remove(node)
        # Children je iterator, kopija tistega kar brisemo
        Children = children.copy()
        # Rekurzivni klic, ki umakne vse otroke vozlišča, ki ga odstranimo
        for child in Children:
            self.remove_node(child)
        # preverimo, da nismo v rootu
        if parent is not None:
            # preverimo, če ni bil odstranjen že prej
            if node in self.tree[parent]['children']:
                # iz liste otrok, starševskega vozlišča umaknemo otroka
                self.tree[parent]['children'].remove(node)
            # če starš nima več otrok, se spremeni ta node v otroka
            if self.tree[parent]['children'] == []:
                # tip mu spremenimo v end
                self.tree[parent]['type'] = 'end'
                #brisanje noda
        del self.tree[node]

    	#risanje posodobljene slike 
        self.draw_tree_in_progress()

    #HELPER FUNCTION
    # funkcija, ki preverja, če so bila obiskana vsa vozlišča 
    # nekega starša
    # kličemo jo iz calculate 
    def children_visited(self, node):
        for child in self.tree[node]['children']:
            if self.tree[child]['visited'] is False:
                return False
        return True

    # 
    # Funkcija, ki poišče vozlišča brez otrok.
    def find_endpoints(self):
        #prazen seznam
        endpoints = []
        for node in self.tree:
            if self.tree[node]['children'] == []:
                endpoints.append(node)
        return endpoints

    def calculate_all(self, type='max'):
        #ponastavimo števce
        for node in self.tree:
            self.tree[node]['internal_label'] = 0
            self.tree[node]['visited'] = False
        self.endpoints = self.find_endpoints()
        
        while self.endpoints:
            endpoint = self.endpoints.pop(0)
            if self.tree[endpoint]['visited']:
                continue
            # Preverimo, če so obiskani vsi listi nekega vozlišča
            if self.children_visited(endpoint):
                if type == 'max':
                    self.calculate_node_max(endpoint)
                else:
                    self.calculate_node_min(endpoint)
                self.tree[endpoint]['visited'] = True
                #preverimo, če smo prišli čisto levo, torej v root
                if endpoint == 0:
                    break
                Parent = self.tree[endpoint]['parent']
                if not (Parent in self.endpoints):
                    self.endpoints.append(Parent)
            # V primeru, da otroci niso obiskani, damo to vozlišče na konec seznama vozlišč
            else:
                self.endpoints.append(endpoint)
        self.draw_tree()


    def calculate_node_min(self, node):
        #default val 
        best_child = None
        if self.tree[node]['type'] == 'decision':
            #default val
            minimum = math.inf
            for child in self.tree[node]['children']:
                
                if minimum > self.tree[child]['internal_label']:
                    minimum = self.tree[child]['internal_label']
                    best_child = child
            self.tree[node]['best_child'] = best_child
            self.tree[node]['internal_label'] = minimum + self.tree[node]['weight']
        
        #Če je tip vozlišča probalistic, torej ima nek %
        elif self.tree[node]['type'] == 'probabilistic':
            temp = 0
            #za vsakega otroka dodamo v temp zmožek verjetnostni in teže otroka
            
            for child in self.tree[node]['children']:
                probability = self.tree[child]['probability']
                temp += self.tree[child]['internal_label']*probability
                #vozlišču, na katerem poračunamo vredosti prištejemo temp
                #in še njegovo vrednost, težo
            self.tree[node]['internal_label'] = temp + self.tree[node]['weight']
        #če je vozlišče tipa end, potem internal_label 
        #Ko smo na vozlišču tipa end, se teža vozlišča spremeni v internal_label
        #Spremenimo vozlišče v obiskano
        elif self.tree[node]['type'] == 'end':
            self.tree[node]['internal_label'] = self.tree[node]['weight']
            #mogoce umakni, dvakrat isto delas
            self.tree[node]['visited'] = True

    def calculate_node_max(self, node):
        best_child = None
        if self.tree[node]['type'] == 'decision':
            maximum = -math.inf
            for child in self.tree[node]['children']:
                if self.tree[child]['internal_label'] > maximum:
                    maximum = self.tree[child]['internal_label']
                    best_child = child
            self.tree[node]['internal_label'] = maximum + self.tree[node]['weight']
            self.tree[node]['best_child'] = best_child
        elif self.tree[node]['type'] == 'probabilistic':
            temp = 0
            for child in self.tree[node]['children']:
                probability = self.tree[child]['probability']
                temp += self.tree[child]['internal_label']*probability
            self.tree[node]['internal_label'] = temp + self.tree[node]['weight']
        elif self.tree[node]['type'] == 'end':
            self.tree[node]['internal_label'] = self.tree[node]['weight']
            self.tree[node]['visited'] = True

    def save_to_file(self, path):
        #with je vbistvu file.close
        with open(path, mode='wb') as file:
            pickle.dump(self.tree, file)

#pickle paket, za shranjevanje in branje py slovarjem
    def load_from_file(self, path):
        with open(path, mode = 'rb') as file:
            self.tree = pickle.load(file)
        self.size = max([key for key in self.tree])
        self.endpoints = self.find_endpoints()
        self.draw_tree_in_progress()

    #vrne slovar
    def get_tree(self):
        return self.tree

    
    def drawNode(self, node, Graph, finished = True):
        node_type = self.tree[node]['type']
        if node_type == "decision":
            Graph.node_attr['width'] = '1'
            Graph.node_attr['height'] = '1'
            Graph.node_attr['shape'] = 'polygon'
            Graph.node_attr['sides'] = '4'
        elif node_type == "probabilistic":
            Graph.node_attr['width'] = '1'
            Graph.node_attr['height'] = '1'
            Graph.node_attr['shape'] = 'circle'
        else:
            Graph.node_attr['width'] = '1'
            Graph.node_attr['height'] = '2'
            Graph.node_attr['shape'] = 'triangle'
            Graph.node_attr['orientation'] = '90'
        if finished:
            label = f"label = {self.tree[node]['external_label']}\n internal label = {self.tree[node]['internal_label']:.2f}"
        else:
            label = f"label = {self.tree[node]['external_label']}\n index = {node}"

        Graph.add_node(str(node), label=label)

    def get_best_path(self):
        best = [0]
        child = self.tree[0]['best_child']
        while child is not None:
            best.append(child)
            child = self.tree[child]['best_child']
        return best

    def draw_tree_in_progress(self):
        self.G = pgv.AGraph(rankdir="LR", size='20.0,20.0')
        self.G.node_attr['width'] = '1'
        self.G.node_attr['height'] = '1'
        self.G.node_attr['shape'] = 'polygon'
        self.G.node_attr['sides'] = '4'

        for child in self.tree:
            self.drawNode(child, self.G, finished=False)

        for i in self.tree:
            for child in self.tree[i]['children']:
                if self.tree[i]['type'] == 'probabilistic':
                    prob = self.tree[child]['probability']
                    label = f"probability = {prob:.3f}"
                    self.G.add_edge(str(i), str(child), label=label)
                else:
                    label = f'{self.tree[child]["weight"]:.2f}'
                    self.G.add_edge(str(i), str(child), label=label, color='black')

        self.G.layout('dot')
        self.G.draw(os.getcwd() + os.path.sep + 'graf_in_progress.png')

    def draw_tree(self):
        self.G = pgv.AGraph(rankdir="LR", size='20.0,20.0')
        self.G.node_attr['width'] = '1'
        self.G.node_attr['height'] = '1'
        self.G.node_attr['shape'] = 'polygon'
        self.G.node_attr['sides'] = '4'

        best_path = self.get_best_path()

        for child in self.tree:
            self.drawNode(child, self.G, finished=True)

        for i in self.tree:
            for child in self.tree[i]['children']:
                if self.tree[i]['type'] == 'probabilistic':
                    prob = self.tree[child]['probability']
                    label = f"probability = {prob:.3f}"
                    self.G.add_edge(str(i), str(child), label=label)
                else:
                    label = f'{self.tree[child]["weight"]:.2f}'
                    if child in best_path:
                        self.G.add_edge(str(i), str(child), label=label, color='green')
                    else:
                        self.G.add_edge(str(i), str(child), label=label, color='black')

        self.G.layout('dot')
        self.G.draw(os.getcwd() + os.path.sep + 'graf1.png')


if __name__ == '__main__':
    tree = Tree()
    tree.create_node()
    tree.create_node(parent = 0, weight = 100)
    tree.load_from_file('D:\\mytree.pkl')
    print(tree.get_tree())
