import Metashape
chunk = Metashape.app.document.chunk
for marker in chunk.markers:
    for camera in list(marker.projections.keys()):
        if not marker.projections[camera].pinned:
            marker.projections[camera] = None