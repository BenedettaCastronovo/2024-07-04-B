import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        self._years = self._model.getY()
        for y in self._years:
            self._view.ddyear.options.append(ft.dropdown.Option(key=y,
                                                                on_click=self.choiceY))

        self._view.update_page()

    def choiceY(self, e):
        self.y = e.control.key
        if self.y is not None:
            self.fillS(self.y)

    def fillS(self, y):
        self.s = self._model.getS(y)
        for s in self.s:
            self._view.ddstate.options.append(ft.dropdown.Option(
                key=s.id,
                data = s,
                text = s.name))
        self._view.update_page()

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        self.s = self._view.ddstate.value
        if self.s is None or self.y is None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("seleziona"))
            self._view.update_page()
            return

        self._model.creaG(self.y, self.s)
        self._view.txt_result1.controls.append(ft.Text("grafo creato"))
        nodi, archi = self._model.len()
        self._view.txt_result1.controls.append(ft.Text(f"nodi: {nodi} - archi: {archi}"))
        lun, mas = self._model.stampa()
        self._view.txt_result1.controls.append(ft.Text(f"lun: {lun}"))
        for n in mas:
            self._view.txt_result1.controls.append(ft.Text(f"mas: {n}"))
        self._view.update_page()


    def handle_path(self, e):
        best, punti = self._model.cerca()
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"punti: {punti}"))
        for n in best:
            self._view.txt_result2.controls.append(ft.Text(f"n: {n}"))
        self._view.update_page()
