from model.model import Model

myModel = Model()
myModel.buildGraph(7, '2016-01-01', '2018-12-28')
nNodes, nEdges = myModel.getGraphDetails()
print(f"Num nodes: {nNodes}, num edges: {nEdges}")
best_5 = myModel.bestProduct()
for b in best_5:
    print(f"{b[0]} - {b[1]}")

nodi = myModel.getNodiCompleti()
percorso, score= myModel.getPath(nodi[0], nodi[5], 6)
print(score)
for p in percorso:
    print(p.product_name)