import Metashape
from PySide2 import QtWidgets
import os

doc = Metashape.app.document
step = 3

if not doc.path:
    QtWidgets.QMessageBox.warning(None, "Error", "Primero guarda el proyecto de Metashape antes de usar este script.")
else:
    class VideoImportDialog(QtWidgets.QDialog):
        def __init__(self, parent=None):
            super(VideoImportDialog, self).__init__(parent)
            self.setWindowTitle("Importar vídeo a Metashape")
            self.setFixedSize(500, 200)

            project_folder = os.path.dirname(doc.path)
            self.default_output_dir = os.path.abspath(os.path.join(project_folder, "..", "imagenes"))

            if not os.path.exists(self.default_output_dir):
                os.makedirs(self.default_output_dir)

            # Widgets
            self.video_label = QtWidgets.QLabel("Ruta del vídeo:")
            self.video_path = QtWidgets.QLineEdit()
            self.video_button = QtWidgets.QPushButton("Buscar vídeo...")

            self.output_label = QtWidgets.QLabel("Carpeta de salida:")
            self.output_path = QtWidgets.QLineEdit(self.default_output_dir)
            self.output_button = QtWidgets.QPushButton("Seleccionar carpeta...")

            self.step_label = QtWidgets.QLabel("Espaciado entre fotogramas:")
            self.step_input = QtWidgets.QSpinBox()
            self.step_input.setMinimum(1)
            self.step_input.setValue(step)

            self.run_button = QtWidgets.QPushButton("Importar vídeo")

            # Layout
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(self.video_label)
            hlayout1 = QtWidgets.QHBoxLayout()
            hlayout1.addWidget(self.video_path)
            hlayout1.addWidget(self.video_button)
            layout.addLayout(hlayout1)

            layout.addWidget(self.output_label)
            hlayout2 = QtWidgets.QHBoxLayout()
            hlayout2.addWidget(self.output_path)
            hlayout2.addWidget(self.output_button)
            layout.addLayout(hlayout2)

            layout.addWidget(self.step_label)
            layout.addWidget(self.step_input)
            layout.addWidget(self.run_button)

            self.setLayout(layout)

            # Conexiones
            self.video_button.clicked.connect(self.select_video)
            self.output_button.clicked.connect(self.select_output_folder)
            self.run_button.clicked.connect(self.import_video)

        def select_video(self):
            path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Seleccionar vídeo", "", "Vídeos (*.mp4 *.avi *.mov *.mkv)")
            if path:
                self.video_path.setText(path)

        def select_output_folder(self):
            path = QtWidgets.QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de salida")
            if path:
                self.output_path.setText(path)

        def import_video(self):
            video_path = self.video_path.text().strip()
            output_dir = self.output_path.text().strip()
            frame_step = self.step_input.value()

            if not os.path.isfile(video_path):
                QtWidgets.QMessageBox.warning(self, "Error", "La ruta del vídeo no es válida.")
                return

            if not os.path.isdir(output_dir):
                QtWidgets.QMessageBox.warning(self, "Error", "La carpeta de salida no es válida.")
                return

            try:
                chunk = doc.addChunk()
                frame_template = os.path.join(output_dir, "frame{filenum}.jpg")

                chunk.importVideo(
                    video_path,
                    frame_template,
                    frame_step=Metashape.CustomFrameStep,
                    custom_frame_step=frame_step,
                    time_start=0,
                    time_end=-1
                )

                QtWidgets.QMessageBox.information(self, "Importación completa", "El vídeo se ha importado correctamente.")
                self.accept()

            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", str(e))

    # Crear y ejecutar el diálogo
    dlg = VideoImportDialog()
    dlg.exec_()
