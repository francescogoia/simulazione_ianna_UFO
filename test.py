from model.model import Model

myModel = Model()
myModel._crea_grafo("circle", "AZ")
print(myModel.get_dettagli_grafo())
pesi = myModel.get_pesi()
"""for p in pesi:
    print(p)"""
path, n_citta, peso_tot = myModel._handle_percorso(5)
print("Lunghezza: ", n_citta)
print("Peso tot: ", peso_tot)
for p in path:
    print(p)
