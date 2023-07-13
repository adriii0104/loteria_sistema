from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QCheckBox, QDesktopWidget, QListView, QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
import sys
import re

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/inicio.ui", self)
        self.Botonlogin.clicked.connect(self.login)
        self.user.returnPressed.connect(self.login)
        self.password.returnPressed.connect(self.login)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)  # Quitar botón de maximizar
        self.setWindowTitle("")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.bodywindow = None
        self.login_window = None
        icon = QIcon("NOTE3710-removebg-preview.png")  # Reemplaza con la ruta de tu archivo de icono
        self.setWindowIcon(icon)

    def keyPressEvent(self, event):
                if event.key() == Qt.Key_Escape:
                    self.close()
                if event.key() == Qt.Key_F5:
                    self.close()
                    if self.login_window is None:
                        self.login_window = LoginWindow()
                    self.login_window.show()


    def login(self):
        usuario = self.user.text()
        password = self.password.text()
        if usuario == "" and password == "":
            self.hide()
            if self.bodywindow is None:
                self.bodywindow = Bodywindow()
                adjustWindowToScreen(self.bodywindow)
            self.bodywindow.show()
        elif usuario == "" and password == "":
            title = "Error"
            icon = QMessageBox.Critical
            text = "Debe introducir al menos un valor"
            ventanta_emergente_def(title, icon, text)
        else:
            title = "Error"
            icon = QMessageBox.Critical
            text = "Nombre de usuario o contraseña incorrectos"
            ventanta_emergente_def(title, icon, text)

class Bodywindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_lotteries = 0
        uic.loadUi("UI/bodyy.ui", self)
        self.siguiente.clicked.connect(self.calculate)
        self.adjustToScreen()
        self.login_window = None
        self.body_window = None
        self.list_view = self.findChild(QListView, "lista_de_jugadas")  # Reemplaza "your_list_view" con el nombre de objeto del QListView en Qt Designer

        checkbox_names = ["AnguiladiezAM", "AnguilaunaPM", "AnguilaseisPM", "AnguilanuevePM", "CuartetadiezAM", "CuartetaunaPM",
                          "CuartetaseisPM", "CuartetanuevePM", "FechaunaPM", "FloridanuevePM", "GanadosPM", "KingdocePM",
                          "KingsietePM", "LeidsaochoPM", "LotekasietePM", "NacionalochoPM", "NewdiezPM", "NewdosPM",
                          "PrimeradocePM", "RealunaPM", "SuertedocePM"]

        for name in checkbox_names:
            checkbox = self.findChild(QCheckBox, name)
            if checkbox:
                checkbox.stateChanged.connect(self.checkbox_state_changed)
        self.precio.returnPressed.connect(self.calculate)  # Conectar la tecla Enter en el campo "monto" al método "calculate"
        self.numero.returnPressed.connect(self.calculate)  # Conectar la tecla Enter en el campo "numero" al método "calculate"


    def calculate(self):
        numero = self.numero.text()
        monto = self.precio.text()

        numero = self.numero.text()
        if numero is not None:
            for i in range(0, len(numero), 2):
                numeros_parte = numero[i:i+2]
                print(numeros_parte)

        totaljugado = self.total_jugado.text()
        #aquí iniciamos diciendo que si  la cantidad de valores que tiene el numero es igual a 4 y la cantidad de valores que tiene el monto es igual o mayor que 1 será un pale
        if monto != '':
            if int(monto) <= 0:
                title = "Error"
                icon = QMessageBox.Critical
                text = "El monto es invalido"
                ventanta_emergente_def(title, icon, text)
        elif len(numero) == 4 and len(monto) >= 1:
            if self.validar_numero_existente(numero[:6], monto):
                title = "Error"
                icon = QMessageBox.Critical
                text = "Los dos primeros números ya existen."
                ventanta_emergente_def(title, icon, text)
            else:
                item_text = f"Palé: {numero}, Monto: {monto}"
                item = QListWidgetItem(item_text)
                self.lista_jugadas.addItem(item)
                self.numero.setText('')
                self.precio.setText('')
                self.numero.setFocus()
            if len(totaljugado) <= 0:
                self.total_jugado.setText(monto)
            else:
                total1 = int(totaljugado) + int(monto)
                self.total_jugado.setText(str(total1))
        elif len(numero) == 4 and len(monto) == 0:
            if self.validar_numero_existente(numero[0:3], monto):
                title = "Error"
                icon = QMessageBox.Critical
                text = "Los dos primeros números ya existen."
                ventanta_emergente_def(title, icon, text)
            else:
                primer_valor = numero[0:2]
                segundo_valor = numero[2:5]
                monto = segundo_valor
                item_text = f"Puntos: {primer_valor}, Monto: {monto}"
                item = QListWidgetItem(item_text)
                self.lista_jugadas.addItem(item)
                self.numero.setText('')
                self.precio.setText('')
            if len(totaljugado) <= 0:
                self.total_jugado.setText(monto)
            else:
                total1 = int(totaljugado) + int(monto)
                self.total_jugado.setText(str(total1))
        
        elif len(numero) == 6 and len(monto) > 0:
            if self.validar_numero_existente(numero[0:5], monto):
                title = "Error"
                icon = QMessageBox.Critical
                text = "Los dos primeros números ya existen."
                ventanta_emergente_def(title, icon, text)
            else:
                item_text = f"Tripleta: {numero}, Monto: {monto}"
                item = QListWidgetItem(item_text)
                self.lista_jugadas.addItem(item)
                self.numero.setText('')
                self.precio.setText('')
                self.numero.setFocus()
            if len(totaljugado) <= 0:
                self.total_jugado.setText(monto)
            else:
                total1 = int(totaljugado) + int(monto)
                self.total_jugado.setText(str(total1))

        elif len(numero) == 6 and len(monto) <= 0:
            if self.validar_numero_existente(numero[:4], monto):
                title = "Error"
                icon = QMessageBox.Critical
                text = "Los dos primeros números ya existen."
                ventanta_emergente_def(title, icon, text)
            else:
                primer_valor = str(numero[0:2])
                segundo_valor = str(numero[2:4])
                total = primer_valor + segundo_valor
                monto = numero[4:6]
                item_text = f"Palé: {total}, Monto: {monto}"
                item = QListWidgetItem(item_text)
                self.lista_jugadas.addItem(item)
                self.numero.setText('')
                self.precio.setText('')
                self.numero.setFocus()
            if len(totaljugado) <= 0:
                self.total_jugado.setText(monto)
            else:
                total1 = int(totaljugado) + int(monto)
                self.total_jugado.setText(str(total1))
        elif len(numero) <= 2 and len(monto) < 1:
            title = "Error"
            icon = QMessageBox.Critical
            text = "Por favor, escribe un valor válido."
            ventanta_emergente_def(title, icon, text)
        elif len(numero) == 2 and len(monto) > 0:
            if self.validar_numero_existente(numero[:2], monto):
                title = "Error"
                icon = QMessageBox.Critical
                text = "Los dos primeros números ya existen."
                ventanta_emergente_def(title, icon, text)
            else:
                item_text = f"Puntos: {numero}, Monto: {monto}"
                item = QListWidgetItem(item_text)
                self.lista_jugadas.addItem(item)
                self.numero.setText('')
                self.precio.setText('')
                self.numero.setFocus()
            if len(totaljugado) <= 0:
                self.total_jugado.setText(monto)
            else:
                total1 = int(totaljugado) + int(monto)
                self.total_jugado.setText(str(total1))
        elif numero == '':
            title = "Error"
            icon = QMessageBox.Critical
            text = "Por favor, escribe un valor válido."
            ventanta_emergente_def(title, icon, text)
        else:
            title = "Error"
            icon = QMessageBox.Critical
            text = "Por favor, escribe un valor válido."
            ventanta_emergente_def(title, icon, text) 
        for i in range(self.lista_jugadas.count()):
                item = self.lista_jugadas.item(i)

    def validar_numero_existente(self, numero, monto):
        for i in range(self.lista_jugadas.count()):
            item = self.lista_jugadas.item(i)
            texto = item.text()
            numeros_extraidos = numero
            valor = numero[4:]
            if numeros_extraidos in texto:
                indice = texto.index(numeros_extraidos)
                print(numeros_extraidos)
                print(monto, "klk")
        return False
    

    def checkbox_state_changed(self, state):
        checkbox = self.sender()
        if state == QtCore.Qt.Checked:
            if self.selected_lotteries < 3:
                self.selected_lotteries += 1
                print(self.selected_lotteries)
            else:
                checkbox.setChecked(False)
                title = "Error"
                icon = QMessageBox.Critical
                text = "Solo se permiten seleccionar 3 loterías."
                ventanta_emergente_def(title, icon, text)
        else:
            self.selected_lotteries -= 1
            print(self.selected_lotteries)

    def adjustToScreen(self):
        desktop = QDesktopWidget().availableGeometry()
        self.setGeometry(desktop)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_F1:
            self.close()
            if self.login_window is None:
                self.login_window = LoginWindow()
            self.login_window.show()
        if event.key() == Qt.Key_F5:
            self.close(65445)
            if self.body_window is None:
                self.body_window = Bodywindow()
            self.body_window.show()

class CobraTicketWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/cobrarticket.ui")


def ventanta_emergente_def(title, icon, text):
    ventana_emergente = QMessageBox()
    ventana_emergente.setWindowTitle(title)
    ventana_emergente.setText(text)
    ventana_emergente.setIcon(icon)
    ventana_emergente.exec_()

def adjustWindowToScreen(window):
    desktop = QDesktopWidget().availableGeometry()
    window.setGeometry(desktop)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())
