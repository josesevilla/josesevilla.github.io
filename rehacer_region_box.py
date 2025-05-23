import Metashape, math

chunk = Metashape.app.document.chunk
region = chunk.region
T = chunk.transform.matrix

m = Metashape.Vector([10E+10, 10E+10, 10E+10])
M = -m

for point in chunk.point_cloud.points:
	if not point.valid:
		continue
	coord = T * point.coord	
	for i in range(3):
		m[i] = min(m[i], coord[i])
		M[i] = max(M[i], coord[i])
		
center = (M + m) / 2
size = M - m
region.center = T.inv().mulp(center)
region.size = size * (1 / T.scale())

region.rot = T.rotation().t()

chunk.region = region
Metashape.app.update()
print("Script finished.")