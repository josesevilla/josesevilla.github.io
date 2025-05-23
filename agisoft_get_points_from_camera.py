#highlights valid matches for selected photos in active chunk
#compatibility: starting from Agisoft PhotoScan Pro 0.9.0

import PhotoScan

doc = PhotoScan.app.document
chunk = doc.chunk
point_cloud = chunk.tie_points
points = point_cloud.points
npoints = len(point_cloud.points)

selected_photos = list()

for photo in chunk.cameras:
    if photo.selected:
        selected_photos.append(photo)

for photo in selected_photos:

	point_index = 0
	for proj in point_cloud.projections[photo]:
		track_id = proj.track_id
		while point_index < npoints and points[point_index].track_id < track_id:
			point_index += 1
		if point_index < npoints and points[point_index].track_id == track_id:
			if points[point_index].valid:
				points[point_index].selected = True

PhotoScan.app.update()
