import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._category = None
        self._start = None
        self._end = None
        self._lun = None

    def fillcategories(self):

        lista_categories = self._model.getCategories()
        for categories in lista_categories:
            self._view._ddcategory.options.append(
                ft.dropdown.Option(data=categories,
                                   key=categories,
                                   text=categories[1],
                                   on_click=self.read_categories)
            )

    def read_categories(self, e):
        if e.control.data is None:
            self._category = None
        else:
            self._category = e.control.data

    def handleCreaGrafo(self, e):

        if  self._view._dp1.value is None or self._view._dp2.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Inserisci tutti i campi"))

        self._model.buildGraph( self._category[0], self._view._dp1.value, self._view._dp2.value)
        n, m = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato! Il grafo è costituito di {n} nodi ed {m} archi"))

        lista_nodi = self._model.getNodiCompleti()
        for nodo in lista_nodi:
            self._view._ddProdStart.options.append(
                ft.dropdown.Option(data=nodo,
                                   key=nodo,
                                   text=nodo.product_name,
                                   on_click=self.read_start)
            )

        for nodo in lista_nodi:
            self._view._ddProdEnd.options.append(
                ft.dropdown.Option(data=nodo,
                                   key=nodo,
                                   text=nodo.product_name,
                                   on_click=self.read_end)
            )

        self._view.update_page()

    def read_start(self, e):
        if e.control.data is None:
            self._start = None
        else:
            self._start = e.control.data

    def read_end(self, e):
        if e.control.data is None:
            self._end = None
        else:
            self._end = e.control.data

    def handleBestProdotti(self, e):

        best_5 = self._model.bestProduct()
        self._view.txt_result.controls.clear()
        for n in best_5:
            self._view.txt_result.controls.append(
                ft.Text(f"{n[0]} - {n[1]}"))

        self._view.update_page()

    def handleCercaCammino(self, e):

       lun = int(self._view._txtInLun.value)
       if lun is None or self._start is None or self._end is None:
           self._view.txt_result.controls.clear()
           self._view.txt_result.controls.append(
               ft.Text(f"Inserisci tutti i campi"))

       if lun < 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Inserisci una lunghezza positiva"))

       best_percorso, score = self._model.getPath(self._start, self._end, lun)

       self._view.txt_result.controls.clear()
       self._view.txt_result.controls.append(
           ft.Text(f"Il percorso ottimale di peso : {score}"))
       for b in best_percorso:

           self._view.txt_result.controls.append(
               ft.Text(f"{b.product_name}"))

       self._view.update_page()













    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
