import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.g = nx.Graph()
        self.mappaN = {}

    def getY(self):
        return DAO.getY()

    def getS(self, y):
        return DAO.get_all_states(y)

    def creaG(self, y, s):
        self.g.clear()
        self.n = DAO.getN(y, s)
        self.g.add_nodes_from(self.n)
        for n in self.n:
            self.mappaN[n.id] = n
        self.archi = DAO.getA(y, s)
        for a in self.archi:
            if self.mappaN[a[0]].distance_HV(self.mappaN[a[1]]) < 100:
                self.g.add_edge(self.mappaN[a[0]], self.mappaN[a[1]])

    def len(self):
        return len(self.g.nodes()), len(self.g.edges())

    def stampa(self):
        comp = list(nx.connected_components(self.g))
        mas = max(comp, key=len)
        return len(comp), mas


    def cerca(self):
        self.best = []
        self.punti = 0
        for n in self.g.nodes():
            parziale = [n]
            self.ric(parziale)
        return self.best, self.punti

    def ric(self, parziale):
        if self.costo(parziale) > self.punti:
            self.best = copy.deepcopy(parziale)
            self.punti = self.costo(parziale)

        for n in self.g.neighbors(parziale[-1]):
            if self.is_valid(n, parziale):
                parziale.append(n)
                self.ric(parziale)
                parziale.pop()

    def is_valid(self, n, parziale):
        if parziale[-1].duration < n.duration:
            somma = sum(1 for n in parziale if n.datetime.month == n.datetime.month)
            if somma <3:
                return True
        return False

    def costo(self, parziale):
        costo = 100
        for i in range(1, len(parziale)):
            if parziale[i-1].datetime.month == parziale[i].datetime.month:
                costo+=200
            costo+=100
        return costo