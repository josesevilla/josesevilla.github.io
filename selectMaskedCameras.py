import Metashape
chunk = Metashape.app.document.chunk
for cam in chunk.cameras:
Metashape.app.update()
    cam.selected = cam.mask is not None