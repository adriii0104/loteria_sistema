from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QCheckBox, QDesktopWidget, QListView, QListWidgetItem, QPushButton
from PyQt5.QtGui import QIcon, QPainter, QFont
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import Qt
import sys
import re
import mysql.connector
from drawticket import generar_recibo
import uuid
from datetime import datetime
import hashlib

conexion = mysql.connector.connect(
    host = 'localhost',
    user =  'root',
    password = '',
    db = 'lotteria_genuine'
)
conexion2 = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    db = 'resultados'
)
sesion_usuario = {}

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/inicio.ui", self)
        self.Botonlogin.clicked.connect(self.login)
        self.user.returnPressed.connect(self.focus)
        self.password.returnPressed.connect(self.login)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("LOTERIA")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.bodywindow = None
        self.login_window = None
        self.admin_window = None
        self.add_numbers_window = None
        icon = QIcon("NOTE3710-removebg-preview.png")  # Reemplaza con la ruta de tu archivo de icono
        self.setWindowIcon(icon)

    def focus(self):
        self.password.setFocus()

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
        usuario.lower()
        password = self.password.text()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM auth WHERE user = %s", (usuario, ))
        usuario_log = cursor.fetchone()

        if usuario == '' or password == '':
                title = "Error"
                icon = QMessageBox.Critical
                text = "Por favor ingrese el usuario o la contraseña"
                ventanta_emergente_def(title, icon, text)
        elif usuario_log is not None:
            password_data = usuario_log[3]
            if password == password_data:
                self.hide()
                if usuario_log[2] == "adminsoftwarelotterie":
                    self.hide()
                    if self.admin_window is None:
                        self.admin_window = Adminwindow()
                        adjustWindowToScreen(self.admin_window)
                    self.admin_window.show()
                elif usuario_log[2] == "lotterie_update":
                    self.close()
                    if self.add_numbers_window is None:
                        self.add_numbers_window = Addnumbers()
                    self.add_numbers_window.show()
                else:
                    cursor2 = conexion.cursor()
                    cursor2.execute("SELECT * FROM banca WHERE idbanca = %s", (usuario_log[1], ))
                    datos = cursor2.fetchone()
                    sesion_usuario['id_banca'] = datos[1]
                    sesion_usuario['nombre_banca'] = datos[2]
                    sesion_usuario['pago_punto'] = datos[10]
                    sesion_usuario['pago_pale'] = datos[11]
                    sesion_usuario['pago_tripleta'] = datos[12]
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
        uic.loadUi("UI/body.ui", self)
        #este es el area de los botones con conexiones a funciones. ---------------------------------
        self.siguiente.clicked.connect(self.calculate)
        self.amount.returnPressed.connect(self.calculate)  # Conectar la tecla Enter en el campo "monto" al método "calculate"
        self.numero.returnPressed.connect(self.calculate)
        self.lista_jugadas.itemClicked.connect(self.delete_item)
        self.total_una_loteria.setText('0')
        self.total_jugado.setText('0')
        self.ESC.clicked.connect(self.cerrar)
        self.F11.clicked.connect(self.limpiar)
        self.numero.setValidator(QtGui.QIntValidator())
        self.amount.setValidator(QtGui.QIntValidator())
        id_banca = sesion_usuario.get('id_banca')
        nombre_banca = sesion_usuario.get('nombre_banca')


        #Fin. ---------------------------------
        self.adjustToScreen()
        self.setWindowTitle(nombre_banca)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.login_window = None
        self.body_window = None
        self.cobrar_ticket = None
        self.list_view = self.findChild(QListView, "lista_de_jugadas")  # Reemplaza "your_list_view" con el nombre de objeto del QListView en Qt Designer


        
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
                    item_primero = numero[:2]
                    item_segundo = numero[2:4]
                    jugada_total = item_primero + '-' + item_segundo + "Palé"
                    monto.format()
                    
                    item_text1 = f"{monto}"
                    item = QListWidgetItem(jugada_total)
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
                    number_for_process = int(monto)
                    numero_formateado = "{:,.2f}".format(number_for_process)
                    item_text1 = f"{numero_formateado}"
                    item_text = f"{primer_valor} (Quiniela)"
                    item1 = QListWidgetItem(item_text1)
                    item = QListWidgetItem(item_text)
                    self.lista_jugadas.addItem(item)
                    self.lista_montos.addItem(item1)
                    self.numero.setText('')
                    self.amount.setText('')
                    self.check_balance(monto)
                    if totaljugado != '':
                        totalhoy = float(totaljugado)
                    else:
                        totalhoy = 0
                    if totalhoy <= 0:
                        if self.selected_lotteries <= 0:
                            self.total_jugado.setText(str(0))
                        else:
                            totaltoday = float(monto) * float(self.selected_lotteries)
                            self.total_jugado.setText(str(totaltoday))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = float(monto) * float(self.selected_lotteries) + float(totalhoy)
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
                    number_for_process = int(monto)
                    numero_formateado = "{:,.2f}".format(number_for_process)
                    item_text = f"{primer_valor} (Quiniela)"
                    monto.format()
                    item_text1 = f"{numero_formateado}"
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
                    primera_parte = numero[:2]
                    segunda_parte = numero[2:4]
                    tercera_parte = numero[4:6]
                    jugada_final = primera_parte + "-" + segunda_parte + "-" + tercera_parte + " (Tripleta)"
                    number_for_process = int(monto)
                    numero_formateado = "{:,.2f}".format(number_for_process)
                    item_text1 = f"{numero_formateado}"
                    item = QListWidgetItem(jugada_final)
                    item1 = QListWidgetItem(item_text1)
                    self.lista_jugadas.addItem(item)
                    self.lista_montos.addItem(item1)
                    self.numero.setText('')
                    self.amount.setText('')
                    self.numero.setFocus()
                    self.check_balance(monto)
                    if totaljugado != '':
                        totalhoy = float(totaljugado)
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
                total = primer_valor + "-" + segundo_valor
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
                    item_text = f"{total} (Palé)"
                    number_for_process = int(monto)
                    numero_formateado = "{:,.2f}".format(number_for_process)
                    item_text1 = f"{numero_formateado}"
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
                total = primer_valor + "-" + segundo_valor
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
                    item_text = f"{total} (Palé)"
                    number_for_process = int(monto)
                    numero_formateado = "{:,.2f}".format(number_for_process)
                    item_text1 = f"{numero_formateado}"
                    item = QListWidgetItem(item_text)
                    item1 = QListWidgetItem(item_text1)
                    self.lista_montos.addItem(item1)
                    self.lista_jugadas.addItem(item)
                    self.numero.setText('')
                    self.amount.setText('')
                    self.numero.setFocus()
                    self.check_balance(monto)
                    if totaljugado != '':
                        totalhoy = float(totaljugado)
                    else:
                        totalhoy = 0
                    if totalhoy <= 0:
                        if self.selected_lotteries <= 0:
                            self.total_jugado.setText(str(0))
                        else:
                            totaltoday = float(monto) * float(self.selected_lotteries)
                            self.total_jugado.setText(str(totaltoday))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = float(monto) * float(self.selected_lotteries) + float(totalhoy)
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
                    item_text = f"{numero} (Quiniela)"
                    number_for_process = int(monto)
                    numero_formateado = "{:,.2f}".format(number_for_process)
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
                numero = float(texto)
                total += numero 

            total_jugado = self.total_jugado.text()
            if total_jugado:
                jugado = float(total_jugado)
                total_jugado1 = total * self.selected_lotteries
            else:
                jugado = 0
                total_jugado1 = total * self.selected_lotteries

            self.total_jugado.setText(str(total_jugado1))

            # Imprimir nombre del checkbox seleccionado
            checkbox_name = checkbox.text()
            checkbox_selected_names.append(checkbox_name)
            # Verificar si el valor del checkbox seleccionado existe en el diccionario y obtener su clave
            clave_del_checkbox = obtener_clave_por_valor(checkbox_names, checkbox_name)
            checkbox_selected_lotteries.append(clave_del_checkbox)
            #for i in range(len(checkbox_selected_lotteries)):
                            #print("Loterias definitivas positivas" + checkbox_selected_lotteries[i])
                            #print("Seleccionadas vlores positivas " + checkbox_selected_names[i])

            # Imprimir la clave del checkbox seleccionado
        else:
            self.selected_lotteries -= 1
            total = 0
            checkbox_name = checkbox.text()
            checkbox_selected_names.remove(checkbox_name)
            clave_del_checkbox = obtener_clave_por_valor(checkbox_names, checkbox_name)
            checkbox_selected_lotteries.remove(clave_del_checkbox) 


            for i in range(self.lista_montos.count()):
                item = self.lista_montos.item(i)
                texto = item.text()
                numero = float(texto)
                total += numero

            total_jugado = self.total_jugado.text()
            if total_jugado:
                jugado = float(total_jugado)
                total_jugado1 = total * self.selected_lotteries
            else:
                jugado = 0
                total_jugado1 = total * self.selected_lotteries

            self.total_jugado.setText(str(total_jugado1))

            # Imprimir nombre del checkbox seleccionado
            checkbox_name = checkbox.text()


    def check_balance(self, monto):
        total_una_loteria = self.total_una_loteria.text()
        if total_una_loteria == '':
            number_for_process = float(monto)
            numero_formateado = "{:,.2f}".format(number_for_process)
            self.total_una_loteria.setText(str(numero_formateado))
        else:
            total_loteria = float(self.total_una_loteria.text()) + float(monto)
            number_for_process = total_loteria
            numero_formateado = "{:,.2f}".format(number_for_process)
            self.total_una_loteria.setText(str(numero_formateado))


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
        if event.key() == Qt.Key_F10:
                self.imprimir_ticket()


    #falta todvia agregarle lo de los numeros, falta todavia integrarle el conteo, todavia hay que pasarlo a imprimir. (pendiente)
    def imprimir_ticket(self):
        nombre_banca = sesion_usuario.get('nombre_banca')
        id_banca = sesion_usuario.get('id_banca')
        if len(self.lista_montos) == 0:
            title = "Error"
            icon = QMessageBox.Critical
            text = "Antes de imprimir debes escribir las jugadas."
            ventanta_emergente_def(title, icon, text)
        elif self.selected_lotteries == 0:
            title = "Error"
            icon = QMessageBox.Critical
            text = "Debe elegir al menos una loteria."
            ventanta_emergente_def(title, icon, text)
        else:
            chosen_numbers = []
            amounts = []
            id = uuid.uuid4()
            idgen = str(id)
            idgen = idgen[:10]
            nuevo = idgen.replace("-", "")
            ticket = "BFSSP01"
            idticket = nuevo.upper() + ticket
            archivo_pdf_azar = nuevo + ".pdf"
            total_precio = float(self.total_jugado.text())

            for i in range(self.lista_montos.count()):
                item = self.lista_montos.item(i)
                amount = item.text()
                items = self.lista_jugadas.item(i)
                chosen_number = items.text()
                added_elements = i + 1
                chosen_numbers.append(str(chosen_number))
                amounts.append(str(amount))
        
            for checkbox_name in checkbox_selected_names:
                lotteries_for_database = checkbox_name

            for checkbox_name_loterries in checkbox_selected_lotteries:
                

                for i in range(len(chosen_numbers)):
                    item_for_database = self.lista_jugadas.item(i)
                    item_for_database_text = item_for_database.text()
                    amount_for_database = self.lista_montos.item(i)
                    amount_for_database_text = amount_for_database.text()
                    numeros_con_signo = re.sub(r"[^\d-]", "", item_for_database_text)

                    cursor = conexion.cursor()
                    cursor.execute("INSERT INTO jugadas VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                   (id_banca, idticket, numeros_con_signo, amount_for_database_text, lotteries_for_database, datetime.now().strftime('%d/%m/%Y - %I:%M:%S %p'), "NO", checkbox_name_loterries))
                    cursor.close()
                    cursor2 = conexion.cursor()
                    cursor2.execute("UPDATE ganancias SET numeros_vendidos = numeros_vendidos + 1, venta_diaria = venta_diaria + %s, venta_total = venta_total + %s WHERE id_banca = %s", (amount_for_database_text, amount_for_database_text, id_banca, ))
                    cursor2.close()
                    conexion.commit()

            self.limpiar_ventana()
            generar_recibo(nombre_banca, added_elements, chosen_numbers, amounts, total_precio, archivo_pdf_azar, idticket, checkbox_selected_names)


    def limpiar_ventana(self):
        checkboxes = self.findChildren(QCheckBox)

        # Deseleccionar todos los checkboxes encontrados
        for checkbox in checkboxes:
            checkbox.setChecked(False)
        self.total_jugado.setText('0')
        self.total_una_loteria.setText('0')
        self.lista_montos.clear()
        self.lista_jugadas.clear()

            


    def delete_item(self, item):
            reply = QMessageBox.question(self, "Eliminar número", "¿Estás seguro de que deseas eliminar este número?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                selected_items = self.lista_jugadas.selectedItems()
                for item in selected_items:
                    row = self.lista_jugadas.row(item)
                    monto_item = self.lista_montos.takeItem(row)
                    self.lista_jugadas.takeItem(row)
                    
                    monto = float(monto_item.text())
                    resultado_actual = float(self.total_jugado.text())
                    resultado_actual -= monto
                    resultado_jugadas = float(self.total_una_loteria.text())
                    resultado_jugadas -= monto
                    if resultado_actual >= 0:
                        self.total_jugado.setText(str(resultado_actual))
                    self.total_una_loteria.setText(str(resultado_jugadas))

  
checkbox_selected_names = []
checkbox_selected_lotteries = []   
primer = []
class CobrarTicketWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/cobrarticket.ui", self)
        self.verificar_id.clicked.connect(self.verificar_ticket)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
    def keyPressEvent(self, event):
            if event.key() == Qt.Key_Escape:
                self.close()



    def verificar_ticket(self):
        pago_punto = sesion_usuario.get('pago_punto')
        pago_pale = sesion_usuario.get('pago_pale')
        pago_tripleta = sesion_usuario.get('pago_tripleta')
        id_ticket = self.id_ticket.text()
        self.id_ticket.setText("")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM jugadas WHERE id_ticket = %s", (id_ticket, ))
        ticket = cursor.fetchall()
        if ticket == []:
            title = "Error"
            icon = QMessageBox.Critical
            text = "Ticket no encontrado, asegurate de ingresar correctamente los datos."
            ventanta_emergente_def(title, icon, text)
        
        elif ticket is not None:
            for i in range(len(ticket)):
                numero = ticket[i][1]
                monto = ticket[i][2]
                loteria = ticket[i][3]
                fecha = ticket[i][4]
                cobrado = ticket[i][5]
                key_loteria = ticket[i][6].lower()
                fecha_for_verifying = fecha[:10]
            
                cursor2 = conexion2.cursor()
                if cobrado == "SI":
                    title = "Error"
                    icon = QMessageBox.Critical
                    text = "Este ticket ya fue canjeado."
                    self.id_ticket.setText('')
                    self.id_ticket.setFocus()
                    ventanta_emergente_def(title, icon, text)
                    break
                else:
                                    # Generamos un patrón para la expresión regular que represente todas las posibles permutaciones del número
                    patron = ''.join(f"(?=.*{digito})" for digito in numero)
                    query = f"SELECT * FROM {key_loteria} WHERE resultados REGEXP %s AND fecha = %s"
                    cursor2.execute(query, (patron, fecha_for_verifying))
                    ganador = cursor2.fetchone()
                    if ganador is not None:
                        numeros_a_buscar = numero.split('-')
                        print(numeros_a_buscar)
                        for x in numeros_a_buscar:
                            pass
                        if x in ganador[1]:
                            print(numero)
                            if len(numero) == 2:
                                if numero in ganador[1][:2]:
                                    primera = float(monto) * 12
                                    primer.append(primera)
                                elif numero in ganador[1][2:5]:
                                    segunda = float(monto) * 8
                                    primer.append(segunda)
                                else:
                                    tercera = float(monto) * 4
                                    primer.append(tercera)
                            elif len(numero) == 5:
                                tercera = float(monto) * pago_pale
                                primer.append(tercera)
                            elif len(numero) == 8:
                                primera = float(monto) * pago_tripleta
                                primer.append(primera)
                        else:
                            title = "Error"
                            icon = QMessageBox.Critical
                            text = "Ticket no ganador."
                            ventanta_emergente_def(title, icon, text)                            
                    else:
                        title = "Error"
                        icon = QMessageBox.Critical
                        text = "Ticket no ganador."
                        ventanta_emergente_def(title, icon, text)
            monto_pagar(primer, id_ticket)

        elif ticket == "":
            title = "Error"
            icon = QMessageBox.Critical
            text = "Ticket no encontrado, asegurate de ingresar correctamente los datos."
            ventanta_emergente_def(title, icon, text)



def monto_pagar(primer, id_ticket):
    suma = sum(primer)  # Sumar los montos en la lista
    title = "Felicidades"
    icon = QMessageBox.Information
    text = f"Ticket Ganador, pague la cantidad de {suma}"
    print(primer)
    primer.clear()

    ventana_emergente = QMessageBox()
    ventana_emergente.setWindowTitle(title)
    ventana_emergente.setText(text)
    ventana_emergente.setIcon(icon)
    # Crear un botón personalizado y agregarlo a la ventana emergente
    boton_pagar = QPushButton("Pagar")
    ventana_emergente.addButton(boton_pagar, QMessageBox.YesRole)

    # Agregar el botón "Cancelar" y establecerlo como el botón por defecto
    boton_cancelar = ventana_emergente.addButton("Cancelar", QMessageBox.NoRole)
    ventana_emergente.setDefaultButton(boton_cancelar)

    # Mostrar la ventana emergente y esperar a que el usuario interactúe con ella
    resultado = ventana_emergente.exec_()

    # Comprobar si el botón "Pagar" fue presionado
    if ventana_emergente.clickedButton() == boton_pagar:
        print(id_ticket)
        try:
            cursor = conexion.cursor()
            nuevo_estado_cobrado = "SI"

            # Utilizamos la sentencia UPDATE para modificar el estado 'cobrado' del ticket con el ID especificado
            sentencia_sql = "UPDATE jugadas SET cobrado = %s WHERE id_ticket = %s"
            valores = (nuevo_estado_cobrado, id_ticket)

            # Ejecutamos la sentencia SQL
            cursor.execute(sentencia_sql, valores)

            # Confirmar los cambios en la base de datos
            conexion.commit()

            # Cerrar la conexión con la base de datos
            conexion.close()

            # Mostrar una ventana emergente de éxito
            QMessageBox.information(None, "Ticket Pagado", "El Ticket ha sido pagado con éxito.")

        except Exception as e:
            # Mostrar una ventana emergente de error en caso de excepción
            QMessageBox.critical(None, "Error", f"Error al pagar el ticket: {str(e)}")




    #print(f"klk {primera}")
    #for numero in primera:
    #    suma += numero
    #print("Suma total:", suma)


checkbox_names = {
    "AnguiladiezAM": "Anguila Mañana 10:00 AM",
    "AnguilaunaPM": "Anguila Medio Día 1:00 PM",
    "AnguilaseisPM": "Anguila Medio Tarde 6:00 PM",
    "AnguilanuevePM": "Anguila Medio Noche 9:00 PM",
    "CuartetadiezAM": "La Cuarteta Mañana 10:00 AM",
    "CuartetaunaPM": "La Cuarteta Día 1:00 PM",
    "CuartetaseisPM": "La Cuarteta Tarde 6:00 PM",
    "CuartetanuevePM": "La Cuarteta Noche 9:00 PM",
    "FechaunaPM": "Tu Fecha Real 1:00 PM",
    "FloridanuevePM": "Florida Noche 9:45 PM",
    "GanadosPM": "Gana Más 2:30 PM",
    "KingdocePM": "King Lottery Quiniela 12:30 PM",
    "KingsietePM": "King Lottery 7:30 PM",
    "LeidsaochoPM": "Quiniela Leidsa 8:55 PM",
    "LotekasietePM": "Quiniela Loteka 7:55 PM",
    "NacionalochoPM": "Lotería nacional  8:50: PM",
    "NewdiezPM": "New York 10:30 PM",
    "NewdosPM": "New York 2:30 PM",
    "PrimeradocePM": "La primera 12:00 PM",
    "RealunaPM": "Quiniela Real 1:00 PM",
    "SuertedocePM": "La suerte 12:30 PM"
}
def obtener_clave_por_valor(diccionario, valor_buscado):
    for clave, valor in diccionario.items():
        if valor_buscado in valor:
            return clave
    return None


def ventanta_emergente_def(title, icon, text):
    ventana_emergente = QMessageBox()
    ventana_emergente.setWindowTitle(title)
    ventana_emergente.setText(text)
    ventana_emergente.setIcon(icon)
    ventana_emergente.exec_()


def adjustWindowToScreen(window):
    desktop = QDesktopWidget().availableGeometry()
    window.setGeometry(desktop)


class Adminwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/admin.ui", self)
        self.registrarwindow = None
        self.registrar.clicked.connect(self.registrarpage)
        self.add_number.clicked.connect(self.add_numbers)
        self.add_numbers_window = None
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

    def keyPressEvent(self, event):
            if event.key() == Qt.Key_Escape:
                self.close()
    def add_numbers(self):
        self.close()
        if self.add_numbers_window is None:
            self.add_numbers_window = Addnumbers()
        self.add_numbers_window.show()
    
    def registrarpage(self):
        self.close()
        if self.registrarwindow == None:
            self.registrarwindow = RegistrarBanca()
        self.registrarwindow.show()




def generate_salt():
    return uuid.uuid4().hex

def hash_password(password, salt):
    hashed_password = hashlib.sha256(password.encode() + salt.encode()).hexdigest()
    return hashed_password

class RegistrarBanca(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/registrobanca.ui", self)
        self.registrar_button.clicked.connect(self.register)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
    def keyPressEvent(self, event):
            if event.key() == Qt.Key_Escape:
                self.close()

    def register(self):
        nombre_banca = self.nombre_banca.text()
        cantidad_sucursales = self.cantidad.text()
        persona_a_cargo = self.persona_acargo.text()
        numero_contacto = self.numerocontacto.text()
        numero_secundario = self.numerosecundario.text()
        email_contacto = self.emailcontacto.text()
        dia_pago = self.diapago.text()
        monto_pago = self.montopago.text()
        tipo_software = self.tiposoftware.text()
        pago_puntos = self.pagopuntos.text()
        pago_pale = self.pagopale.text()
        pago_tripleta = self.pagotripleta.text()
        usuario = self.user.text()
        password = self.password.text()
        nm = nombre_banca[:1]
        id_banca = str(uuid.uuid4()) + nm
        print(id_banca)

        cursor1 = conexion.cursor()
        cursor1.execute("SELECT user FROM auth WHERE user = %s", (usuario, ))
        usuario_log = cursor1.fetchone()
        if usuario_log is not None:
            title = "Error"
            icon = QMessageBox.Critical
            text = "El nombre de usuario ya existe, por favor elige otro."
            ventanta_emergente_def(title, icon, text)
        else:
            salt = generate_salt()
            hashed_password = hash_password(password, salt)

            cursor = conexion.cursor()
            cursor.execute("INSERT INTO banca (id, idbanca, nombre_banca, persona_encargada, numerocontacto, contacto_secundario, email_contacto, dia_pago, monto_pago, software_comprado, pago_punto, pago_pale, pago_tripleta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
               (0, id_banca, nombre_banca, persona_a_cargo, numero_contacto, numero_secundario, email_contacto, dia_pago, monto_pago, tipo_software, pago_puntos, pago_pale, pago_tripleta))
            cursor2 = conexion.cursor()
            cursor2.execute("INSERT INTO auth (idauth, id_banca, user, password) VALUES (%s, %s, %s, %s)", 
                            (0, id_banca, usuario, hashed_password))
            cursor3 = conexion.cursor()
            cursor3.execute("INSERT INTO ganancias VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                            (0, id_banca, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
            conexion.commit()
            conexion.close()

            title = "Realizado"
            icon = QMessageBox.Information
            text = f"""La banca ha sido registrada con éxito. El nombre de usuario es {usuario}. 
            Las credenciales y el contrato del comprador serán enviados por correo, gracias por usar GENUINE.
            """
            ventanta_emergente_def(title, icon, text)

            # Limpiar los campos de texto
            self.nombre_banca.setText('')
            self.cantidad.setText('')
            self.persona_acargo.setText('')
            self.numerocontacto.setText('')
            self.numerosecundario.setText('')
            self.emailcontacto.setText('')
            self.diapago.setText('')
            self.montopago.setText('')
            self.tiposoftware.setText('')
            self.pagopuntos.setText('')
            self.pagopale.setText('')
            self.pagotripleta.setText('')
            self.user.setText('')
            self.password.setText('')

class Addnumbers(QMainWindow):
    def __init__(self):
        super().__init__()
        self.update_numbers = None
        uic.loadUi("UI/add_numbers.ui", self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        
        self.AnguiladiezAM.clicked.connect(lambda: self.button_clicked("anguiladiezam"))
        self.CuartetadiezAM.clicked.connect(lambda: self.button_clicked("cuartetadiezam"))
        self.PrimeradocePM.clicked.connect(lambda: self.button_clicked("primeradocepm"))
        self.KingdocePM.clicked.connect(lambda: self.button_clicked("kingdocepm"))
        self.SuertedocePM.clicked.connect(lambda: self.button_clicked("suertedocepm"))
        self.AnguilaunaPM.clicked.connect(lambda: self.button_clicked("anguilaunapm"))
        self.CuartetaunaPM.clicked.connect(lambda: self.button_clicked("cuartetaunapm"))
        self.RealunaPM.clicked.connect(lambda: self.button_clicked("realunapm"))
        self.FechaunaPM.clicked.connect(lambda: self.button_clicked("fechaunapm"))
        self.GanadosPM.clicked.connect(lambda: self.button_clicked("ganadospm"))
        self.NewdosPM.clicked.connect(lambda: self.button_clicked("newdospm"))
        self.AnguilaseisPM.clicked.connect(lambda: self.button_clicked("anguilaseispm"))
        self.CuartetaseisPM.clicked.connect(lambda: self.button_clicked("cuartetaseispm"))
        self.KingsietePM.clicked.connect(lambda: self.button_clicked("kingsietepm"))
        self.LotekasietePM.clicked.connect(lambda: self.button_clicked("lotekasietepm"))
        self.NacionalochoPM.clicked.connect(lambda: self.button_clicked("nacionalochopm"))
        self.LeidsaochoPM.clicked.connect(lambda: self.button_clicked("leidsaochopm"))
        self.AnguilanuevePM.clicked.connect(lambda: self.button_clicked("anguilanuevepm"))
        self.CuartetanuevePM.clicked.connect(lambda: self.button_clicked("cuartetanuevepm"))
        self.FloridanuevePM.clicked.connect(lambda: self.button_clicked("floridanuevepm"))
        self.NewdiezPM.clicked.connect(lambda: self.button_clicked("newdiezpm"))
    def keyPressEvent(self, event):
            if event.key() == Qt.Key_Escape:
                self.close()

    def button_clicked(self, button_name):
        self.add_numbers(button_name)

    def add_numbers(self, lottery):
        self.close()
        if self.update_numbers is None:
            self.update_numbers = UpdateNumber(lottery)
        self.update_numbers.show()


class UpdateNumber(QMainWindow):
    def __init__(self, lottery):
        super().__init__()
        uic.loadUi("UI/UPDATE_NUMBER.ui", self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.push_lotterie.clicked.connect(lambda: self.push_number(lottery))
        self.first.setFocus()
        self.add_numbers_window = None
        self.first.returnPressed.connect(self.firstfocus)
        self.second.returnPressed.connect(self.secondfocus)
        self.third.returnPressed.connect(lambda: self.push_number(lottery))
        self.loteria.setText(f"Loteria seleccionada: {lottery}")
    
    def keyPressEvent(self, event):
            if event.key() == Qt.Key_Escape:
                self.add_numbers()


    def firstfocus(self):
        self.second.setFocus()


    def secondfocus(self):
        self.third.setFocus()


    def add_numbers(self):
        self.close()
        if self.add_numbers_window is None:
            self.add_numbers_window = Addnumbers()
        self.add_numbers_window.show()



    def push_number(self, lottery):
        first = self.first.text()
        second = self.second.text()
        third = self.third.text()
        final = first + "-" + second + "-" + third
        if first == "":
            title = "ERROR"
            icon = QMessageBox.Critical
            text = "El primer premio no puede estar vacío"
            ventanta_emergente_def(title, icon, text)
            self.first.setFocus()
            print(lottery)
        elif second == "":
            title = "ERROR"
            icon = QMessageBox.Critical
            text = "El segundo premio no puede estar vacío"
            ventanta_emergente_def(title, icon, text)
            self.second.setFocus()
            print(lottery)
        elif third == "":
            title = "ERROR"
            icon = QMessageBox.Critical
            text = "El tercer premio no puede estar vacío"
            ventanta_emergente_def(title, icon, text)
            self.third.setFocus()
            print(lottery)
        else:
            print(lottery)
            print(final)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())
