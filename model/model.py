import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMap = {}
        self._grafo = nx.Graph()
        self._states = DAO.getAllStates()
        self._shapes = DAO.getAllShapes()

    def _crea_grafo(self, forma, stato):
        self._nodes = DAO.getAllNodes(stato)
        self._grafo.add_nodes_from(self._nodes)
        archi = DAO.getAllEdges(stato, forma)
        for a in archi:
            self._grafo.add_edge(a[0], a[1], weight=a[2])

    def get_dettagli_grafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_pesi(self):
        result = []
        for c in self._nodes:
            vicini = self._grafo.neighbors(c)
            peso_vicini = 0
            for v in vicini:
                peso_vicini += self._grafo[c][v]["weight"]
            result.append((c, peso_vicini))
        return result

    def _handle_percorso(self, max_citta):
        self._bestPath = []
        self._n_citta_percorso = 0
        self._bestPeso = 0
        for n in self._nodes:
            self._ricorsione(n, [], max_citta)
        return self._bestPath, self._n_citta_percorso, self._bestPeso

    def _ricorsione(self, nodo, parziale, max_citta):
        n_citta_parziale, peso_parziale = self.get_info_parziale(parziale)
        if peso_parziale > self._bestPeso:
            self._bestPeso = peso_parziale
            self._n_citta_percorso = n_citta_parziale
            self._bestPath = copy.deepcopy(parziale)
        if n_citta_parziale == max_citta:
            return
        vicini = self._grafo.neighbors(nodo)
        vicini_ordinati = []
        for v in vicini:
            vicini_ordinati.append((nodo, v, self._grafo[nodo][v]["weight"]))
        vicini_ordinati.sort(key=lambda x: x[2], reverse=True)
        for v in vicini_ordinati:
            if self._filtroNodi(v[1], parziale):
                peso_arco = self._grafo[v[0]][v[1]]["weight"]
                if len(parziale) > 0:
                    if peso_arco < parziale[-1][2]:
                        parziale.append((v[0], v[1], peso_arco))
                        self._ricorsione(v[1], parziale, max_citta)
                        parziale.pop()
                else:
                    parziale.append((v[0], v[1], peso_arco))
                    self._ricorsione(v[1], parziale, max_citta)
                    parziale.pop()

    def get_info_parziale(self, parziale):
        s_citta = set()
        pTot = 0
        for a in parziale:
            s_citta.add(a[0])
            s_citta.add(a[1])
            pTot += a[2]
        return len(s_citta), pTot

    def _filtroNodi(self, v, parziale):
        for a in parziale:
            if a[0] == v or a[1] == v:
                return False
        return True
