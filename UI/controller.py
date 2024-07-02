import time

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selected_state = None
        self._selected_shape = None

    def fillDDStato(self):
        states = self._model._states
        for s in states:
            self._view._DD_stato.options.append(ft.dropdown.Option(data=s, text=s, on_click=self._choice_state))
        self._view.update_page()

    def _choice_state(self, e):
        if e.control.data is None:
            self._selected_state = None
        else:
            self._selected_state = e.control.data


    def fillDDShapes(self):
        shapes = self._model._shapes
        for s in shapes:
            self._view._DD_shape.options.append(ft.dropdown.Option(data=s, text=s, on_click=self._choice_shape))
        self._view.update_page()

    def _choice_shape(self, e):
        if e.control.data is None:
            self._selected_shape = None
        else:
            self._selected_shape = e.control.data



    def handleGrafo(self, e):
        if self._selected_state != None and self._selected_shape != None:
            self._model._crea_grafo(self._selected_shape, self._selected_state)
            nNodi, nArchi = self._model.get_dettagli_grafo()
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text(f"Grafo correttamente creato. Il grafo ha {nNodi} nodi e {nArchi} archi."))
            pesi = self._model.get_pesi()
            for p in pesi:
                self._view.txt_result1.controls.append(ft.Text(f"{p[0]}, peso = {p[1]}"))
            self._view._txtIn_max_citta.disabled = False
            self._view._btn_percorso.disabled = False
        else:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text(f"Errore, selezionare uno stato e una forma."))
            self._view.update_page()
            return

        self._view.update_page()

    def handlePercorso(self, e):
        n_citta = self._view._txtIn_max_citta.value
        try:
            int_n_citta = int(n_citta)
        except ValueError:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text(f"Errore, inserire un valore intero in 'Max città'."))
            self._view.update_page()
            return
        path, n_citta_percorso, peso_tot = self._model._handle_percorso(int_n_citta)
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Trovato percorso che attraversa {n_citta_percorso} e pesante {peso_tot}:"))
        for p in path:
            self._view.txt_result2.controls.append(ft.Text(f"{p[0]} --> {p[1]}, peso = {p[2]}"))
        self._view.update_page()


