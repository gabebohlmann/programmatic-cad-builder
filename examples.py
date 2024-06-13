from build123d import *
from ocp_vscode import show

'''

# Create a box with holes on each face
with BuildPart() as custom_box:
    Box(100, 100, 100)
    with GridLocations(25, 25, 4, 4):
        Hole(10)
# show(custom_box.part)

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

'''
       







