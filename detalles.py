from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QLineEdit, QMessageBox, QFileDialog #BUSCAR COMPROBANTE
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from styles import STYLE_SHEET
from functions import obtener_tasa_bcv, validar_reserva

class VentanaDetalle(QWidget):
    def __init__(self, datos_cancha):
        super().__init__()
        self.datos = datos_cancha # Aquí recibimos toda la info de la cancha tocada
        self.main_layout = QVBoxLayout(self)
        self.setWindowTitle(f"Reservar - {self.datos['nombre']}")
        self.resize(500, 800)
        self.setStyleSheet(STYLE_SHEET)      

        # Creamos una etiqueta vacía que usaremos luego para mostrar el precio en Bs
        self.label_pago = QLabel("")
        self.label_pago.setStyleSheet("color: #FF8C00; font-weight: bold; font-size: 18px;")
        self.main_layout.addWidget(self.label_pago)
        


        #TÍTULO DE LA CANCHA
        self.label_nombre = QLabel(self.datos['nombre'])
        self.label_nombre.setStyleSheet("font-size: 24px; font-weight: bold; color: #FF8C00;")
        self.label_nombre.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.label_nombre)

        #imagen
        self.img_detalle = QLabel()
        mapa_pixeles = QPixmap(self.datos['img']) 
        self.img_detalle.setPixmap(mapa_pixeles.scaled(400, 250, Qt.KeepAspectRatio)) #la imagen no se vea estirada
        self.img_detalle.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.img_detalle)

        #INFORMACIÓN
        info_txt = f"Ubicación: {self.datos['ubicación']}\nPrecio: {self.datos['precios_USD']}$"
        self.label_info = QLabel(f"Ubicación: {self.datos['ubicación']}\nPrecio: {self.datos['precios_USD']}$")
        self.label_info.setStyleSheet("font-size: 16px; color: white; margin: 10px;")
        self.main_layout.addWidget(self.label_info)

        #SELECCIÓN DE HORARIO
        self.main_layout.addWidget(QLabel("Seleccione el Horario:"))
        self.combo_horarios = QComboBox() #menu desplegable
        
        # Llenamos el combo solo con horarios "Disponibles"
        for h in self.datos['horarios']:
            if h['estado'] == "Disponible":
                self.combo_horarios.addItem(h['hora'])
        self.main_layout.addWidget(self.combo_horarios)

        #JUGADORES
        self.main_layout.addWidget(QLabel("Número de jugadores (Mínimo 10):"))
        self.input_jugadores = QLineEdit()
        self.input_jugadores.setPlaceholderText("Ej: 12")
        self.main_layout.addWidget(self.input_jugadores)

        #pagos
        self.label_pago = QLabel("")
        self.label_pago.setStyleSheet("color: #FF8C00; font-weight: bold; font-size: 16px;")
        self.main_layout.addWidget(self.label_pago)
        self.main_layout.addStretch()

        #Boton de validacion
        
        self.btn_confirmar = QPushButton("Validar Reserva")
        self.btn_confirmar.clicked.connect(self.procesar_reserva) # Conectamos a la función
        self.main_layout.addWidget(self.btn_confirmar)

    def procesar_reserva(self):
        # 1. Obtener lo que el usuario escribió
        texto_jugadores = self.input_jugadores.text()

        # 2. Verificar que no esté vacío y que sea un número
        if not texto_jugadores.isdigit(): #si ingresa alguna letra
            QMessageBox.warning(self, "Error", "Por favor, ingresa un número válido de jugadores.")
            return

        cantidad = int(texto_jugadores)

        # 3. Usar tu función de validar_reserva
        if validar_reserva(cantidad):
            # --- SI HAY 10 O MÁS JUGADORES ---
            tasa = obtener_tasa_bcv()
            precio_usd = self.datos['precios_USD']
            precio_bs = precio_usd * tasa

            # Mostramos el resultado
            self.label_pago.setText(
                f"Tasa BCV: {tasa} Bs.\n"
                f"Total a Pagar: {precio_bs:.2f} Bs."
            )
            QMessageBox.information(self, "Éxito", "Mínimo de jugadores alcanzado. Puede proceder al pago.")
            
            # Aquí es donde luego mostraremos los botones de Pago Móvil
            self.mostrar_metodos_pago() 
        else:
            # --- SI HAY MENOS DE 10 ---
            QMessageBox.critical(self, "Reserva Bloqueada", "Se requiere un mínimo de 10 jugadores para reservar.")
            self.label_pago.setText("")

    def mostrar_metodos_pago(self):
        # 1. Título de pagos
        if hasattr(self, 'combo_pago'): #impide que se vuelvan a crear los elementos de pago en pantalla
            return
        
        titulo_pago = QLabel("MÉTODOS DE PAGO")
        titulo_pago.setStyleSheet("font-weight: bold; margin-top: 20px; color: #FF8C00;")
        self.main_layout.addWidget(titulo_pago)

        # 2. Selección de método
        self.combo_pago = QComboBox()
        self.combo_pago.addItems(["Pago Móvil"])
        self.main_layout.addWidget(self.combo_pago)

        # 3. Datos del Pago Móvil (estarán ocultos al principio)
        self.info_pago_movil = QLabel("Banco: 0102 - Banesco\nRIF: J-12345678\nTelf: 0412-0000000")
        self.info_pago_movil.setStyleSheet("color: white; font-size: 14px; margin: 10px 0px;")
        self.info_pago_movil.setVisible(True)  #aparezca solo cuando la reserva ha sido validada
        self.main_layout.addWidget(self.info_pago_movil)

        # 4. Botón para cargar comprobante
        self.btn_comprobante = QPushButton("Cargar Comprobante de Pago")
        self.btn_comprobante.setVisible(True) # Se oculta
        self.btn_comprobante.clicked.connect(self.subir_foto_pago)
        self.main_layout.addWidget(self.btn_comprobante)        

    def subir_foto_pago(self):
        # Abre el explorador de archivos de Windows/Mac/Linux
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar Comprobante", "", "Imágenes (*.png *.jpg *.jpeg)")
        
        if archivo:
            QMessageBox.information(self, "Carga Exitosa", f"Comprobante recibido: {archivo.split('/')[-1]}")
            self.btn_comprobante.setText("✅ Comprobante Cargado")
            self.btn_comprobante.setStyleSheet("background-color: green; color: white;")

    def cambio_metodo_pago(self):
        # Si elige Pago Móvil, mostramos los datos y el botón de subir foto
        es_pago_movil = self.combo_pago.currentText() == "Pago Móvil"
        self.info_pago_movil.setVisible(es_pago_movil)
        self.btn_comprobante.setVisible(es_pago_movil)
    