import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()

    def buildGraph(self, id_category, data1, data2):

        nodi = self.getNodes(id_category)
        self._graph.add_nodes_from(nodi)

        self._dizionario = {}
        for n in nodi:
            self._dizionario[n.product_id] = n

        archi = self.getArchi(id_category, data1, data2)

        for arco in archi:
            self._graph.add_edge(arco.u, arco.v, weight=arco.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges(data=True))

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        return DAO.getAllCategories()

    def getNodes(self, id_category):
        return DAO.getAllNodes(id_category)

    def getArchi(self, id_category, data1, data2):
        return DAO.getAllArchi(id_category, data1, data2, self._dizionario)

    def getArchiCompleto(self):
        return self._graph.edges(data=True)

    def bestProduct(self):
        nodi = self._graph.nodes()
        lista_differenza = []
        for n in nodi:
            somma_entranti = 0
            somma_uscenti = 0
            differenza = 0

            # METODO CON ARCHI USCENTI ED ENTRANTI
            # uscenti = list(self._graph.out_edges(n, data = "weight"))
            # entranti = list(self._graph.in_edges(n, data = "weight"))
            #
            # for u,v,peso in uscenti:
            #     somma_uscenti += self._graph[u][v]["weight"]
            # for v,u,peso in entranti:
            #     somma_entranti += self._graph[v][u]["weight"]

            # METODO CON SUCCESSORI(nodi uscenti) E PREDECESSORI(nodi entranti)
            uscenti = list(self._graph.successors(n))
            entranti = list(self._graph.predecessors(n))

            for u in uscenti:
                somma_uscenti += self._graph[n][u]["weight"]

            for e in entranti:
                somma_entranti += self._graph[e][n]["weight"]

            differenza = somma_uscenti - somma_entranti
            lista_differenza.append((n,differenza))

        lista_differenza.sort(key=lambda x: x[1], reverse = True)
        best_5 = lista_differenza[:5]
        return best_5

    def getNodiCompleti(self):
        return list(self._graph.nodes())

    def getPath(self, start, end, lun):

        self._bestpath = []
        self._bestscore = 0

        parziale = []
        parziale.append(start)
        vicini = list(self._graph.edges(start, data=True))
        vicini.sort(key=lambda x: x[2]["weight"], reverse=True)

        for u,v,peso in vicini:
            parziale.append(v)
            self._ricorsione(parziale,end,lun)
            parziale.pop()

        return self._bestpath, self._bestscore

    def _ricorsione(self, parziale,end,lun):

        #1 condizione di ottimalità
        if len(parziale) == lun:
            if parziale[-1] == end and self._getScore(parziale) > self._bestscore:
                self._bestpath = copy.deepcopy(parziale)
                self._bestscore = self._getScore(parziale)

            return

        #2 condizione di terminazione

        #3 condizioni della ricorsione : si rispettino i versi, un nodo non può essere attraversato più volte, la somma degli archi deve essere massima
        vicini = list(self._graph.edges(parziale[-1], data = True))
        vicini.sort(key = lambda x: x[2]["weight"], reverse = True)

        for u,v,peso in vicini:
            if v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale,end,lun)
                parziale.pop()

    def _getScore(self, parziale):

        score = 0
        for i in range(0, len(parziale)-1):
            score += self._graph[parziale[i]][parziale[i+1]]["weight"]

        return score

    # def getBestPath(self, lun, start, end):
    #     self._bestPath = []
    #     self._bestScore = 0
    #     parziale = [start]
    #     self._ricorsione(parziale, lun, end)
    #     return self._bestPath, self._bestScore
    #
    # def _ricorsione(self, parziale, lun, end):
    #     if len(parziale) == lun:
    #         if parziale[-1] == end and self._getScore(parziale) > self._bestScore:
    #             self._bestScore = self._getScore(parziale)
    #             self._bestPath = copy.deepcopy(parziale)
    #         return
    #
    #     for n in self._graph.successors(parziale[-1]):
    #         if n not in parziale:
    #             parziale.append(n)
    #             self._ricorsione(parziale, lun, end)
    #             parziale.pop()
    #
    # def _getScore(self, parziale):
    #     score = 0
    #     for i in range(0, len(parziale) - 1):
    #         score += self._graph[parziale[i]][parziale[i + 1]]["weight"]
    #     return score
