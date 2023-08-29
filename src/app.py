from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QCheckBox, QDesktopWidget, QListView, QListWidgetItem, QPushButton, QApplication, QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QWidget, QFormLayout
from PyQt5.QtGui import QIcon, QPainter, QFont
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import Qt, QTimer, QDateTime
import sys
import re
import mysql.connector
from drawticket import generar_recibo
import uuid
from datetime import datetime, timedelta
import hashlib
import random
import time
from config import login, connection, register, registrar_sucursal_data
from dict import sesion_usuario
from timer import hour_rd


class LoginWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi("UI/inicio.ui", self)
            self.msj = False  # Inicializar la variable como atributo de la instancia
            self.msj_exito = False  # Inicializar la variable como atributo de la instancia
            self.Botonlogin.clicked.connect(self.login)
            self.user.returnPressed.connect(self.focus)
            self.password.returnPressed.connect(self.login)
            self.check_connection()
            # self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
            # self.setWindowTitle("LOTERIA")
            # self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
            self.bodywindow = None
            self.login_window = None
            self.admin_window = None
            self.add_numbers_window = None
            # Reemplaza con la ruta de tu archivo de icono
            icon = QIcon("NOTE3710-removebg-preview.png")
            # Agregar un ícono a la barra de navegación
            # Reemplaza con la ruta de tu archivo de icono
            icon = QIcon("./IMGS/Safeimagekit-resized-img (3).png")
            self.setWindowIcon(icon)
        except Exception as e:
            self.title = "Ha ocurrido un error"
            self.icon = QMessageBox.Information
            self.text = f"Ha ocurrido un error inesperado {e}"
            self.ventanta_emergente_def(self.title, self.icon, self.text)

    def ventanta_emergente_def(self, title, icon, text):
        self.ventana_emergente = QMessageBox()
        self.ventana_emergente.setWindowTitle(title)
        self.ventana_emergente.setText(text)
        self.ventana_emergente.setIcon(icon)
        self.ventana_emergente.show()

    def check_connection(self):
        conexion = connection()
        if conexion == True:
            pass
        else:
            self.title = "No se estableció una conexión"
            self.icon = QMessageBox.Information
            self.text = "No se pudo establecer una conexión, por favor revise su conexión a internet"
            self.ventanta_emergente_def(self.title, self.icon, self.text)
            QTimer.singleShot(999, self.close)

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
        self.check_connection()
        usuario = self.user.text()
        usuario.lower()
        password = self.password.text()

        if usuario == '' or password == '':
            title = "Error"
            icon = QMessageBox.Critical
            text = "Por favor ingrese el usuario o la contraseña."
            ventanta_emergente_def(title, icon, text)
        else:
            response_server = login(usuario, password)
            if response_server == True:
                self.close()
                if self.bodywindow is None:
                    self.bodywindow = Bodywindow()
                self.bodywindow.show()
            elif response_server == "admin":
                self.close()
                if self.admin_window == None:
                    self.admin_window = Adminwindow()
                self.admin_window.show()
            elif response_server == False:
                title = "Error"
                icon = QMessageBox.Critical
                text = "Usuario o contraseña incorrectos."
                ventanta_emergente_def(title, icon, text)
            elif response_server == None:
                title = "Error"
                icon = QMessageBox.Critical
                text = "La información no existe."
                ventanta_emergente_def(title, icon, text)
            elif response_server == "error":
                title = "Error"
                icon = QMessageBox.Critical
                text = "Error al contactar la Api"
                ventanta_emergente_def(title, icon, text)


class Bodywindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.check_connection()
        self.selected_lotteries = 0
        uic.loadUi("UI/body.ui", self)
        # este es el area de los botones con self.conexiones a funciones. ---------------------------------
        self.siguiente.clicked.connect(self.calculate)
        self.msj = False  # Inicializar la variable como atributo de la instancia
        # Conectar la tecla Enter en el campo "monto" al método "calculate"
        self.amount.returnPressed.connect(self.calculate)
        self.numero.returnPressed.connect(self.calculate)
        self.lista_jugadas.itemClicked.connect(self.delete_item)
        self.time_now.setText(datetime.now().strftime("%H:%M:%S"))
        # Configurar el temporizador para actualizar la hora cada segundo (1000 ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_hora)
        self.timer.start(1000)  # 1000 ms = 1 segundo
        self.total_una_loteria.setText('0.00')
        self.total_jugado.setText('0.00')
        self.ESC.clicked.connect(self.cerrar)
        self.F1.clicked.connect(self.reiniciar)
        self.F2.clicked.connect(self.limpiar_lot)
        self.F3.clicked.connect(self.emergency)
        self.F4.clicked.connect(self.devolucion)
        self.F5.clicked.connect(self.restart)
        self.F6.clicked.connect(self.copy)
        self.F7.clicked.connect(self.cobrar)
        # self.F8.clicked.connect(self)
        self.F9.clicked.connect(self.bloqueados)
        self.F10.clicked.connect(self.imprimir_ticket)
        self.F11.clicked.connect(self.limpiar)
        self.F11_2.clicked.connect(self.limpiar)
        self.numero.setValidator(QtGui.QIntValidator())
        self.amount.setValidator(QtGui.QIntValidator())
        id_banca = sesion_usuario.get('id_banca')
        nombre_banca = sesion_usuario.get('nombre_banca')
        self.id_banca = sesion_usuario.get('id_banca')
        self.id_sucursal = sesion_usuario.get('id_sucursal')
        # Fin. ---------------------------------
        self.adjustToScreen()
        self.setWindowTitle(nombre_banca)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.login_window = None
        self.body_window = None
        self.cobrar_ticket = None
        # Reemplaza "your_list_view" con el nombre de objeto del QListView en Qt Designer
        self.list_view = self.findChild(QListView, "lista_de_jugadas")
        for name in checkbox_names:
            checkbox = self.findChild(QCheckBox, name)
            if checkbox:
                checkbox.stateChanged.connect(self.checkbox_state_changed)


    def check_connection(self):
        conexion = connection()
        if conexion == True:
            pass
        else:
            self.hide()
            self.title = "No se estableció una conexión"
            self.icon = QMessageBox.Information
            self.text = "No se pudo establecer una conexión, por favor revise su conexión a internet"
            self.ventanta_emergente_def(self.title, self.icon, self.text)
            QTimer.singleShot(333, self.close)


                

    def emergency(self):
        title = "INFORMACION"
        icon = QMessageBox.Information
        text = f"Número de teléfono: {sesion_usuario['numero_principal']} debido a cualquier emergencia no dudes en contactar."
        ventanta_emergente_def(title, icon, text)

    def reiniciar(self):
        self.close()
        if self.login_window is None:
            self.login_window = LoginWindow()
        self.login_window.show()

    def limpiar_lot(self):
        checkboxes = self.findChildren(QCheckBox)
        for checkbox in checkboxes:
            checkbox.setChecked(False)

    def devolucion(self):
        self.devolucion_window = None
        if self.devolucion_window is None:
            self.devolucion_window = DevolucionWindow()
        self.devolucion_window.show()

    def restart(self):
        self.close()
        if self.body_window is None:
            self.body_window = Bodywindow()
        self.body_window.show()

    def cobrar(self):
        if self.cobrar_ticket is None:
            self.cobrar_ticket = CobrarTicketWindow()
        self.cobrar_ticket.show()

    def bloqueados(self):
        self.block_numbers = None
        if self.block_numbers is None:
            self.block_numbers = BlockNumbers()
        self.block_numbers.show()

    def actualizar_hora(self):
        # Obtener la hora actual
        hora_actual = QDateTime.currentDateTime().toString('HH:mm:ss')

        # Actualizar la etiqueta con la hora actual
        self.time_now.setText(hora_actual)

    def calculate(self):
        numero = self.numero.text()
        monto = self.amount.text()

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
                    jugada_total = item_primero + \
                        '-' + item_segundo + " (Palé)"
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
                        numero_for_replace = totaljugado.replace(',', '')
                        totalhoy = float(numero_for_replace)
                    else:
                        totalhoy = 0
                    if totalhoy <= 0:
                        if self.selected_lotteries <= 0:
                            self.total_jugado.setText(str('0.00'))
                        else:
                            totaltoday = float(monto) * \
                                float(self.selected_lotteries)
                            numero_formateado = "{:,.2f}".format(totaltoday)
                            self.total_jugado.setText(str(numero_formateado))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = float(
                                monto) * float(self.selected_lotteries) + float(totalhoy)
                            numero_formateado = "{:,.2f}".format(totaltoday)
                            self.total_jugado.setText(str(numero_formateado))
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
                    number_for_process = float(monto)
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
                        number_for_replace = totaljugado.replace(',', '')
                        totalhoy = float(number_for_replace)
                    else:
                        totalhoy = 0
                    if totalhoy <= 0:
                        if self.selected_lotteries <= 0:
                            self.total_jugado.setText(str('0.00'))
                        else:
                            totaltoday = float(monto) * \
                                float(self.selected_lotteries)
                            numero_formateado = "{:,.2f}".format(totaltoday)
                            self.total_jugado.setText(str(numero_formateado))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = float(
                                monto) * float(self.selected_lotteries) + float(totalhoy)
                            numero_formateado = "{:,.2f}".format(totaltoday)
                            self.total_jugado.setText(str(numero_formateado))
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
                    number_for_process = float(monto)
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
                        totalhoy = float(totaljugado)
                    else:
                        totalhoy = 0
                    if totalhoy <= 0:
                        if self.selected_lotteries <= 0:
                            self.total_jugado.setText(str('0.00'))
                        else:
                            totaltoday = float(monto) * \
                                float(self.selected_lotteries)
                            numero_formateado = "{:,.2f}".format(totaltoday)
                            self.total_jugado.setText(str(numero_formateado))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = float(
                                monto) * float(self.selected_lotteries) + float(totalhoy)
                            numero_formateado = "{:,.2f}".format(totaltoday)
                            self.total_jugado.setText(str(numero_formateado))

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
                    jugada_final = primera_parte + "-" + segunda_parte + \
                        "-" + tercera_parte + " (Tripleta)"
                    number_for_process = float(monto)
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
                            self.total_jugado.setText(str('0.00'))
                        else:
                            totaltoday = float(monto) * \
                                float(self.selected_lotteries)
                            numero_formateado = "{:,.2f}".format(totaltoday)
                            self.total_jugado.setText(str(numero_formateado))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = float(
                                monto) * float(self.selected_lotteries) + float(totalhoy)
                            numero_formateado = "{:,.2f}".format(totaltoday)
                            self.total_jugado.setText(str(numero_formateado))
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
                    number_for_process = float(monto)
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
                            self.total_jugado.setText(str('0.00'))
                        else:
                            totaltoday = float(monto) * \
                                float(self.selected_lotteries)
                            numero_formateado = "{:,.2f}".format(totaltoday)
                            self.total_jugado.setText(str(numero_formateado))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = float(
                                monto) * float(self.selected_lotteries) + float(totalhoy)
                            numero_formateado = "{:,.2f}".format(totaltoday)
                            self.total_jugado.setText(str(numero_formateado))
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
                    number_for_process = float(monto)
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
                        total_hoy = totaljugado.replace(',', '')
                        totalhoy = float(total_hoy)
                    else:
                        totalhoy = 0
                    if totalhoy <= 0:
                        if self.selected_lotteries <= 0:
                            self.total_jugado.setText(str('0.00'))
                        else:
                            totaltoday = float(monto) * \
                                float(self.selected_lotteries)
                            numero_formateado = "{:,.2f}".format(totaltoday)
                            self.total_jugado.setText(str(numero_formateado))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = float(
                                monto) * float(self.selected_lotteries) + float(totalhoy)
                            numero_formateado = "{:,.2f}".format(totaltoday)
                            self.total_jugado.setText(str(numero_formateado))
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
                    number_for_process = float(monto)
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
                        resultado = totaljugado.replace(',', '')
                        totalhoy = float(resultado)
                    else:
                        totalhoy = 0
                    if totalhoy <= 0:
                        if self.selected_lotteries <= 0:
                            self.total_jugado.setText(str('0.00'))
                        else:
                            totaltoday = float(monto) * \
                                float(self.selected_lotteries)
                            numero_formateado = "{:,.2f}".format(totaltoday)
                            self.total_jugado.setText(str(numero_formateado))
                    else:
                        if self.selected_lotteries <= 0:
                            pass
                        else:
                            totaltoday = float(
                                monto) * float(self.selected_lotteries) + float(totalhoy)
                            numero_formateado = "{:,.2f}".format(totaltoday)
                            self.total_jugado.setText(str(numero_formateado))
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
        self.total_una_loteria.setText('0.00')
        self.total_jugado.setText('0.00')

    def checkbox_state_changed(self, state):
        checkbox = self.sender()
        if state == QtCore.Qt.Checked:
            self.selected_lotteries += 1
            total = 0
            for i in range(self.lista_montos.count()):
                item = self.lista_montos.item(i)
                texto = item.text()
                texto_replace = texto.replace(',', '')
                numero = float(texto_replace)
                total += numero

            total_jugado = self.total_jugado.text()
            if total_jugado:
                texto_replace = total_jugado.replace(',', '')
                numero = float(texto_replace)
                jugado = float(numero)
                total_jugado1 = total * self.selected_lotteries
            else:
                jugado = 0
                total_jugado1 = total * self.selected_lotteries
            numero_formateado = "{:,.2f}".format(total_jugado1)
            self.total_jugado.setText(str(numero_formateado))

            # Imprimir nombre del checkbox seleccionado
            checkbox_name = checkbox.text()
            print(checkbox_name)
            item = QListWidgetItem(checkbox_name)
            self.selected_lotteries_list.addItem(item)
            checkbox_selected_names.append(checkbox_name)
            # Verificar si el valor del checkbox seleccionado existe en el diccionario y obtener su clave
            clave_del_checkbox = obtener_clave_por_valor(
                checkbox_names, checkbox_name)
            checkbox_selected_lotteries.append(clave_del_checkbox)
            # Imprimir la clave del checkbox seleccionado
        else:
            checkbox_name = checkbox.text()
            clave_del_checkbox = obtener_clave_por_valor(
                checkbox_names, checkbox_name)
            for i, name in enumerate(checkbox_selected_lotteries):
                item = name
                if item == clave_del_checkbox:
                    row_index = i
                    self.selected_lotteries_list.takeItem(row_index)
            self.selected_lotteries -= 1
            checkbox_selected_names.remove(checkbox_name)
            checkbox_selected_lotteries.remove(clave_del_checkbox)
            total = 0

            for i in range(self.lista_montos.count()):
                item = self.lista_montos.item(i)
                texto = item.text()
                texto_replace = texto.replace(',', '')
                numero = float(texto_replace)
                total += numero

            total_jugado = self.total_jugado.text()
            if total_jugado:
                number_for_replce = total_jugado.replace(',', '')
                jugado = float(number_for_replce)
                total_jugado1 = total * self.selected_lotteries
            else:
                jugado = 0
                total_jugado1 = total * self.selected_lotteries

            numero_formateado = "{:,.2f}".format(total_jugado1)
            self.total_jugado.setText(str(numero_formateado))

            # Imprimir nombre del checkbox seleccionado
            checkbox_name = checkbox.text()

    def check_balance(self, monto):
        total_una_loteria = self.total_una_loteria.text()
        if total_una_loteria == '':
            number_for_process = float(monto)
            numero_formateado = "{:,.2f}".format(number_for_process)
            self.total_una_loteria.setText(str(numero_formateado))
        else:
            monto_replace = monto.replace(',', '')
            monto_to_page = self.total_una_loteria.text()
            monto_to_page_replace = monto_to_page.replace(',', '')
            total_loteria = float(monto_to_page_replace) + float(monto_replace)
            number_for_process = total_loteria
            numero_formateado = "{:,.2f}".format(number_for_process)
            self.total_una_loteria.setText(str(numero_formateado))

    def adjustToScreen(self):
        desktop = QDesktopWidget().availableGeometry()
        self.setGeometry(desktop)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_Shift:
            self.amount.setFocus()
        if event.key() == Qt.Key_F1:
            self.reiniciar()
        if event.key() == Qt.Key_F2:
            self.limpiar_lot()
        if event.key() == Qt.Key_F3:
            self.emergency
        if event.key() == Qt.Key_F4:
            self.devolucion()
        if event.key() == Qt.Key_F5:
            self.restart()
        if event.key() == Qt.Key_F6:
            self.copy()
        if event.key() == Qt.Key_F7:
            self.cobrar()
        if event.key() == Qt.Key_F11:
            self.lista_jugadas.clear()
            self.lista_montos.clear()
            self.total_una_loteria.setText('0.00')
            self.total_jugado.setText('0.00')
        if event.key() == Qt.Key_F9:
            self.bloqueados()
        if event.key() == Qt.Key_F10:
            self.imprimir_ticket()
        if event.key() == Qt.Key_F12:

            #Adriel lo va hacer.
            cursor = self.conexion.cursor()
            cursor.execute("SELECT numeros FROM jugadas WHERE id_banca = %s AND id_sucursal = %s",
                           (self.id_banca, self.id_sucursal))
            jugadas = cursor.fetchall()

            numbers_count = {}  # Diccionario para contar las ocurrencias de cada número
            print(jugadas)
            if jugadas != []:
                for i in range(len(jugadas)):
                    for_work = jugadas[i][0]
                    for_work1 = for_work.replace('-', '')
                    if for_work1 in numbers_count:
                        numbers_count[for_work1] += 1
                    else:
                        numbers_count[for_work1] = 1
                most_common_number = max(numbers_count, key=numbers_count.get)
                most_common_count = numbers_count[most_common_number]
                if most_common_count > 75:
                    title = "Informacion"
                    icon = QMessageBox.Information
                    text = f"El número peligrando del día es: {most_common_number}: con {most_common_count} jugadas"
                    ventanta_emergente_def(title, icon, text)
                else:
                    title = "Informacion"
                    icon = QMessageBox.Information
                    text = "Por el momento no hay jugadas peligrosas."
                    ventanta_emergente_def(title, icon, text)
            else:
                title = "Informacion"
                icon = QMessageBox.Information
                text = "Por el momento no hay jugadas peligrosas."
                ventanta_emergente_def(title, icon, text)

    # falta todvia agregarle lo de los numeros, falta todavia integrarle el conteo, todavia hay que pasarlo a imprimir. (pendiente)

    def imprimir_ticket(self):

        #Adriel lo va hacer
        nombre_banca = sesion_usuario.get('nombre_banca')
        id_banca = sesion_usuario.get('id_banca')
        id_sucursal = sesion_usuario.get('id_sucursal')
        cursor = self.conexion.cursor()
        cursor.execute(
            "SELECT * FROM bloqueado WHERE id_banca = %s and id_sucursal = %s", (id_banca, id_sucursal))
        bloqueado = cursor.fetchall()
        cursor.close()
        cursor2 = self.conexion.cursor()
        cursor3 = self.conexion.cursor()
        list_numbers = []
        condition = False
        z = 0
        cantidad_permitida = 0
        resultado = 0
        randomss = str(random.randint(000000000000, 999999999999))
        # Rellena con ceros a la izquierda hasta completar 12 dígitos
        randoms = f"{randomss:012}"
        # numero_bloqueado_analicts = numero_bloqueado[2]
        if len(self.lista_montos) > 0:
            for i in range(self.lista_montos.count()):
                items = self.lista_jugadas.item(i)
                jugadas_texto = items.text()
                resultado = re.sub(r'[^\d-]', '', jugadas_texto)
            cursor2.execute("SELECT * FROM jugadas WHERE id_banca = %s and id_sucursal = %s and numeros = %s",
                            (id_banca, id_sucursal, resultado))
            resultado2 = cursor2.fetchall()
            cursor2.close()
            cursor3.execute("SELECT * FROM restringido WHERE id_banca = %s and id_sucursal = %s and numero = %s",
                            (id_banca, id_sucursal, resultado))
            restringido = cursor3.fetchall()
            for x in range(len(bloqueado)):
                list_numbers.append(bloqueado[x][2])
            if restringido != []:
                for z in range(len(resultado2)):
                    hoy = datetime.now()
                    dia = int(hoy.strftime("%d"))
                    fecha_database = (resultado2[z][6])
                    fecha_data = int(fecha_database[:2])
                z += 1
                condition = True
                for n in range(len(restringido)):
                    cantidad_permitida = int(restringido[n][3])
                    fecha = int(restringido[n][4])
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
        elif condition == True and z >= cantidad_permitida:
            if z >= cantidad_permitida and dia <= fecha:
                title = "Error"
                icon = QMessageBox.Critical
                text = f"Esta jugada no está disponible debido a que se agotó la disponibilidad de los números. error(101)"
                ventanta_emergente_def(title, icon, text)
        elif resultado in list_numbers:
            title = "Error"
            icon = QMessageBox.Critical
            text = f"La jugada no pudo ser realizada debido que el numero {resultado} no está disponible para ventas."
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
            total_precio1 = (self.total_jugado.text())
            total_precio_convert = total_precio1.replace(',', '')
            total_precio = float(total_precio_convert)
            day = today.day

            for i in range(self.lista_montos.count()):
                item = self.lista_montos.item(i)
                amount = item.text()
                items = self.lista_jugadas.item(i)
                chosen_number = items.text()
                added_elements = i + 1
                chosen_numbers.append(str(chosen_number))
                amounts.append(str(amount))

            # Obtener la hora actual
            hora_actual = datetime.now()

            # Iterar por las loterías seleccionadas
            for checkbox_name in checkbox_selected_names:
                lotteries_for_database = checkbox_name
                if lotteries_for_database in checkbox_times:
                    hora_checkbox_str = checkbox_times[lotteries_for_database]

                    # Convertir la hora del diccionario a objeto datetime (con formato de 12 horas)
                    hora_checkbox = datetime.strptime(
                        hora_checkbox_str, "%I:%M %p")

                    # Ajustar la fecha del objeto hora_checkbox con la fecha actual para comparar solo las horas
                    hora_checkbox = hora_checkbox.replace(
                        year=hora_actual.year, month=hora_actual.month, day=hora_actual.day)

                    # Verificar si ya no hay tiempo suficiente (la diferencia es menor o negativa)
                    diferencia_tiempo = hora_checkbox - hora_actual
                    if diferencia_tiempo <= timedelta(minutes=0):
                        title = "ERROR"
                        icon = QMessageBox.Critical
                        text = f"¡Lotería cerrada!: {lotteries_for_database}"
                        ventanta_emergente_def(title, icon, text)
                        return
                    elif diferencia_tiempo <= timedelta(minutes=10):
                        title = "ERROR"
                        icon = QMessageBox.Critical
                        text = f"¡Lotería cerrada!: {lotteries_for_database}"
                        ventanta_emergente_def(title, icon, text)
                        return
                    else:
                        pass

            for checkbox_name_loterries in checkbox_selected_lotteries:

                for i in range(len(chosen_numbers)):
                    item_for_database = self.lista_jugadas.item(i)
                    item_for_database_text = item_for_database.text()
                    amount_for_database = self.lista_montos.item(i)
                    amount_for_database_text = amount_for_database.text()
                    numeros_con_signo = re.sub(
                        r"[^\d-]", "", item_for_database_text)

                    cursor = self.conexion.cursor()
                    cursor.execute("INSERT INTO jugadas VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                   (id_banca, id_sucursal, idticket, numeros_con_signo, amount_for_database_text, lotteries_for_database, datetime.now().strftime('%d/%m/%Y - %I:%M:%S %p'), "NO", checkbox_name_loterries, day, randoms))
                    cursor.close()
                    cursor2 = self.conexion.cursor()
                    cursor2.execute("UPDATE ganancias SET numeros_vendidos = numeros_vendidos + 1, venta_diaria = venta_diaria + %s, venta_total = venta_total + %s WHERE id_banca = %s and id_sucursal = %s",
                                    (amount_for_database_text, amount_for_database_text, id_banca, id_sucursal))
                    cursor2.close()
                    self.conexion.commit()

            generar_recibo(nombre_banca, added_elements, chosen_numbers, amounts,
                           total_precio, archivo_pdf_azar, idticket, checkbox_selected_names, randoms)
            self.limpiar_ventana()

    def limpiar_ventana(self):
        checkboxes = self.findChildren(QCheckBox)

        # Deseleccionar todos los checkboxes encontrados
        for checkbox in checkboxes:
            checkbox.setChecked(False)
        self.total_jugado.setText('0.00')
        self.total_una_loteria.setText('0.00')
        self.lista_montos.clear()
        self.lista_jugadas.clear()

    def delete_item(self, item):
        reply = QMessageBox.question(
            self, "Eliminar número", "¿Estás seguro de que deseas eliminar este número?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            selected_items = self.lista_jugadas.selectedItems()
            for item in selected_items:
                row = self.lista_jugadas.row(item)
                monto_item = self.lista_montos.takeItem(row)
                self.lista_jugadas.takeItem(row)

                monto = float(monto_item.text().replace(',', ''))
                resultado_actual = float(
                    self.total_jugado.text().replace(',', ''))
                resultado_actual -= monto
                resultado_jugadas = float(
                    self.total_una_loteria.text().replace(',', ''))
                resultado_jugadas -= monto
                numero_formateado = "{:,.2f}".format(resultado_jugadas)
                self.total_una_loteria.setText(str(numero_formateado))
                total_una = float(
                    self.total_una_loteria.text().replace(',', ''))
                for i in range(len(checkbox_selected_lotteries) + 1):
                    total_calculate = total_una * i
                if resultado_actual >= 0:
                    numero_formateado = "{:,.2f}".format(total_calculate)
                    self.total_jugado.setText(str(numero_formateado))
        # Ejemplo de uso

    def copy(self):
        intentado = True
        id_banca = id_banca = sesion_usuario['id_banca']
        id_sucursal = sesion_usuario["id_sucursal"]
        while True:
            respuesta_usuario, resultado_dialogo = ventana_emergente_con_input(
                "Copiar Ticket", "dialog-question", "Por favor ingresa el ID del ticket que deseas copiar."
            )
            if resultado_dialogo == QDialog.Accepted:
                # Aquí deberías realizar la lógica para copiar el ticket utilizando respuesta_usuario (el ID del ticket ingresado)
                cursor = self.conexion.cursor()
                cursor.execute("SELECT * FROM jugadas WHERE id_ticket = %s and id_sucursal = %s and id_banca = %s",
                               (respuesta_usuario, id_sucursal, id_banca))
                id_ticket = cursor.fetchall()
                if id_ticket != []:
                    for i in range(len(id_ticket)):
                        jugada = (id_ticket[i][3])
                        monto = (id_ticket[i][4])
                        if len(jugada) == 2:
                            item_text = f"{jugada} (Quiniela)"
                            item_text1 = f"{monto}"
                            item = QListWidgetItem(item_text)
                            item1 = QListWidgetItem(item_text1)
                            self.lista_montos.addItem(item1)
                            self.lista_jugadas.addItem(item)
                            self.check_balance(monto)
                        elif len(jugada) == 5:
                            item_text = f"{jugada} (Palé)"
                            item_text1 = f"{monto}"
                            item = QListWidgetItem(item_text)
                            item1 = QListWidgetItem(item_text1)
                            self.lista_montos.addItem(item1)
                            self.lista_jugadas.addItem(item)
                            self.check_balance(monto)
                        elif len(jugada) == 8:
                            item_text = f"{jugada} (Tripleta)"
                            item_text1 = f"{monto}"
                            item = QListWidgetItem(item_text)
                            item1 = QListWidgetItem(item_text1)
                            self.lista_montos.addItem(item1)
                            self.lista_jugadas.addItem(item)
                            self.check_balance(monto)
                    break
                else:
                    if intentado:
                        title = "ERROR"
                        icon = QMessageBox.Critical
                        text = f"el ticket con el id: {respuesta_usuario} es invalido".upper(
                        )
                        ventanta_emergente_def(title, icon, text)
            else:
                break


def ventana_emergente_con_input(title, icon, text):
    # Creamos una ventana emergente personalizada (QDialog)
    ventana_emergente = QDialog()
    ventana_emergente.setWindowTitle(title)
    # Convertimos el icono a QIcon
    ventana_emergente.setWindowIcon(QIcon.fromTheme(icon))

    # Establecemos un ancho mínimo para la ventana
    ventana_emergente.setMinimumWidth(300)

    # Creamos un layout de formulario para organizar los elementos
    layout = QFormLayout(ventana_emergente)

    # Agregamos una etiqueta con el texto deseado
    etiqueta = QLabel(text)
    layout.addRow(etiqueta)

    # Creamos un campo de entrada de texto (QLineEdit) y lo configuramos
    input_box = QLineEdit()
    # Texto de ayuda para el usuario
    input_box.setPlaceholderText("Ingresa el ID del ticket")
    layout.addRow("ID del ticket:", input_box)

    # Creamos un botón de aceptar
    boton_aceptar = QPushButton("Aceptar")
    layout.addRow(boton_aceptar)

    # Conectamos el botón "Aceptar" a la función que cierra la ventana y devuelve la respuesta
    boton_aceptar.clicked.connect(ventana_emergente.accept)

    # Ejecutamos la ventana y esperamos la respuesta del usuario
    resultado = ventana_emergente.exec_()

    # Obtenemos el texto ingresado por el usuario
    respuesta = input_box.text()

    # Devolvemos la respuesta del usuario y el resultado del cuadro de diálogo (Aceptar o Cancelar)
    return respuesta, resultado


checkbox_selected_names = []
checkbox_selected_lotteries = []
primer = []
ganadores = []
montos = []


class CobrarTicketWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/cobrarticket.ui", self)
        self.check_connection()
        self.verificar_id.clicked.connect(self.verificar_ticket)
        self.id_ticket.returnPressed.connect(self.verificar_ticket)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

    def check_connection(self):
        conexion = connection()
        if conexion == True:
            pass
        else:
            self.hide()
            self.title = "No se estableció una conexión"
            self.icon = QMessageBox.Information
            self.text = "No se pudo establecer una conexión, por favor revise su conexión a internet"
            self.ventanta_emergente_def(self.title, self.icon, self.text)
            QTimer.singleShot(333, self.close)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
            primer.clear()

    def verificar_ticket(self):
        if self.id_ticket.text() == '':
            title = "Error"
            icon = QMessageBox.Critical
            text = "Por favor introduce el ID del ticket."
            self.id_ticket.setText('')
            self.id_ticket.setFocus()
            ventanta_emergente_def(title, icon, text)
        else:
            pago_punto = sesion_usuario.get('pago_punto')
            pago_pale = sesion_usuario.get('pago_pale')
            pago_tripleta = sesion_usuario.get('pago_tripleta')
            puntos_primera = sesion_usuario.get('puntos_primera')
            puntos_segunda = sesion_usuario.get('puntos_segunda')
            puntos_tercera = sesion_usuario.get('puntos_tercera')
            id_banca = sesion_usuario['id_banca']
            id_sucursal = sesion_usuario['id_sucursal']
            id_ticket = self.id_ticket.text()
            self.id_ticket.setText("")
            cursor2 = self.conexion.cursor()
            cursor2.execute("SELECT * FROM jugadas WHERE id_ticket = %s and id_banca = %s and id_sucursal = %s",
                            (id_ticket, id_banca, id_sucursal))
            ticket = cursor2.fetchall()
            cursor2.close()
            if ticket == []:
                title = "Error"
                icon = QMessageBox.Critical
                text = "Ticket no encontrado, asegurate de ingresar correctamente los datos."
                ventanta_emergente_def(title, icon, text)

            elif ticket is not None:
                for i in range(len(ticket)):
                    numero = ticket[i][3]
                    monto = ticket[i][4]
                    loteria = ticket[i][5]
                    fecha = ticket[i][6]
                    cobrado = ticket[i][7]
                    key_loteria = ticket[i][8].lower()
                    fecha_for_verifying = fecha[:10]

                    cursor2 = self.conexion2.cursor()
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
                        patron = ''.join(
                            f"(?=.*{digito})" for digito in numero)
                        query = f"SELECT * FROM {key_loteria} WHERE resultados REGEXP %s AND fecha = %s"
                        cursor2.execute(query, (patron, fecha_for_verifying))
                        ganador = cursor2.fetchone()
                        if ganador is not None:
                            numeros_a_buscar = numero.split('-')
                            for x in numeros_a_buscar:
                                pass
                            if x in ganador[1]:
                                if len(numero) == 2:
                                    if numero in ganador[1][:2]:
                                        monto_replace = monto.replace(',', '')
                                        primera = float(
                                            monto_replace) * float(puntos_primera)
                                        primer.append(primera)
                                        ganadores.append(numero)
                                        montos.append(monto)
                                    elif numero in ganador[1][2:5]:
                                        monto_replace = monto.replace(',', '')
                                        segunda = float(
                                            monto_replace) * float(puntos_segunda)
                                        primer.append(segunda)
                                        ganadores.append(numero)
                                        montos.append(monto)
                                    else:
                                        monto_replace = monto.replace(',', '')
                                        tercera = float(
                                            monto_replace) * float(puntos_tercera)
                                        primer.append(tercera)
                                        ganadores.append(numero)
                                        montos.append(monto)
                                elif len(numero) == 5:
                                    monto_replace = monto.replace(',', '')
                                    tercera = float(
                                        monto_replace) * float(pago_pale)
                                    primer.append(tercera)
                                    ganadores.append(numero)
                                    montos.append(monto)
                                elif len(numero) == 8:
                                    monto_replace = monto.replace(',', '')
                                    primera = float(
                                        monto_replace) * float(pago_tripleta)
                                    primer.append(primera)
                                    ganadores.append(numero)
                                    montos.append((monto))
                            else:
                                pass
                        else:
                            pass
                self.monto_pagar(primer, id_ticket)
            elif ticket == "":
                title = "Error"
                icon = QMessageBox.Critical
                text = "Ticket no encontrado, asegurate de ingresar correctamente los datos."
                ventanta_emergente_def(title, icon, text,)


def monto_pagar(primer, id_ticket, self):
    id_sucursal = sesion_usuario.get('id_sucursal')
    id_banca = sesion_usuario.get('id_banca')

    if primer:
        suma = sum(primer)  # Sumar los montos en la lista
        title = "Felicidades"
        icon = QMessageBox.Information
        text = f"Ticket Ganador, pague la cantidad de {suma}"

        ventana_emergente = QMessageBox()
        ventana_emergente.setWindowTitle(title)
        ventana_emergente.setText(text)
        ventana_emergente.setIcon(icon)
        # Crear un botón personalizado y agregarlo a la ventana emergente
        boton_pagar = QPushButton("Pagar")
        ventana_emergente.addButton(boton_pagar, QMessageBox.YesRole)

        # Agregar el botón "Cancelar" y establecerlo como el botón por defecto
        boton_cancelar = ventana_emergente.addButton(
            "Cancelar", QMessageBox.NoRole)
        ventana_emergente.setDefaultButton(boton_cancelar)

        # Mostrar la ventana emergente y esperar a que el usuario interactúe con ella
        resultado = ventana_emergente.exec_()

        # Comprobar si el botón "Pagar" fue presionado
        if ventana_emergente.clickedButton() == boton_pagar:
            try:
                cursor = self.conexion.cursor()

                # Utilizamos la sentencia DELETE para eliminar las jugadas con el ID de ticket y números en 'ganadores'
                for numero in ganadores:
                    sentencia_sql = "DELETE FROM jugadas WHERE id_ticket = %s and numeros = %s and id_sucursal = %s"
                    # Convertir 'numero' a entero
                    valores = (id_ticket, numero, id_sucursal)

                    # Ejecutamos la sentencia SQL
                    cursor.execute(sentencia_sql, valores)

                # Confirmar los cambios en la base de datos
                self.conexion.commit()

                # Cerrar el cursor y la conexión con la base de datos
                cursor.close()
                for (i) in range(len(ganadores) - 1):
                    ganador = ganadores[i]
                    monto_jugado = montos[i]
                    monto_ganado = primer[i]
                    cursor2 = self.conexion.cursor()
                    cursor2.execute("INSERT INTO tickets_ganadores VALUES (%s, %s, %s, %s, %s, %s)", ((
                        id_banca, id_sucursal, id_ticket, ganador, monto_ganado, monto_jugado)))
                    self.conexion.commit()
                    cursor2.close()

                # Mostrar una ventana emergente de éxito
                QMessageBox.information(
                    None, "Ticket Pagado", "El Ticket ha sido pagado con éxito.")
                primer.clear()
            except Exception as e:
                # Mostrar una ventana emergente de error en caso de excepción
                QMessageBox.critical(
                    None, "Error", f"Error al pagar el ticket: {str(e)}")
                primer.clear()
    else:
        title = "Error"
        icon = QMessageBox.Critical
        text = "Ticket no ganador."
        ventanta_emergente_def(title, icon, text)
        primer.clear()


checkbox_names = {
    "AnguiladiezAM": "Anguila Mañana 10:00 AM",
    "AnguilaunaPM": "Anguila Medio Día 1:00 PM",
    "AnguilaseisPM": "Anguila Medio Tarde 6:00 PM",
    "AnguilanuevePM": "Anguila Medio Noche 9:00 PM",
    "CuartetadiezAM": "La Cuarteta Mañana 10:00 AM",
    "CuartetaunaPM": "La Cuarteta Día 1:00 PM",
    "CuartetaseisPM": "La Cuarteta Tarde 6:00 PM",
    "CuartetanuevePM": "La Cuarteta Noche 9:00 PM",
    "FloridanuevePM": "Florida Noche 9:45 PM",
    "FloridadosPM": "Florida Día 2:30 PM",
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

checkbox_times = {
    "Anguila Mañana 10:00 AM": "10:00 AM",
    "Anguila Medio Día 1:00 PM": "1:00 PM",
    "Anguila Medio Tarde 6:00 PM": "6:00 PM",
    "Anguila Medio Noche 9:00 PM": "9:00 PM",
    "La Cuarteta Mañana 10:00 AM": "10:00 AM",
    "La Cuarteta Día 1:00 PM": "1:00 PM",
    "La Cuarteta Tarde 6:00 PM": "6:00 PM",
    "La Cuarteta Noche 9:00 PM": "9:00 PM",
    "Florida Noche 9:45 PM": "9:45 PM",
    "Florida Día 2:30 PM": "2:30 PM",
    "Gana Más 2:30 PM": "2:30 PM",
    "King Lottery Quiniela 12:30 PM": "12:30 PM",
    "King Lottery 7:30 PM": "7:30 PM",
    "Quiniela Leidsa 8:55 PM": "8:55 PM",
    "Quiniela Loteka 7:55 PM": "7:55 PM",
    "Lotería nacional 8:50 PM": "8:50 PM",
    "New York 10:30 PM": "10:30 PM",
    "New York 2:30 PM": "2:30 PM",
    "La primera 12:00 PM": "12:00 PM",
    "Quiniela Real 1:00 PM": "1:00 PM",
    "La suerte 12:30 PM": "12:30 PM"
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
        self.check_connection()
        self.registrarwindow = None
        self.msj = False
        self.registrar.clicked.connect(self.registrarpage)
        self.add_number.clicked.connect(self.add_numbers)
        self.eliminar_banca.clicked.connect(self.desactivar_banca)
        self.registrar_sucursal.clicked.connect(self.registrar_sucursal_banca)
        self.mantenimiento_button.clicked.connect(self.mantenimiento)
        self.eliminar_base_datos_button.clicked.connect(
            self.eliminar_base_datos)
        self.add_numbers_window = None
        self.desactivar_window = None
        self.mantain_window = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar)
        self.timer.start(1000)  # 1000 ms = 1 segundo
        self.id_banca = sesion_usuario.get("id_banca")
        self.id_sucursal = sesion_usuario.get("id_sucursal")
        self.correos_adeudos = []
        self.nombres_to_send = []

    def check_connection(self):
        conexion = connection()
        if conexion == True:
            pass
        else:
            self.hide()
            self.title = "No se estableció una conexión"
            self.icon = QMessageBox.Information
            self.text = "No se pudo establecer una conexión, por favor revise su conexión a internet"
            self.ventanta_emergente_def(self.title, self.icon, self.text)
            QTimer.singleShot(333, self.close)

    def recordatorio_pagos(self):

        #cursor = self.conexion.cursor()
#
        #cursor.execute("SELECT * FROM informacion_banca")
#
        #bancas = cursor.fetchall()

        #hoy = today.day
#
        #for i in range(len(bancas)):
#
        #    dia_pago = bancas[i][6]
#
        #    if int(hoy) == int(dia_pago):
#
        #        correo = bancas[i][4]
        #        nombre = bancas[i][2]
#
        #        self.correos_adeudos.append(correo)
        #        self.nombres_to_send.append(nombre)

        self.send_mail_adeudo()

    def send_mail_adeudo(self):
        for i, correo in enumerate(self.correos_adeudos):
            nombre = self.nombres_to_send[i]
            enviar_correo_adeudo(correo, nombre)

    def eliminar_base_datos(self):
        self.eliminar_base_datos_window = None
        if self.eliminar_base_datos_window is None:
            self.eliminar_base_datos_window = Eliminar_base()
        self.eliminar_base_datos_window.show()

    def actualizar(self):
        try:
            hora_actual = QDateTime.currentDateTime().toString('HH:mm:ss')
            hoy = today.day
            if hora_actual == "00:00:00" and hoy == 1:
                self.mantenimiento_mensual()
            if hora_actual == "12:17:00":
                # self.mantain()
                # self.un_dia_func()
                self.recordatorio_pagos()
        except Exception as e:
            print(e)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def add_numbers(self):
        self.close()
        if self.add_numbers_window is None:
            self.add_numbers_window = Addnumbers()
        self.add_numbers_window.show()

    def mantenimiento(self):
        self.close()
        if self.mantain_window is None:
            self.mantain_window = Mantain()
        self.mantain_window.show()

    def mantain(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("SELECT * FROM jugadas")

            plays = cursor.fetchall()

            current_datetime = datetime.now()

            for play in plays:

                fecha_hora_jugada = play[6]

                # Ajusta el formato para el nuevo estilo de fecha y hora

                fecha_hora_jugada = datetime.strptime(
                    fecha_hora_jugada, '%d/%m/%Y - %I:%M:%S %p')

                dias_pasados = (current_datetime - fecha_hora_jugada).days

                if dias_pasados >= 1:
                    id_banca = play[0]
                    id_sucursal = play[1]
                    id_ticket = play[2]
                    cursor = self.conexion.cursor()

                    cursor.execute("delete from jugadas where id_banca = %s and id_sucursal = %s and id_ticket = %s", (
                        id_banca, id_sucursal, id_ticket))

            self.conexion.commit()

            cursor.close()

        except Exception as e:

            enviar_correo_error(e)

            title = "Error"

            icon = QMessageBox.Critical

            text = f"Ha ocurrido un error inesperado y se le ha notificado a soporte. Se volverá a intentar de nuevo en segundos."

            ventanta_emergente_def(title, icon, text)

    def un_dia_func(self):
        try:

            cursor = self.conexion.cursor()

            tables = ["bloqueado", "restringido"]

            for i in range(len(tables)):

                tables_to_delete = tables[i]

                consulta = f"TRUNCATE TABLE {tables_to_delete}"

                cursor.execute(consulta)

                self.conexion.commit()

            cursor2 = self.conexion.cursor()

            cursor2.execute("SELECT * FROM ganancias")

            venta_hoy = cursor2.fetchall()

            for i in range(len(venta_hoy)):

                id_banca = venta_hoy[i][1]

                id_sucursal = venta_hoy[i][2]

                cursor3 = self.conexion.cursor()

                cursor3.execute(
                    "UPDATE ganancias SET venta_mensual = venta_mensual + venta_diaria, venta_diaria = '0' WHERE id_banca = %s AND id_sucursal = %s", (id_banca, id_sucursal))

                self.conexion.commit()

                cursor3.close()

            title = "Hecho"

            icon = QMessageBox.Information

            text = "La base de datos ha sido actualizada con exito, gracias por usar Genuine."

            ventanta_emergente_def(title, icon, text)

        except Exception as e:

            enviar_correo_error(e)

            title = "Error"

            icon = QMessageBox.Critical

            text = f"Ha ocurrido un error inesperado y se le ha notificado a soporte. Se volverá a intentar de nuevo en segundos."

            ventanta_emergente_def(title, icon, text)

    def mantenimiento_mensual(self):
        try:
            cursor2 = self.conexion.cursor()

            cursor2.execute("SELECT * FROM ganancias")

            venta_hoy = cursor2.fetchall()

            for i in range(len(venta_hoy)):

                id_banca = venta_hoy[i][1]

                id_sucursal = venta_hoy[i][2]

                cursor3 = self.conexion.cursor()

                cursor3.execute(
                    "UPDATE ganancias SET venta_anual = venta_mensual + venta_anual, venta_mensual = '0' WHERE id_banca = %s AND id_sucursal = %s", (id_banca, id_sucursal))

                self.conexion.commit()

                cursor3.close()

            title = "Hecho"

            icon = QMessageBox.Information

            text = "La base de datos ha sido actualizada con exito, gracias por usar Genuine."

            ventanta_emergente_def(title, icon, text)

        except mysql.connector.Error as err:

            print("Error:", err)

    def registrar_sucursal_banca(self):
        intentado = True
        while True:
            respuesta_usuario, resultado_dialogo = registrar_sucursal(
                "REGISTRO SUCURSAL", "dialog-question", "Por favor ingresa el ID de la banca."
            )
            if resultado_dialogo == QDialog.Accepted:
                registrar_sucursal_data(respuesta_usuario)

                    # para abrir la otra ventana.
                    #if self.registro_sucursal is None:
                    #    self.registro_sucursal = SucursalWindow(
                    #        id_banca, nombre_banca, nombre_propietario, telefono_principal, email_principal, cantidad_sucursales, nombre_sucursal)
                    #self.registro_sucursal.show()
                    #break
                #else:
                #    if intentado:
                #        title = "ERROR"
                #        icon = QMessageBox.Critical
                #        text = f"El ID de banca: {respuesta_usuario} es invalido".upper(
                #        )
                #        ventanta_emergente_def(title, icon, text)
            else:
                break

    def registrarpage(self):
        self.close()
        if self.registrarwindow == None:
            self.registrarwindow = RegistrarBanca()
        self.registrarwindow.show()

    def desactivar_banca(self):
        self.close()
        if self.desactivar_window is None:
            self.desactivar_window = Desactivar()
        self.desactivar_window.show()


def registrar_sucursal(title, icon, text):
    # Creamos una ventana emergente personalizada (QDialog)
    ventana_emergente = QDialog()
    ventana_emergente.setWindowTitle(title)
    # Convertimos el icono a QIcon
    ventana_emergente.setWindowIcon(QIcon.fromTheme(icon))

    # Establecemos un ancho mínimo para la ventana
    ventana_emergente.setMinimumWidth(300)

    # Creamos un layout de formulario para organizar los elementos
    layout = QFormLayout(ventana_emergente)

    # Agregamos una etiqueta con el texto deseado
    etiqueta = QLabel(text)
    layout.addRow(etiqueta)

    # Creamos un campo de entrada de texto (QLineEdit) y lo configuramos
    input_box = QLineEdit()
    # Texto de ayuda para el usuario
    input_box.setPlaceholderText("Ingresa el ID del ticket")
    layout.addRow("ID del ticket:", input_box)

    # Creamos un botón de aceptar
    boton_aceptar = QPushButton("Aceptar")
    layout.addRow(boton_aceptar)

    # Conectamos el botón "Aceptar" a la función que cierra la ventana y devuelve la respuesta
    boton_aceptar.clicked.connect(ventana_emergente.accept)

    # Ejecutamos la ventana y esperamos la respuesta del usuario
    resultado = ventana_emergente.exec_()

    # Obtenemos el texto ingresado por el usuario
    respuesta = input_box.text()

    # Devolvemos la respuesta del usuario y el resultado del cuadro de diálogo (Aceptar o Cancelar)
    return respuesta, resultado


def generate_salt():
    return uuid.uuid4().hex


def hash_password(password, salt):
    hashed_password = hashlib.sha256(
        password.encode() + salt.encode()).hexdigest()
    return hashed_password


class Eliminar_base(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/eliminar_base_datos.ui", self)
        self.check_connection()

    def check_connection(self):
        conexion = connection()
        if conexion == True:
            pass
        else:
            self.hide()
            self.title = "No se estableció una conexión"
            self.icon = QMessageBox.Information
            self.text = "No se pudo establecer una conexión, por favor revise su conexión a internet"
            self.ventanta_emergente_def(self.title, self.icon, self.text)
            QTimer.singleShot(333, self.close)


class Mantain(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/mantenimiento_base_datos.ui", self)
        self.uno.clicked.connect(self.un_dia_func)
        self.quince.clicked.connect(self.quince_dias)
        self.treinta.clicked.connect(self.treinta_dias)
        self.check_connection()
        self.id_banca = sesion_usuario.get("id_banca")
        self.id_sucursal = sesion_usuario.get("id_sucursal")

        # Obtener la fecha actual
        fecha_actual = datetime.now()

        # Calcular la fecha hace 30 días
        treinta_dias_antes = fecha_actual - timedelta(days=30)

        # Formatear las fechas en el formato deseado (dd/mm/yyyy)
        fecha_actual_formateada = fecha_actual.strftime('%d/%m/%Y')
        self.treinta_dias_antes_formateada = treinta_dias_antes.strftime(
            '%d/%m/%Y - %I:%M:%S %p')

    def check_connection(self):
        conexion = connection()
        if conexion == True:
            pass
        else:
            self.hide()
            self.title = "No se estableció una conexión"
            self.icon = QMessageBox.Information
            self.text = "No se pudo establecer una conexión, por favor revise su conexión a internet"
            self.ventanta_emergente_def(self.title, self.icon, self.text)
            QTimer.singleShot(333, self.close)

    def un_dia_func(self):
        try:
            cursor = self.conexion.cursor()
            tables = ["bloqueado", "restringido"]
            for i in range(len(tables)):
                tables_to_delete = tables[i]
                consulta = f"TRUNCATE TABLE {tables_to_delete}"
                cursor.execute(consulta)
                self.conexion.commit()
            title = "Hecho"
            icon = QMessageBox.Information
            text = "La base de datos ha sido actualizada con exito, gracias por usar Genuine."
            ventanta_emergente_def(title, icon, text)
            cursor2 = self.conexion.cursor()
            cursor2.execute("SELECT venta_diaria FROM ganancias WHERE id_banca = %s AND id_sucursal = %s",
                            (self.id_banca, self.id_sucursal))
            venta_hoy = cursor2.fetchone()
        except mysql.connector.Error as err:
            print("Error:", err)

    def quince_dias(self):
        pass

    def treinta_dias(self):
        try:
            # Crear un objeto cursor
            cursor = self.conexion.cursor()

            # Ejecutar la consulta para obtener los registros de hace 30 días o más
            tables = ["jugadas", "restringido"]
            dia = int(today.day)
            if dia == 1:
                for i in range(len(tables)):
                    tables_to_delete = tables[i]
                    consulta = f"TRUNCATE TABLE {tables_to_delete}"
                    cursor.execute(consulta)
                    self.conexion.commit()
                title = "Hecho"
                icon = QMessageBox.Information
                text = "La base de datos ha sido actualizada con exito, gracias por usar Genuine."
                ventanta_emergente_def(title, icon, text)
            else:
                title = "ERROR"
                icon = QMessageBox.Critical
                text = "Error, solo se puede actualizar la base de datos los días 1 de cada mes."
                ventanta_emergente_def(title, icon, text)
            cursor.close()

        except mysql.connector.Error as err:
            print("Error:", err)


class RegistrarBanca(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/registrobanca.ui", self)
        self.msj = False
        self.registrar_button.clicked.connect(self.register)
        self.check_connection()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def check_connection(self):
        conexion = connection()
        if conexion == True:
            pass
        else:
            self.hide()
            self.title = "No se estableció una conexión"
            self.icon = QMessageBox.Information
            self.text = "No se pudo establecer una conexión, por favor revise su conexión a internet"
            self.ventanta_emergente_def(self.title, self.icon, self.text)
            QTimer.singleShot(333, self.close)

    def register(self):
        # try:
        nombre_banca = self.nombre_banca.text()
        prefijo = self.prefijo.currentText()
        dia_pago = self.diapago.text()
        monto_pago = self.montopago.currentText()
        tipo_software = self.tiposoftware.currentText()
        pago_pale = self.pagopale.text()
        pago_tripleta = self.pagotripleta.text()
        puntos_primera = self.puntos_primera.text()
        puntos_segunda = self.puntos_segunda.text()
        puntos_tercera = self.puntos_tercera.text()
        nombre_dueno = self.nombre_dueno.text()
        nombre_sucursal = self.nombre_sucursal.text()
        telefono_principal = self.telefono_principal.text()
        email_principal = self.email_principal.text()
        usuario = self.user.text()
        password = self.password.text()
        nm = nombre_banca[:1]
        id_banca = str(uuid.uuid4()) + nm
        id_sucursal_to_convert = uuid.uuid4()
        id_sucursal = str(id_sucursal_to_convert)

        Lineedit_check = self.findChildren(QLineEdit)
        for i in Lineedit_check:
            input = i.text()

        if input == "":
            title = "Error"
            icon = QMessageBox.Critical
            text = "Uno o mas campos estan vacíos."
            ventanta_emergente_def(title, icon, text)
        else:
            data = register(nombre_banca, prefijo, dia_pago, monto_pago, tipo_software, pago_pale, pago_tripleta, puntos_primera, puntos_segunda,
                            puntos_tercera, nombre_dueno, nombre_sucursal, telefono_principal, email_principal, usuario, password, id_banca, id_sucursal
                            )
            if data == True:
                title = "Realizado"
                icon = QMessageBox.Information
                text = f"La banca ha sido registrada con éxito. El nombre de usuario es {usuario}. Las credenciales y el contrato del comprador serán enviados por correo. Gracias por usar GENUINE."
                ventanta_emergente_def(title, icon, text)
                Lineedit = self.findChildren(QLineEdit)
                for i in Lineedit:
                    i.setText("")
            else:
                title = "Error"
                icon = QMessageBox.Critical
                text = "Ha ocurrido un error al intentar registrar la banca."
   # except Exception as e:
        # Mostrar una ventana emergente de error en caso de excepción
        # QMessageBox.critical(None, "Error", f"Error: {str(e)}")


class Addnumbers(QMainWindow):
    def __init__(self):
        super().__init__()
        self.update_numbers = None
        uic.loadUi("UI/add_numbers.ui", self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.check_connection()

        self.AnguiladiezAM.clicked.connect(
            lambda: self.button_clicked("anguiladiezam"))
        self.CuartetadiezAM.clicked.connect(
            lambda: self.button_clicked("cuartetadiezam"))
        self.PrimeradocePM.clicked.connect(
            lambda: self.button_clicked("primeradocepm"))
        self.KingdocePM.clicked.connect(
            lambda: self.button_clicked("kingdocepm"))
        self.SuertedocePM.clicked.connect(
            lambda: self.button_clicked("suertedocepm"))
        self.AnguilaunaPM.clicked.connect(
            lambda: self.button_clicked("anguilaunapm"))
        self.CuartetaunaPM.clicked.connect(
            lambda: self.button_clicked("cuartetaunapm"))
        self.RealunaPM.clicked.connect(
            lambda: self.button_clicked("realunapm"))
        self.GanadosPM.clicked.connect(
            lambda: self.button_clicked("ganadospm"))
        self.NewdosPM.clicked.connect(lambda: self.button_clicked("newdospm"))
        self.AnguilaseisPM.clicked.connect(
            lambda: self.button_clicked("anguilaseispm"))
        self.CuartetaseisPM.clicked.connect(
            lambda: self.button_clicked("cuartetaseispm"))
        self.KingsietePM.clicked.connect(
            lambda: self.button_clicked("kingsietepm"))
        self.LotekasietePM.clicked.connect(
            lambda: self.button_clicked("lotekasietepm"))
        self.NacionalochoPM.clicked.connect(
            lambda: self.button_clicked("nacionalochopm"))
        self.LeidsaochoPM.clicked.connect(
            lambda: self.button_clicked("leidsaochopm"))
        self.AnguilanuevePM.clicked.connect(
            lambda: self.button_clicked("anguilanuevepm"))
        self.CuartetanuevePM.clicked.connect(
            lambda: self.button_clicked("cuartetanuevepm"))
        self.FloridanuevePM.clicked.connect(
            lambda: self.button_clicked("floridanuevepm"))
        self.floridadospm.clicked.connect(
            lambda: self.button_clicked("floridadospm"))
        self.NewdiezPM.clicked.connect(
            lambda: self.button_clicked("newdiezpm"))

    def check_connection(self):
        conexion = connection()
        if conexion == True:
            pass
        else:
            self.hide()
            self.title = "No se estableció una conexión"
            self.icon = QMessageBox.Information
            self.text = "No se pudo establecer una conexión, por favor revise su conexión a internet"
            self.ventanta_emergente_def(self.title, self.icon, self.text)
            QTimer.singleShot(333, self.close)

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


class DevolucionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/devolucion.ui", self)
        self.boton_devolucion.clicked.connect(self.on_devolution)
        self.id_banca = sesion_usuario.get('id_banca')
        self.id_sucursal = sesion_usuario.get('id_sucursal')
        self.check_connection()

    def check_connection(self):
        conexion = connection()
        if conexion == True:
            pass
        else:
            self.hide()
            self.title = "No se estableció una conexión"
            self.icon = QMessageBox.Information
            self.text = "No se pudo establecer una conexión, por favor revise su conexión a internet"
            self.ventanta_emergente_def(self.title, self.icon, self.text)
            QTimer.singleShot(333, self.close)

    def on_devolution(self):
        id_ticket = self.idticket.text()
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM jugadas WHERE id_banca = %s and id_sucursal = %s and id_ticket = %s",
                       (self.id_banca, self.id_sucursal, id_ticket))
        ticket = cursor.fetchall()
        cursor.close()
        if ticket:
            tickets = []
            numeros_jugados = []
            montos_jugados = []
            for i in range(len(ticket)):
                fecha_hora_str = ticket[i][6]
                fecha_hora = datetime.strptime(
                    fecha_hora_str, "%d/%m/%Y - %I:%M:%S %p")
                tickets.append(ticket[i])
                numero_jugado = ticket[i][3]
                monto_jugado = ticket[i][4]
                numeros_jugados.append(numero_jugado)
                montos_jugados.append(monto_jugado)

                # Obtiene la hora actual
                hora_actual = datetime.now()

                # Calcula la diferencia entre la hora actual y la hora almacenada en el ticket
                diferencia = hora_actual - fecha_hora

                # Obtener el tiempo transcurrido en minutos
                minutos_transcurridos = diferencia.total_seconds() / 60

                # Comparar si han pasado 15 minutos
            if minutos_transcurridos >= 15:
                title = "ERROR"
                icon = QMessageBox.Critical
                text = "Ya pasaron 15 minutos desde que se realizó esta jugada."
                ventanta_emergente_def(title, icon, text)
            else:
                title = "!"
                icon = QMessageBox.Information
                text = f"Realmente deseas cancelar este ticket?"

                ventana_emergente = QMessageBox()
                ventana_emergente.setWindowTitle(title)
                ventana_emergente.setText(text)
                ventana_emergente.setIcon(icon)
                # Crear un botón personalizado y agregarlo a la ventana emergente
                boton_pagar = QPushButton("Aceptar")
                ventana_emergente.addButton(boton_pagar, QMessageBox.YesRole)

                # Agregar el botón "Cancelar" y establecerlo como el botón por defecto
                boton_cancelar = ventana_emergente.addButton(
                    "Cancelar", QMessageBox.NoRole)
                ventana_emergente.setDefaultButton(boton_cancelar)

                # Mostrar la ventana emergente y esperar a que el usuario interactúe con ella
                resultado = ventana_emergente.exec_()
                if ventana_emergente.clickedButton() == boton_pagar:
                    i = 0
                    for i in range(len(tickets)):
                        numero_for_database = numeros_jugados[i]
                        monto_for_database = montos_jugados[i]
                        cursor = self.conexion.cursor()
                        cursor.execute("DELETE FROM jugadas WHERE id_banca = %s AND id_sucursal = %s AND id_ticket = %s", (
                            self.id_banca, self.id_sucursal, id_ticket))
                        cursor2 = self.conexion.cursor()
                        cursor2.execute("INSERT INTO anulados VALUES (%s, %s, %s, %s, %s, %s)", (
                            self.id_banca, self.id_sucursal, id_ticket, monto_for_database, numero_for_database, today.day))
                        self.conexion.commit()
                        cursor.close()
                    title = "Hecho"
                    icon = QMessageBox.Critical
                    text = "Ticket anulado con exito"
                    ventanta_emergente_def(title, icon, text)
        else:
            title = "ERROR"
            icon = QMessageBox.Critical
            text = "TICKET NO ENCONTRADO"
            ventanta_emergente_def(title, icon, text)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


class UpdateNumber(QMainWindow):
    def __init__(self, lottery):
        super().__init__()
        uic.loadUi("UI/UPDATE_NUMBER.ui", self)
        self.check_connection()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.push_lotterie.clicked.connect(lambda: self.push_number(lottery))
        self.first.setFocus()
        self.add_numbers_window = None
        self.first.setValidator(QtGui.QIntValidator())
        self.second.setValidator(QtGui.QIntValidator())
        self.third.setValidator(QtGui.QIntValidator())
        self.first.returnPressed.connect(self.firstfocus)
        self.second.returnPressed.connect(self.secondfocus)
        self.third.returnPressed.connect(lambda: self.push_number(lottery))
        self.loteria.setText(f"Loteria seleccionada: {lottery}")

    def check_connection(self):
        conexion = connection()
        if conexion == True:
            pass
        else:
            self.hide()
            self.title = "No se estableció una conexión"
            self.icon = QMessageBox.Information
            self.text = "No se pudo establecer una conexión, por favor revise su conexión a internet"
            self.ventanta_emergente_def(self.title, self.icon, self.text)
            QTimer.singleShot(333, self.close)

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
        elif second == "":
            title = "ERROR"
            icon = QMessageBox.Critical
            text = "El segundo premio no puede estar vacío"
            ventanta_emergente_def(title, icon, text)
            self.second.setFocus()
        elif third == "":
            title = "ERROR"
            icon = QMessageBox.Critical
            text = "El tercer premio no puede estar vacío"
            ventanta_emergente_def(title, icon, text)
            self.third.setFocus()
        else:

            title = "!"
            icon = QMessageBox.Information
            text = f"Desea agregar esos numeros a la plataforma?"

            ventana_emergente = QMessageBox()
            ventana_emergente.setWindowTitle(title)
            ventana_emergente.setText(text)
            ventana_emergente.setIcon(icon)
            # Crear un botón personalizado y agregarlo a la ventana emergente
            boton_pagar = QPushButton("Aceptar")
            ventana_emergente.addButton(boton_pagar, QMessageBox.YesRole)

            # Agregar el botón "Cancelar" y establecerlo como el botón por defecto
            boton_cancelar = ventana_emergente.addButton(
                "Cancelar", QMessageBox.NoRole)
            ventana_emergente.setDefaultButton(boton_cancelar)

            # Mostrar la ventana emergente y esperar a que el usuario interactúe con ella
            resultado = ventana_emergente.exec_()

            # Comprobar si el botón "Pagar" fue presionado
            if ventana_emergente.clickedButton() == boton_pagar:
                # Obtenemos la fecha actual
                fecha_actual = datetime.now()
                dia_mes_ano = fecha_actual.strftime('%d/%m/%Y')

                # Formamos la consulta SQL con el nombre de la tabla
                consulta_sql = f"INSERT INTO {lottery} VALUES (%s, %s)"
                # Ejecutamos la consulta SQL con los valores
                cursor = self.conexion2.cursor()
                cursor.execute(consulta_sql, (dia_mes_ano, final))
                self.conexion2.commit()
                cursor.close()
                self.add_numbers()


class Desactivar(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/desactivar.ui", self)
        self.check_connection()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.eliminar_boton.clicked.connect(self.desactivar)

    def check_connection(self):
        conexion = connection()
        if conexion == True:
            pass
        else:
            self.hide()
            self.title = "No se estableció una conexión"
            self.icon = QMessageBox.Information
            self.text = "No se pudo establecer una conexión, por favor revise su conexión a internet"
            self.ventanta_emergente_def(self.title, self.icon, self.text)
            QTimer.singleShot(333, self.close)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def desactivar(self):
        id_banca = self.id_banca.text()
        cursor = self.conexion.cursor()
        cursor.execute(
            "SELECT activa FROM banca WHERE idbanca = %s", (id_banca, ))
        deativated = cursor.fetchall()
        if deativated is not None:
            title = "!"
            icon = QMessageBox.Critical
            text = f"Realmente desea desactivar esta banca?"

            ventana_emergente = QMessageBox()
            ventana_emergente.setWindowTitle(title)
            ventana_emergente.setText(text)
            ventana_emergente.setIcon(icon)
            # Crear un botón personalizado y agregarlo a la ventana emergente
            boton_pagar = QPushButton("Desactivar")
            ventana_emergente.addButton(boton_pagar, QMessageBox.YesRole)

            # Agregar el botón "Cancelar" y establecerlo como el botón por defecto
            boton_cancelar = ventana_emergente.addButton(
                "Cancelar", QMessageBox.NoRole)
            ventana_emergente.setDefaultButton(boton_cancelar)

            # Mostrar la ventana emergente y esperar a que el usuario interactúe con ella
            resultado = ventana_emergente.exec_()

            # Comprobar si el botón "Pagar" fue presionado
            if ventana_emergente.clickedButton() == boton_pagar:
                cursor.execute(
                    "UPDATE banca SET activa = %s WHERE idbanca = %s", ("NO", id_banca))
                self.conexion.commit()
                cursor.close()
                title = "Hecho"
                icon = QMessageBox.Information
                text = "La banca ha sido desactivada con exito."
                ventanta_emergente_def(title, icon, text)
        else:
            title = "Error"
            icon = QMessageBox.Critical
            text = "Banca no encontrada, por favor inserte el ID nuevamente."
            ventanta_emergente_def(title, icon, text)


class desactivada(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/banca_desactivada.ui", self)
        self.check_connection()

    def check_connection(self):
        conexion = connection()
        if conexion == True:
            pass
        else:
            self.hide()
            self.title = "No se estableció una conexión"
            self.icon = QMessageBox.Information
            self.text = "No se pudo establecer una conexión, por favor revise su conexión a internet"
            self.ventanta_emergente_def(self.title, self.icon, self.text)
            QTimer.singleShot(333, self.close)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


class SucursalWindow(QMainWindow):
    def __init__(self, id_banca, nombre_banca, nombre_dueno, telefono_principal, email_principal, cantidad_sucursales, nombre_sucursal_text):
        super().__init__()
        uic.loadUi("UI/banca_sucursal.ui", self)
        self.check_connection()
        self.nombre_banca.setText(nombre_banca)
        self.button_for_register.clicked.connect(self.sucursal)
        self.nombre_dueno.setText(nombre_dueno)
        self.telefono_principal.setText(telefono_principal)
        self.cantidad.setText(cantidad_sucursales)
        self.email_principal.setText(email_principal)
        self.nombre_sucursal.setText(nombre_sucursal_text)
        self.id_banca = id_banca
        self.email_principal = email_principal

    def check_connection(self):
        conexion = connection()
        if conexion == True:
            pass
        else:
            self.hide()
            self.title = "No se estableció una conexión"
            self.icon = QMessageBox.Information
            self.text = "No se pudo establecer una conexión, por favor revise su conexión a internet"
            self.ventanta_emergente_def(self.title, self.icon, self.text)
            QTimer.singleShot(333, self.close)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def sucursal(self):
        id_banca = self.id_banca
        email_principal = self.email_principal
        id_sucursal_to_convert = uuid.uuid4()
        id_sucursal = str(id_sucursal_to_convert)
        persona_a_cargo = self.persona_acargo.text()
        numero_contacto = self.numerocontacto.text()
        numero_secundario = self.numerosecundario.text()
        email_contacto = self.emailcontacto.text()
        dia_pago = self.diapago.text()
        monto_pago = self.montopago.currentText()
        tipo_software = self.tiposoftware.currentText()
        pago_pale = self.pagopale.text()
        pago_tripleta = self.pagotripleta.text()
        puntos_primera = self.puntos_primera.text()
        puntos_segunda = self.puntos_segunda.text()
        puntos_tercera = self.puntos_tercera.text()
        nombre_sucursal = self.nombre_sucursal.text()
        usuario = self.user.text()
        password = self.password.text()
        inputs = self.findChildren(QLineEdit)
        for i in inputs:
            input = i.text()
        if input == '' or input == ' ':
            title = "Error"
            icon = QMessageBox.Critical
            text = "Para continuar debes rellenar todos los campos"
            ventanta_emergente_def(title, icon, text)
        else:
            cursor = self.conexion.cursor()
            cursor.execute(
                "UPDATE informacion_banca SET cantidad_sucursales = cantidad_sucursales + 1 WHERE id_banca = %s", (id_banca, ))
            cursor.close()
            cursor2 = self.conexion.cursor()
            cursor2.execute("INSERT INTO banca (id, idbanca, id_sucursal, nombre_sucursal, persona_encargada, numerocontacto, contacto_secundario, email_contacto, dia_pago, monto_pago, software_comprado, pago_pale, pago_tripleta, punto_primera, punto_segunda, punto_tercera, activa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (0, id_banca, id_sucursal, nombre_sucursal, persona_a_cargo, numero_contacto, numero_secundario, email_contacto, dia_pago, monto_pago, tipo_software, pago_pale, pago_tripleta, puntos_primera, puntos_segunda, puntos_tercera, "SI"))
            cursor3 = self.conexion.cursor()
            cursor3.execute("INSERT INTO auth (idauth, id_banca, id_sucursal, user, password) VALUES (%s, %s, %s, %s, %s)",
                            (0, id_banca, id_sucursal, usuario, password))
            cursor4 = self.conexion.cursor()
            cursor4.execute("INSERT INTO ganancias VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (0, id_banca, id_sucursal, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
            title = "Realizado"
            icon = QMessageBox.Information
            text = f"""La banca ha sido registrada con éxito. El nombre de usuario es {usuario}. 
                        Las credenciales y el contrato del comprador serán enviados por correo.
                        Gracias por usar GENUINE.
                    """
            self.conexion.commit()
            Lineedit = self.findChildren(QLineEdit)
            for i in Lineedit:
                i.setText("")
            ventanta_emergente_def(title, icon, text)
            destinatario = email_principal
            enviar_correo2(destinatario, usuario, password)


class BlockNumbers(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/numeros_bloqueados.ui", self)
        self.check_connection()
        id_banca = sesion_usuario.get('id_banca')
        id_sucursal = sesion_usuario.get('id_sucursal')
        cursor = self.conexion.cursor()
        cursor.execute(
            "SELECT * FROM bloqueado WHERE id_banca = %s AND id_sucursal = %s", (id_banca, id_sucursal))
        numeros = cursor.fetchall()
        if numeros != []:
            for i in range(len(numeros)):
                item1 = QListWidgetItem(numeros[i][2])
                self.block_numbers.addItem(item1)

    def check_connection(self):
        conexion = connection()
        if conexion == True:
            pass
        else:
            self.hide()
            self.title = "No se estableció una conexión"
            self.icon = QMessageBox.Information
            self.text = "No se pudo establecer una conexión, por favor revise su conexión a internet"
            self.ventanta_emergente_def(self.title, self.icon, self.text)
            QTimer.singleShot(333, self.close)


today = datetime.now()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())
