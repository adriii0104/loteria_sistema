from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QCheckBox, QDesktopWidget, QListView, QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
import sys
import re
import mysql.connector

conexion = mysql.connector.connect(
    host = 'localhost',
    user =  'root',
    password = '',
    db = 'lotteria_genuine'
)








class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/inicio.ui", self)
        self.Botonlogin.clicked.connect(self.login)
        self.user.returnPressed.connect(self.login)
        self.password.returnPressed.connect(self.login)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)  # Quitar botón de maximizar
        self.setWindowTitle("BFS SP#01")
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
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM auth WHERE username = %s", (usuario, ))
        usuario = cursor.fetchone()

        if usuario == '' or password == '':
                title = "Error"
                icon = QMessageBox.Critical
                text = "Por favor ingrese el usuario o la contraseña"
                ventanta_emergente_def(title, icon, text)
        elif usuario is not None:
            password_data = usuario[2]
            if password == password_data:
                self.hide()
                if self.bodywindow is None:
                    self.bodywindow = Bodywindow()
                    adjustWindowToScreen(self.bodywindow)
                self.bodywindow.show()
            else:
                title = "Error"
                icon = QMessageBox.Critical
                text = "Nombre de usuario o contraseña incorrectos"
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
        #este es el area de los botones con conexiones a funciones. ---------------------------------
        self.siguiente.clicked.connect(self.calculate)
        self.amount.returnPressed.connect(self.calculate)  # Conectar la tecla Enter en el campo "monto" al método "calculate"
        self.numero.returnPressed.connect(self.calculate)
        self.lista_jugadas.itemClicked.connect(self.delete_item)
        self.total_una_loteria.setText('0')
        self.total_jugado.setText('0')
        self.ESC.clicked.connect(self.cerrar)
        self.F11.clicked.connect(self.limpiar)


        #Fin. ---------------------------------
        self.adjustToScreen()
        self.setWindowTitle("BFS SP#01")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.login_window = None
        self.body_window = None
        self.cobrar_ticket = None
        self.list_view = self.findChild(QListView, "lista_de_jugadas")  # Reemplaza "your_list_view" con el nombre de objeto del QListView en Qt Designer

        checkbox_names = ["AnguiladiezAM", "AnguilaunaPM", "AnguilaseisPM", "AnguilanuevePM", "CuartetadiezAM", "CuartetaunaPM",
                          "CuartetaseisPM", "CuartetanuevePM", "FechaunaPM", "FloridanuevePM", "GanadosPM", "KingdocePM",
                          "KingsietePM", "LeidsaochoPM", "LotekasietePM", "NacionalochoPM", "NewdiezPM", "NewdosPM",
                          "PrimeradocePM", "RealunaPM", "SuertedocePM"]

        for name in checkbox_names:
            checkbox = self.findChild(QCheckBox, name)
            if checkbox:
                checkbox.stateChanged.connect(self.checkbox_state_changed)

    def calculate(self):
        numero = self.numero.text()
        monto =  self.amount.text()

        if numero is not None:
            for i in range(0, len(numero), 2):
                numeros_parte = numero[i:i+2]

        totaljugado = self.total_jugado.text()

        if monto is None:
            if int(monto) <= 0:
                title = "Error"
                icon = QMessageBox.Critical
                text = "El monto es inválido"
                ventanta_emergente_def(title, icon, text)
        elif len(numero) == 4 and len(monto) >= 1:
            if self.validar_numero_existente(numero[:6], monto):
                title = "Error"
                icon = QMessageBox.Critical
                text = "Los dos primeros números ya existen."
                ventanta_emergente_def(title, icon, text)
            else:
                if int(monto) <= 0:
                    title = "Error"
                    icon = QMessageBox.Critical
                    text = "El monto es inválido, por favor ingrese un monto valido."
                    self.numero.setText('')
                    self.amount.setText('')
                    self.numero.setFocus()
                    ventanta_emergente_def(title, icon, text)
                else:
                    item_text = f"{numero}"
                    item_text1 = f"{monto}"
                    item = QListWidgetItem(item_text)
                    item1 = QListWidgetItem(item_text1)
                    self.lista_jugadas.addItem(item)
                    self.lista_montos.addItem(item1)
                    self.numero.setText('')
                    self.amount.setText('')
                    self.numero.setFocus()
                    self.check_balance(monto)
                    if totaljugado != '':
                        totalhoy = int(totaljugado)
                    else:
                        totalhoy = 0
                    if totalhoy <= 0:
                        if self.selected_lotteries <= 0:
                            self.total_jugado.setText(str(0))
                        else:
                            totaltoday = int(monto) * int(self.selected_lotteries)
                            self.total_jugado.setText(str(totaltoday))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = int(monto) * int(self.selected_lotteries) + int(totalhoy)
                            self.total_jugado.setText(str(totaltoday))
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
                if int(monto) <= 0:
                    title = "Error"
                    icon = QMessageBox.Critical
                    text = "El monto es inválido, por favor ingrese un monto valido."
                    self.numero.setText('')
                    self.amount.setText('')
                    self.numero.setFocus()
                    ventanta_emergente_def(title, icon, text)
                else:
                    item_text1 = f"{monto}"
                    item_text = f"{primer_valor}"
                    item1 = QListWidgetItem(item_text1)
                    item = QListWidgetItem(item_text)
                    self.lista_jugadas.addItem(item)
                    self.lista_montos.addItem(item1)
                    self.numero.setText('')
                    self.amount.setText('')
                    self.check_balance(monto)
                    if totaljugado != '':
                        totalhoy = int(totaljugado)
                    else:
                        totalhoy = 0
                    if totalhoy <= 0:
                        if self.selected_lotteries <= 0:
                            self.total_jugado.setText(str(0))
                        else:
                            totaltoday = int(monto) * int(self.selected_lotteries)
                            self.total_jugado.setText(str(totaltoday))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = int(monto) * int(self.selected_lotteries) + int(totalhoy)
                            self.total_jugado.setText(str(totaltoday))
        elif len(numero) == 5 and len(monto) <= 0:
            if self.validar_numero_existente(numero[0:3], monto):
                title = "Error"
                icon = QMessageBox.Critical
                text = "Los dos primeros números ya existen."
                ventanta_emergente_def(title, icon, text)
            else:
                primer_valor = numero[0:2]
                monto = numero[2:7]
                if int(monto) <= 0:
                    title = "Error"
                    icon = QMessageBox.Critical
                    text = "El monto es inválido, por favor ingrese un monto valido."
                    self.numero.setText('')
                    self.amount.setText('')
                    self.numero.setFocus()
                    ventanta_emergente_def(title, icon, text)
                else:
                    item_text = f"{primer_valor}"
                    item_text1 = f"{monto}"
                    item1 = QListWidgetItem(item_text1)
                    item = QListWidgetItem(item_text)
                    self.lista_jugadas.addItem(item)
                    self.lista_montos.addItem(item1)
                    self.numero.setText('')
                    self.amount.setText('')
                    self.check_balance(monto)
                    if totaljugado != '':
                        totalhoy = int(totaljugado)
                    else:
                        totalhoy = 0
                    if totalhoy <= 0:
                        if self.selected_lotteries <= 0:
                            self.total_jugado.setText(str(0))
                        else:
                            totaltoday = int(monto) * int(self.selected_lotteries)
                            self.total_jugado.setText(str(totaltoday))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = int(monto) * int(self.selected_lotteries) + int(totalhoy)
                            self.total_jugado.setText(str(totaltoday))

        elif len(numero) == 6 and len(monto) > 0:
            if self.validar_numero_existente(numero[0:5], monto):
                title = "Error"
                icon = QMessageBox.Critical
                text = "Los dos primeros números ya existen."
                self.numero.setFocus()
                ventanta_emergente_def(title, icon, text)
            else:
                if int(monto) <= 0:
                    title = "Error"
                    icon = QMessageBox.Critical
                    text = "El monto es inválido, por favor ingrese un monto valido."
                    self.numero.setText('')
                    self.amount.setText('')
                    self.numero.setFocus()
                    ventanta_emergente_def(title, icon, text)
                else:
                    item_text = f"{numero}"
                    item_text1 = f"{monto}"
                    item = QListWidgetItem(item_text)
                    item1 = QListWidgetItem(item_text1)
                    self.lista_jugadas.addItem(item)
                    self.lista_montos.addItem(item1)
                    self.numero.setText('')
                    self.amount.setText('')
                    self.numero.setFocus()
                    self.check_balance(monto)
                    if totaljugado != '':
                        totalhoy = int(totaljugado)
                    else:
                        totalhoy = 0
                    if totalhoy <= 0:
                        if self.selected_lotteries <= 0:
                            self.total_jugado.setText(str(0))
                        else:
                            totaltoday = int(monto) * int(self.selected_lotteries)
                            self.total_jugado.setText(str(totaltoday))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = int(monto) * int(self.selected_lotteries) + int(totalhoy)
                            self.total_jugado.setText(str(totaltoday))
        elif len(numero) == 7 or len(numero) == 8 and len(monto) <= 0:
            if self.validar_numero_existente(numero[:4], monto):
                title = "Error"
                icon = QMessageBox.Critical
                text = "Los dos primeros números ya existen."
                self.numero.setText('')
                self.amount.setText('')
                ventanta_emergente_def(title, icon, text)
            else:
                primer_valor = str(numero[0:2])
                segundo_valor = str(numero[2:4])
                total = primer_valor + segundo_valor
                monto = numero[4:20]
                if int(monto) <= 0:
                    title = "Error"
                    icon = QMessageBox.Critical
                    text = "El monto es inválido, por favor ingrese un monto valido."
                    self.numero.setText('')
                    self.amount.setText('')
                    self.numero.setFocus()
                    ventanta_emergente_def(title, icon, text)
                else:
                    item_text = f"{total}"
                    item_text1 = f"{monto}"
                    item = QListWidgetItem(item_text)
                    item1 = QListWidgetItem(item_text1)
                    self.lista_montos.addItem(item1)
                    self.lista_jugadas.addItem(item)
                    self.numero.setText('')
                    self.amount.setText('')
                    self.numero.setFocus()
                    self.check_balance(monto)
                    if totaljugado != '':
                        totalhoy = int(totaljugado)
                    else:
                        totalhoy = 0
                    if totalhoy <= 0:
                        if self.selected_lotteries <= 0:
                            self.total_jugado.setText(str(0))
                        else:
                            totaltoday = int(monto) * int(self.selected_lotteries)
                            self.total_jugado.setText(str(totaltoday))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = int(monto) * int(self.selected_lotteries) + int(totalhoy)
                            self.total_jugado.setText(str(totaltoday))
        elif len(numero) == 6 and len(monto) <= 0:
            if self.validar_numero_existente(numero[:4], monto):
                title = "Error"
                icon = QMessageBox.Critical
                text = "Los dos primeros números ya existen."
                self.numero.setText('')
                self.amount.setText('')
                ventanta_emergente_def(title, icon, text)
            else:
                primer_valor = str(numero[0:2])
                segundo_valor = str(numero[2:4])
                total = primer_valor + segundo_valor
                monto = numero[4:6]
                if int(monto) <= 0:
                    title = "Error"
                    icon = QMessageBox.Critical
                    text = "El monto es inválido, por favor ingrese un monto valido."
                    self.numero.setText('')
                    self.amount.setText('')
                    self.numero.setFocus()
                    ventanta_emergente_def(title, icon, text)
                else:
                    item_text = f"{total}"
                    item_text1 = f"{monto}"
                    item = QListWidgetItem(item_text)
                    item1 = QListWidgetItem(item_text1)
                    self.lista_montos.addItem(item1)
                    self.lista_jugadas.addItem(item)
                    self.numero.setText('')
                    self.amount.setText('')
                    self.numero.setFocus()
                    self.check_balance(monto)
                    if totaljugado != '':
                        totalhoy = int(totaljugado)
                    else:
                        totalhoy = 0
                    if totalhoy <= 0:
                        if self.selected_lotteries <= 0:
                            self.total_jugado.setText(str(0))
                        else:
                            totaltoday = int(monto) * int(self.selected_lotteries)
                            self.total_jugado.setText(str(totaltoday))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = int(monto) * int(self.selected_lotteries) + int(totalhoy)
                            self.total_jugado.setText(str(totaltoday))
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
                self.numero.setText('')
                self.amount.setText('')
            else:
                if int(monto) <= 0:
                    title = "Error"
                    icon = QMessageBox.Critical
                    text = "El monto es inválido, por favor ingrese un monto valido."
                    self.numero.setText('')
                    self.amount.setText('')
                    self.numero.setFocus()
                    ventanta_emergente_def(title, icon, text)
                else:
                    item_text = f"{numero}"
                    item_text1 = f"{monto}"
                    item = QListWidgetItem(item_text)
                    item1 = QListWidgetItem(item_text1)
                    self.lista_jugadas.addItem(item)
                    self.lista_montos.addItem(item1)
                    self.numero.setText('')
                    self.amount.setText('')
                    self.numero.setFocus()
                    self.check_balance(monto)
                    if totaljugado != '':
                        totalhoy = int(totaljugado)
                    else:
                        totalhoy = 0
                    if totalhoy <= 0:
                        if self.selected_lotteries <= 0:
                            self.total_jugado.setText(str(0))
                        else:
                            totaltoday = int(monto) * int(self.selected_lotteries)
                            self.total_jugado.setText(str(totaltoday))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = int(monto) * int(self.selected_lotteries) + int(totalhoy)
                            self.total_jugado.setText(str(totaltoday))
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
        return False
    

    def cerrar(self):
        self.close()
    def limpiar(self):
            self.lista_jugadas.clear()
            self.lista_montos.clear()
            self.total_una_loteria.setText('0')
            self.total_jugado.setText('0')

    def checkbox_state_changed(self, state):
        checkbox = self.sender()
        if state == QtCore.Qt.Checked:
            self.selected_lotteries += 1
            total = 0
            for i in range(self.lista_montos.count()):
                item = self.lista_montos.item(i)
                texto = item.text()
                numero = int(texto)
                total += numero 
            total_jugado = self.total_jugado.text()
            if total_jugado:
                jugado = int(total_jugado)
                total_jugado1 = total * self.selected_lotteries
            else:
                jugado = 0
                total_jugado1 = total * self.selected_lotteries

            self.total_jugado.setText(str(total_jugado1))
        else:
            self.selected_lotteries -= 1
            total = 0
            for i in range(self.lista_montos.count()):
                item = self.lista_montos.item(i)
                texto = item.text()
                numero = int(texto)
                total += numero

            total_jugado = self.total_jugado.text()
            if total_jugado:
                jugado = int(total_jugado)
                total_jugado1 = total * self.selected_lotteries
            else:
                jugado = 0
                total_jugado1 = total * self.selected_lotteries

            self.total_jugado.setText(str(total_jugado1))

    def check_balance(self, monto):
            total_una_loteria = self.total_una_loteria.text()
            if total_una_loteria == '':
                self.total_una_loteria.setText(monto)
            else:
                total_loteria = int(self.total_una_loteria.text()) + int(monto)
                self.total_una_loteria.setText(str(total_loteria))

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
            self.close()
            if self.body_window is None:
                self.body_window = Bodywindow()
            self.body_window.show()
        if event.key() == Qt.Key_F7:
            if self.cobrar_ticket is None:
                self.cobrar_ticket = CobrarTicketWindow()
            self.cobrar_ticket.show()
        if event.key() == Qt.Key_F11:
            self.lista_jugadas.clear()
            self.lista_montos.clear()
            self.total_una_loteria.setText('0')
            self.total_jugado.setText('0')
            

    def delete_item(self, item):
            reply = QMessageBox.question(self, "Eliminar número", "¿Estás seguro de que deseas eliminar este número?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                selected_items = self.lista_jugadas.selectedItems()
                for item in selected_items:
                    row = self.lista_jugadas.row(item)
                    monto_item = self.lista_montos.takeItem(row)
                    self.lista_jugadas.takeItem(row)
                    
                    monto = int(monto_item.text())
                    resultado_actual = int(self.total_jugado.text())
                    resultado_actual -= monto
                    resultado_jugadas = int(self.total_una_loteria.text())
                    resultado_jugadas -= monto
                    if resultado_actual >= 0:
                        self.total_jugado.setText(str(resultado_actual))
                    self.total_una_loteria.setText(str(resultado_jugadas))

        

class CobrarTicketWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/cobrarticket.ui", self)


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
