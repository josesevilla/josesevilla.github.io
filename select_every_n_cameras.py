import Metashape
chunk = Metashape.app.document.chunk
Metashape.app.update()
step = Metashape.app.getInt("Specify the selection step:" ,5)
index = 1
for camera in chunk.cameras:
      if not (index % step):
            camera.selected = True
      else:
            camera.selected = False
      index += 1