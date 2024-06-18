from build123d import *
from ocp_vscode import show, show_all


'''
# Create a box with holes on each face
with BuildPart() as custom_box:
    Box(100, 100, 100)
    with GridLocations(25, 25, 4, 4):
        Hole(10)
show(custom_box)

b = Box(1, 2, 3)
c = Cylinder(0.2, 5)
r = b & c
# show(r)

alg = Plane.XZ * Pos(1, 2, 3) * Rot(0, 100, 45) * Box(1, 2, 3)
alg2 = Location((1, 2, 3), (0, 100, 45)) * Box(1, 2, 3)
# show(Plane.XY, Plane.XZ, alg, alg2)

l, w, h = 80.0, 60.0, 10.0
with BuildPart() as ex1:
    Box(l, w, h)
ex1a = Box(l, w, h)
# show(ex1a)

center_hole_diam = 22.0
with BuildPart() as ex2:
    Box(l, w, h)
    Cylinder(radius=center_hole_diam / 2, height=h, mode=Mode.SUBTRACT)
ex2a = Box(l, w, h) - Cylinder(radius=center_hole_diam / 2, height=h)
# show(ex2a)

with BuildPart() as ex3:
    with BuildSketch() as ex3_sk:
        Circle(w)
        Rectangle(l / 2, w / 2, mode=Mode.SUBTRACT)
    extrude(amount=2 * h)
sk3 = Circle(w) - Rectangle(l / 2, w / 2)
ex3a = extrude(sk3, amount=2 * h)
# show(ex3a)

with BuildPart() as ex4:
    with BuildSketch() as ex4_sk:
      with BuildLine() as ex4_ln:
          l1 = Line((0, 0), (l, 0))
          l2 = Line((l, 0), (l, w))
          l3 = ThreePointArc((l, w), (w, w * 1.5), (0.0, w))
          l4 = Line((0.0, w), (0, 0))
      make_face()
    extrude(amount=h)
    
l, w, h = 80.0, 60.0, 10.0
lines = Curve() + [
  Line((0, 0), (l, 0)),
  Line((l, 0), (l, w)),
  ThreePointArc((l, w), (w, w * 1.5), (0.0, w)),
  Line((0.0, w), (0, 0)),
]
sk4a = make_face(lines)
ex4a = extrude(sk4a, h)
# show(ex4a)

diam = 80
holes = Sketch()
r = Rectangle(2,2)
for loc in GridLocations(4, 4, 20, 20):
  if loc.position.X**2 + loc.position.Y**2 < (diam / 2 - 1.8) ** 2:
    holes += loc * r
# holes = [
#   loc * r
#   for loc in GridLocations(4, 4, 20, 20).locations
#     if loc.position.X**2 + loc.position.Y**2 < (diam / 2 - 1.8) ** 2
# ]
c = Circle(diam / 2) - holes
# show(c)

polygons = Sketch() + [
  loc * RegularPolygon(radius=5, side_count=5)
  for loc in GridLocations(40, 40, 2, 2)
]
# show(polygons)
  

a, b, c, d = 90, 45, 15, 7.5
with BuildPart() as ex5:
  with BuildSketch() as ex5_sk:
    Circle(a)
    with Locations((b, 0.0)):
      Rectangle(c, c, mode=Mode.SUBTRACT)
    with Locations((0, b)):
      Circle(d, mode=Mode.SUBTRACT)
  extrude(amount=c)
# show(ex5)

sk5a = Circle(a) - Pos(b, 0.0) * Rectangle(c, c) - Pos(0.0, b) * Circle(d)
ex5a = extrude(sk5a, c)
# show(ex5a)

a, b, c = 80, 60, 10
with BuildPart() as ex6:
  with BuildSketch() as ex6_sk:
    Circle(a)
    with Locations((b, 0), (0, b), (-b, 0), (0, -b)):
      Circle(c, mode=Mode.SUBTRACT)
  extrude(amount=c)
# show(ex6)

sk6 = [loc * Circle(c) for loc in Locations((b, 0), (0, b), (-b, 0), (0, -b))]
ex6a = extrude(Circle(a) - sk6, c)
# show(ex6a)

a, b, c = 60, 80, 5
with BuildPart() as  ex7: 
  with BuildSketch() as sk7:
    Rectangle(a, b)
    with Locations((0, 3 * c), (0, -3 * c)):
      RegularPolygon(radius=2 * c, side_count=6, mode=Mode.SUBTRACT)
  extrude(amount=c)
# show(ex7)

polygons = [
  loc * RegularPolygon(radius=2 * c, side_count=6)
  for loc in Locations((0, 3 * c), (0, -3 * c))
]
sk7a = Rectangle(a, b) - polygons
ex7a = extrude(sk7, amount=c)
# show(ex7a)

(L, H, W, t) = (100.0, 20.0, 20.0, 1.0)
pts = [
  (0, H / 2.0),
  (W / 2.0, H / 2.0),
  (W / 2.0, (H / 2.0 - t)),
  (t / 2.0, (H / 2.0 - t)),
  (t / 2.0, (t - H / 2.0)),
  (W / 2.0, (t - H / 2.0)),
  (W / 2.0, H / -2.0),
  (0, H / -2.0),
]
with BuildPart() as ex8: 
  with BuildSketch(Plane.YZ) as ex8_sk:
    with BuildLine() as ex8_ln:
      Polyline(*pts)
      mirror(ex8_ln.line, about=Plane.YZ)
    make_face()
  extrude(amount=L)
# show(ex8)
ln = Polyline(*pts)
ln += mirror(ln, Plane.YZ)
sk8a = make_face(Plane.YZ * ln)
ex8a = extrude(sk8a, -L).clean()
# show(ex8a)
 
l, w, h = 80.0, 60.0, 10.0
with BuildPart() as ex9:
  Box(l, w, h)
  chamfer(ex9.edges().group_by(Axis.Z)[-1], length=4)
  fillet(ex9.edges().filter_by(Axis.Z), radius=5)
# show(ex9)
ex9a = Part() + Box(l, w, h)
ex9a = chamfer(ex9a.edges().group_by(Axis.Z)[-1], length=4)
ex9a = fillet(ex9a.edges().filter_by(Axis.Z), radius=5)
# show(ex9a)

with BuildPart() as ex10:
  Box(l, w, h)
  Hole(radius=w/4)
  fillet(ex10.edges(Select.LAST).group_by(Axis.Z)[-1], radius=2)
# show(ex10)

ex10a = Part() + Box(l, w, h)
snapshot = ex10a. edges()
ex10a -= Hole(radius = w / 4, depth=h)
last_edges = ex10a.edges() - snapshot
ex10a = fillet(last_edges.group_by(Axis.Z)[-1], 2)
show(ex10a)

with BuildPart() as ex11:
  Box(l, w, h)
  chamfer(ex11.edges().group_by(Axis.Z)[-1], length=4)
  fillet(ex11.edges().filter_by(Axis.Z), radius=5)
  Hole(radius= w / 4)
  fillet(ex11.edges(Select.LAST).sort_by(Axis.Z)[-1], radius=2)
  with BuildSketch(ex11.faces().sort_by(Axis.Z)[-1]) as ex11_sk:
    with GridLocations(l / 2, w / 2, 2, 2):
      RegularPolygon(radius=5, side_count=5)
  extrude(amount=-h, mode=Mode.SUBTRACT)
# show(ex11)

l, w, h = 80.0, 60.0, 10.0
ex11a = Part() + Box(l, w, h)
ex11a = chamfer(ex11a.edges().group_by()[-1], 4)
ex11a = fillet(ex11a.edges().filter_by(Axis.Z), 5)
last = ex11a.edges()
ex11a -= Hole(radius = w / 4, depth=h)
ex11a = fillet((ex11a.edges() - last).sort_by().last, 2)
plane = Plane(ex11a.faces().sort_by().last)
polygons = Sketch() + [
  plane * loc * RegularPolygon(radius=5, side_count=5)
  for loc in GridLocations(l / 2, w / 2, 2, 2)
]
ex11a -= extrude(polygons, -h)
# show(ex11a)

w, h = 80.0, 10.0

with BuildPart() as ex28: 
  with BuildSketch() as ex28_sk:
    RegularPolygon(radius= w / 4, side_count=3)
  ex28_ex = extrude(amount=h, mode=Mode.PRIVATE)
  midfaces = ex28_ex.faces().group_by(Axis.Z)[1]
  Sphere(radius = w / 2)
  for face in midfaces:
    with Locations(face):
      Hole(h / 2)
# show(ex28) 

sk28a = RegularPolygon(radius = w / 4, side_count=3)
tmp28a = extrude(sk28a, h)
ex28a = Sphere(radius = w/2)
for p in [Plane(face) for face in tmp28a.faces().group_by(Axis.Z)[1]]:
  ex28a -= p * Hole(h/2, depth=w)
# show(ex28a)

sPnts = [ 
  (55, 30),
  (50, 35),
  (40, 30),
  (30, 20),
  (20, 25),
  (10, 20),
  (0, 20),
]
with BuildPart() as ex12:
  with BuildSketch() as ex12_sk:
    with BuildLine() as ex12_ln:
      l1 = Spline(*sPnts)
      l2 = Line((55, 30), (60, 0))
      l3 = Line((60, 0), (0, 0))
      l4 = Line((0, 0), (0, 20))
    make_face()
  extrude(amount=10)
# show(ex12)
      
l1 = Spline(*sPnts)
l2 = Line((55, 30), (60, 0))
l3 = Line((60, 0), (0, 0))
l4 = Line((0, 0), (0, 20))
sk12a = make_face([l1, l2, l3, l4])
ex12a = extrude(sk12a, 10)
# show(ex12a)

a, b = 40, 4
with BuildPart() as ex13:
  Cylinder(radius=50, height=10)
  with Locations(ex13.faces().sort_by(Axis.Z)[-1]):
    with PolarLocations(radius=a, count=4): 
      CounterSinkHole(radius=b, counter_sink_radius=2*b)
    with PolarLocations(radius=a, count=4, start_angle=45, angular_range=360):
      CounterBoreHole(radius=b, counter_bore_radius=2*b, counter_bore_depth=b)
# show(ex13)

ex13a = Cylinder(radius=50, height=10)
plane = Plane(ex13.faces().sort_by().last)
ex13a -= (
  plane
  * PolarLocations(radius=a, count=4)
  * CounterSinkHole(radius=b, counter_sink_radius=2*b, depth=10)
)
ex13a -= (
  plane
  * PolarLocations(radius=a, count=4, start_angle=45, angular_range=360)
  * CounterBoreHole(radius=b, counter_bore_radius=2*b, depth=10, counter_bore_depth=b)
)
# show(ex13a)

a, b = 40, 20
with BuildPart() as ex14:
  with BuildLine() as ex14_ln:
    l1 = JernArc(start=(0, 0), tangent=(0, 1), radius=a, arc_size=180)
    l2 = JernArc(start= l1 @ 1, tangent= l1 % 1, radius=a, arc_size=-90)
    l3 = Line(l2 @ 1, l2@1 + Vector(-a, a))
  with BuildSketch(Plane.XZ) as ex14_sk:
    Rectangle(b, b)
  sweep()
# show(ex14)

l1 = JernArc(start=(0, 0), tangent=(0, 1), radius=a, arc_size=180)
l2 = JernArc(start= l1 @ 1, tangent= l1 % 1, radius=a, arc_size=-90)
l3 = Line(l2 @ 1, l2@1 + Vector(-a, a))
ex14a_ln = l1 + l2 + l3
sk14a = Plane.XZ * Rectangle(b, b)
ex14a = sweep(sk14a, path=ex14_ln.wires()[0])
# show(ex14a)

a, b, c = 80, 40, 20
with BuildPart() as ex15:
  with BuildSketch() as ex15_sk:
    with BuildLine() as ex15_ln:
      l1 = Line((0, 0), (a, 0))
      l2 = Line((l1@1, l1@1 + Vector(0,b)))
      l3 = Line(l2@1, l2@1 + Vector(-c, 0))
      l4 = Line(l3@1, l3@1 + Vector(0, -c))
      l5 = Line(l4@1, Vector(0, (l4@1).Y))
      mirror(ex15_ln.line, about=Plane.YZ)
    make_face()
  extrude(amount=c)
# show(ex15)

l1 = Line((0, 0), (a, 0))
l2 = Line(l1 @ 1, l1 @ 1 + Vector(0, b))
l3 = Line(l2 @ 1, l2 @ 1 + Vector(-c, 0))
l4 = Line(l3 @ 1, l3 @ 1 + Vector(0, -c))
l5 = Line(l4 @ 1, Vector(0, (l4 @ 1).Y))
ln = Curve() + [l1, l2, l3, l4, l5]
ln += mirror(ln, Plane.YZ)
sk15a = make_face(ln)
ex15a = extrude(sk15a, c)
# show(ex15a)

l, w, h = 80.0, 60.0, 10.0

with BuildPart() as ex16_single:
  with BuildSketch(Plane.XZ) as ex16_sk:
    Rectangle(l, w)
    fillet(ex16_sk.vertices(), radius = l/10)
    with GridLocations(x_spacing = l / 4, y_spacing=0, x_count=3, y_count=1):
      Circle(l/12, mode=Mode.SUBTRACT)
    # alignment defaults to the center of the original sketch/plane, this moves the rectangle to be centered on the origin (top-right) corner of the original sketch
    Rectangle(l, w, align=(Align.MIN, Align.MIN), mode=Mode.SUBTRACT)
  extrude(amount = l)
# show(ex16_single)

with BuildPart() as ex16:
  add(ex16_single.part)
  mirror(ex16_single.part, about=Plane.XY.offset(w))
  mirror(ex16_single.part, about=Plane.YX.offset(w))
  mirror(ex16_single.part, about=Plane.YZ.offset(w))
  mirror(ex16_single.part, about=Plane.YZ.offset(-w))
# show(ex16)

sk16a = Rectangle(l, w)
sk16a = fillet(sk16a.vertices(), l/10)
circles = [loc * Circle(l/12) for loc in GridLocations(l/4, 0, 3, 1)]
sk16a = sk16a - circles - Rectangle(l, w, align=(Align.MIN, Align.MIN))
ex16a_single = extrude(Plane.XZ * sk16a, l)
# show(ex16a_single)
planes = [
  Plane.XY.offset(w),
  Plane.YX.offset(w),
  Plane.YZ.offset(w),
  Plane.YZ.offset(-w),
]
objs = [mirror(ex16a_single, plane) for plane in planes]
ex16a = ex16a_single + objs
# show(ex16a)

a, b = 30, 20
with BuildPart() as ex17:
  with BuildSketch() as ex17_sk: 
    RegularPolygon(radius=a, side_count=5)
  extrude(amount=b)
  mirror(ex17.part, about=Plane(ex17.faces().group_by(Axis.Y)[0][0]))
# show(ex17)

sk17a = RegularPolygon(radius=a, side_count=5)
ex17a = extrude(sk17a, amount=b)
ex17a += mirror(ex17a, Plane(ex17a.faces().sort_by(Axis.Y).first))
# show(ex17a)

l, w, h = 80.0, 60.0, 10.0
a, b = 4, 5
with BuildPart() as ex18:
  Box(l, w, h)
  chamfer(ex18.edges().group_by(Axis.Z)[-1], length=a)
  fillet(ex18.edges().filter_by(Axis.Z),radius=b)
  with BuildSketch(ex18.faces().sort_by(Axis.Z)[-1]):
    Rectangle(2 * b, 2 * b)
  extrude(amount= -h, mode=Mode.SUBTRACT)
# show(ex18)

ex18a = Part() + Box(l, w, h)
ex18a = chamfer(ex18a.edges().group_by()[-1], a)
ex18a = fillet(ex18a.edges().filter_by(Axis.Z), b)
sk18a = Plane(ex18a.faces().sort_by().first) * Rectangle(2 * b, 2 * b)
ex18a -= extrude(sk18a, -h)
# show(ex18a)

l, h = 80.0, 10.0
with BuildPart() as ex19:
  with BuildSketch() as ex19_sk19:
    RegularPolygon(radius=l/2, side_count=7)
  extrude(amount=h)
  topf = ex19.faces().sort_by(Axis.Z)[-1]
  vtx = topf.vertices().group_by(Axis.X)[-1][0]
  vtx2Axis = Axis((0, 0, 0), (-1, -0.5, 0))
  vtx2 = topf.vertices().sort_by(vtx2Axis)[-1]
  with BuildSketch(topf) as ex19_sk2:
    with Locations((vtx.X, vtx.Y), (vtx2.X, vtx2.Y)):
      Circle(radius=l/8)
  extrude(amount=-h, mode=Mode.SUBTRACT)
# show(ex19)

ex19a_sk = RegularPolygon(radius=l/2, side_count=7)
ex19a = extrude(ex19a_sk, h)
topf = ex19a.faces().sort_by().last
vtx = topf.vertices().group_by(Axis.X)[-1][0]
vtx2Axis = Axis((0, 0, 0),(-1, -0.5, 0))
vtx2 = topf.vertices().sort_by(vtx2Axis)[-1]
ex19a_sk2 = Circle(radius=l/8)
ex19a_sk2 = Pos(vtx.X, vtx.Y) * ex19a_sk2 + Pos(vtx2.X, vtx2.Y) * ex19a_sk2
ex19a -= extrude(ex19_sk2, h)
show(ex19a)

l, w, h = 80.0, 60.0, 10.0
with BuildPart() as ex20:
  Box(l, w, h)
  plane = Plane(ex20.faces().group_by(Axis.X)[0][0])
  with BuildSketch(plane.offset(2*h)):
    Circle(w/3)
  extrude(amount=w)
# show(ex20)

ex20a = Box(l, w, h)
plane = Plane(ex20.faces().group_by(Axis.X)[0][0])
sk20 = plane * Circle(w/3)
ex20a = extrude(sk20, w)

w, l = 10.0, 60.0
with BuildPart() as ex21:
  with BuildSketch() as ex21_sk:
    Circle(w/2)
  extrude(amount=l)
  with BuildSketch(Plane(origin=ex21.part.center(), z_dir=(-1, 0, 0))):
    Circle(w/2)
  extrude(amount=l)
# show(ex21)

ex21a = extrude(Circle(w/2), l)
plane = Plane(origin=ex21a.center(), z_dir=(-1, 0, 0))
ex21a += plane * extrude(Circle(w/2), l)
# show(ex21a)

l, w, h = 80.0, 60, 10.0
with BuildPart() as ex22:
  Box(l, w, h)
  pln = Plane(ex22.faces().group_by(Axis.Z)[0][0]).rotated((0, -10, 0))
  with BuildSketch(pln) as ex22_sk:
    with GridLocations(l / 4, w / 4, 2, 2):
      Circle(h/4)
  extrude(amount=-100, both=True, mode=Mode.SUBTRACT)
# show(ex22)

ex22a = Box(l, w, h)
plane = Plane((ex22a.faces().group_by(Axis.Z)[0][0])) * Rot(0, 50, 0)
holes = Sketch() + [
  plane * loc * Circle(h/4)
  for loc in GridLocations(l / 4, w / 4, 2, 2)
]
ex22a -= extrude(holes, -100, both=True)
# show(ex22a)
'''

pts = [
    (-25, 35),
    (-25, 0),
    (-20, 0),
    (-20, 5),
    (-15, 10),
    (-15, 35),
]

with BuildPart() as ex23: 
  with BuildSketch(Plane.XZ) as ex23_sk:
    with BuildLine() as ex23_ln:
      l1 = Polyline(*pts)
      l2 = Line(l1 @ 1, l1 @ 0)
    make_face()
    with Locations((0, 35)):
      Circle(25)
  #   split(bisect_by=Plane.ZY)
  # revolve(axis=Axis.Z)
# show(ex23)
show_all()




