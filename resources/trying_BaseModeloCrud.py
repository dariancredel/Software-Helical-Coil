import os
import json
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.Qt import QModelIndex, QVariant


class BaseTableModel(QAbstractTableModel):
    def __init__(self, parent=None, nombre_fichero=""):
        QAbstractTableModel.__init__(self, parent)
        self.nombre_fichero = os.getcwd() + "/data/" + nombre_fichero
        self.datos = []
        self.modificado = False
        self.HEADER_TEXT = {}

    def rowCount(self, index=QModelIndex()):
        return len(self.datos)

    def columnCount(self, index=QModelIndex()):
        return len(self.HEADER_TEXT)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.TextAlignmentRole:
                return (QVariant(int(Qt.AlignCenter | Qt.AlignVCenter)))
            elif role == Qt.DisplayRole:
                return QVariant(self.HEADER_TEXT[section])

        return QVariant()

    def nuevo(self, dato):
        if not dato:
            raise Exception("No puede haber datos en blanco")

        self.beginResetModel()
        self.datos.append(dato)
        self.endResetModel()
        self.modificado = True

    def editar(self, dato, rowId):
        if rowId < 0 or not dato:
            raise Exception("Parametros incorrectos")

        self.beginResetModel()
        self.datos[rowId] = dato
        self.endResetModel()
        self.modificado = True
        
    def borrar(self, rowId):
        self.beginResetModel()
        self.datos.pop(rowId)
        self.endResetModel()
        self.modificado = True

    def save(self):
            lista = []
            for dato in self.datos:
                lista.append(dato.get_dict())

            try:
                fichero = open(self.nombre_fichero, "w")
                json.dump(lista, fichero)
                fichero.close()

            except Exception as err:
                raise err

    def _dict_objecto(self, lista):
        raise NotImplementedError

    def load(self):
        self.beginResetModel()
        lista = []
        try:
            fichero = open(self.nombre_fichero, "r")
            lista = json.load(fichero)
            fichero.close()
        except FileNotFoundError:
            self.datos = []
            return

        self.datos = self._dict_objecto(lista)
        self.endResetModel()

    def get_elemento(self, pos):
        return self.datos[pos]

class myWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.model = BaseTableModel(self)
        self.model.load()

if __name__=='__main__':
    app = QApplication([])
    win = myWindow()
    win.show()
    app.exec()