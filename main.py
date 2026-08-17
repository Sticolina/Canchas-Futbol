import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea
from database import CANCHAS
from styles import STYLE_SHEET
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from detalles import VentanaDetalle


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Canchas Futbol')
        self.resize(700, 800)
        self.setStyleSheet(STYLE_SHEET)

        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setSpacing(0)
        layout_principal.setContentsMargins(10, 50, 10, 10) # Espacio en los bordes (izq, arriba, der, abajo)
        layout_principal.setAlignment(Qt.AlignTop)
        layout_principal.setSpacing(20)

        # TITULO PRINCIPAL
        self.label_titulo = QLabel('FUTBOL GAMES')

        # Estilo para resaltar
        self.label_titulo.setStyleSheet("font-size: 35px; font-weight: bold; color: #FF8C00; margin-top: 5px;")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(self.label_titulo)

        #SUBTÍTULO / INSTRUCCIÓN 
        self.label_subtitulo = QLabel("Debe seleccionar una cancha de su preferencia\ny así continuar con la reserva")
        # Un estilo más discreto pero elegante
        self.label_subtitulo.setStyleSheet("font-size: 14px; color: white; margin-top: 0px; margin-bottom: 10px;")
        self.label_subtitulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(self.label_subtitulo)
        layout_principal.addSpacing(40)

        fila_actual = None

        for i, cancha in enumerate(CANCHAS):
            if i % 2 == 0:
                fila_actual = QHBoxLayout()
                layout_principal.addLayout(fila_actual)

            caja_cancha = QVBoxLayout()

            imagen_label = QLabel()
            pixel_map = QPixmap(cancha['img'])
            imagen_label.setPixmap(pixel_map.scaled(250, 180, Qt.KeepAspectRatio))
            imagen_label.setAlignment(Qt.AlignCenter)

            caja_cancha.addWidget(imagen_label)
            boton = QPushButton(cancha['nombre'])
            caja_cancha.addWidget(boton)
            fila_actual.addLayout(caja_cancha)
            boton.clicked.connect(lambda checked, c=cancha: self.mostrar_detalle(c))

    # Al final de todo el __init__, fuera del for:
        layout_principal.addStretch(1)   
   
    def mostrar_detalle(self, datos_cancha):
        # Por ahora, solo vamos a imprimir en la consola para ver si funciona
        print(f"--- Abriendo información de: {datos_cancha['nombre']} ---")
        print(f"Ubicación: {datos_cancha['ubicación']}")
        print(f"Precio: ${datos_cancha['precios_USD']}")
        self.nueva_ventana = VentanaDetalle(datos_cancha)
        self.nueva_ventana.show()

if __name__ == '__main__':
    app= QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())