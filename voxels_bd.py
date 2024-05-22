import random
import os

# import cadquery as cq
# from build123d import *
from build123d import (
  BuildPart, 
  BuildLine, 
  BuildSketch, 
  Box, 
  Mode,
  Axis,
  extrude,
  Location,
  Circle,
  Line,
  RadiusArc,
  Text, 
  make_face,
  RigidJoint,
  Compound, 
)
from ocp_vscode import show

## TODO
# 1. Add build123d code for hook
# 1. Add argument to export function to specify .STEP or .STL
# 1. Change from star imports to individual component imports

### Functions ###


def create_voxel(s_i, d_i, t_b, t_c, h_c, i):
  """
  Creates a voxel based on given parameters.

  :param s_i: Side length of the inside of the hollow cube.
  :type s_i: float
  :param d_i: Inside diameter of plug cylinder, "cut".
  :type d_i: float
  :param t_b: Box wall 3DP wall thickness.
  :type t_b: float
  :param t_c: Cylinder wall 3DP thickness.
  :type t_c: float
  :param h_c: Distance from inside cube that the cylinder extends.
  :type h_c: float
  :param i: Index number to label the voxel.
  :type i: int
  :return: A voxel assembly including the voxel and a hook.
  :rtype: Compound
  """
  # derived parameters
  d_i_p = d_i  # diameter of inside cylinder on plug
  r_i_p = d_i_p / 2  # radius of inside cylinder on plug
  # r_o_p = r_i_p + t_c  # radius of outside cylinder on plug
  # r_i_s = r_o_p                                     # radius of inside cylinder on socket
  # r_o_s = r_i_s + t_c                               # radius of outside cylinder on socket
  r_i_s = r_i_p
  # r_o_s = r_o_p
  s_o = s_i + (2 * t_b)  # side length of cube on inside
  # h_c_a = h_c - t_b  # actual cylinder height

  with BuildPart() as voxel:
    voxel.label = f"Part_{i}"
    # Construct the hollow cube
    Box(s_o, s_o, s_o)
    Box(s_i, s_i, s_i, mode=Mode.SUBTRACT)

    # Identify the front, back, and top faces of the cube
    front_face = voxel.faces().sort_by(Axis.Z).first
    back_face = voxel.faces().sort_by(Axis.Z).last
    # top_face = voxel.faces().group_by(Axis.Y)[-1]

    # Create hole on the front face
    with BuildSketch(front_face) as plug_hol_sk:
      Circle(r_i_p)
    extrude(amount=-t_b, mode=Mode.SUBTRACT)

    # Create cylinder on front face
    # with BuildSketch(front_face) as plug_cyl_sk:
    #     Circle(r_o_p)
    #     Circle(r_i_p, mode=Mode.SUBTRACT)
    # extrude(amount=h_c_a)

    # Create hole on the back face
    with BuildSketch(back_face) as sock_hol_sk:
      Circle(r_i_s)
      
    extrude(amount=-t_b, mode=Mode.SUBTRACT)

    # Create cylinder on the front face
    # with BuildSketch(back_face) as sock_cyl_sk:
    #     Circle(r_o_s)
    #     Circle(r_i_s, mode=Mode.SUBTRACT)
    # extrude(amount= h_c_a)

    with BuildSketch(
      Location(((s_i / 2) - 7.5, (s_o / 2), (s_i / 2) + 2.5), (270, 0, 0))
    ) as label_sk:
      Text(str(i), font_size=10, align=(0, 0))
      # Location(top_face[0].center(), (100, 100, 0))
    extrude(amount=2)
    
    # with BuildPart() as front_tube:
    #   with BuildSketch(Location(front_face.center().add((-1, 4.9, 0)), (0,0,0))) as sketch:
    #     with BuildLine() as line:
    #       l1 = Line((0, 0), (0, 2.101))
    #       l2 = Line((0, 2.101), (2.101, 2.101))
    #       l3 = Line((2.101, 2.101), (2.101, 0))
    #       # l4 = Line((2, 0), (0, 0))
    #       # l5 = ThreePointArc(l1 @ 0, (-10, -10), l3 @ 1)
    #       l5 = RadiusArc(l1 @ 0, l3@ 1, 5, False )
    #     make_face()
    #   extrude(amount=-20, mode=Mode.ADD)
      
    # with BuildPart() as back_tube:
    #   with BuildSketch(Location(back_face.center().add((-1, 4.9, 0)), (0,0,0))) as sketch:
    #     with BuildLine() as line:
    #       l6 = Line((0, 0), (0, 2.101))
    #       l7 = Line((0, 2.101), (2.101, 2.101))
    #       l8 = Line((2.101, 2.101), (2.101, 0))
    #       # l9 = Line((2, 0), (0, 0))
    #       # l10 = ThreePointArc(l1 @ 0, (-10, -10), l3 @ 1)
    #       l11= RadiusArc(l6 @ 0, l8@ 1, 5, False )
    #     make_face()
    #   extrude(amount=-20, mode=Mode.ADD)
  
  # # Identify the front, back, and top faces of the cube

  # top_face = part.faces().group_by(Axis.Y)[-1]
  # top_face = part.faces().sort_by(Axis.Y).first
  # tube_front_face = tube.faces().sort_by(Axis.Z).first
  

  # # Create hole on the front face
  # # with BuildSketch(Location((1, -4.9, 0), (180, 0, 0))) as hole:
  # with BuildSketch(Location(tube_front_face.center(), (0, 0, 0))) as hole:
  #   Circle(2.5)
  # extrude(amount=-20, mode=Mode.SUBTRACT)

    # Create the voxel side joint for hook mounting
  #   RigidJoint(
  #     "hook_mount_voxel",
  #     voxel,
  #     Location(top_face[0].center(), (0, 0, 0)),
  #   )

  #   # Create the voxel side joints for tube mounting
  #   RigidJoint(
  #     "tube_front_mount_voxel",
  #     voxel,
  #     Location(front_face.center(), (0, 0, 0)),
  #   )
    
  #   RigidJoint(
  #       "tube_back_mount_voxel",
  #       voxel,
  #       Location(back_face.center(), (0, 0, 0)),
  #   )

  # # with BuildPart() as hook:
  # #   cd = os.path.dirname(
  # #     os.path.realpath(__file__)
  # #   )  # Get the current directory of the script
  # #   hook_path = os.path.join(cd, "hook.STEP")
  # #   hook = import_step(hook_path)
  # #   bottom_face = voxel.faces().group_by(Axis.Y)[
  # #     -3
  # #   ]  # Identify the bottom face of the voxel for hook placement
  # #   # Create the hook side joint for hook mounting
  # #   RigidJoint("hook_mount_hook", hook, Location((0, 0, 0), (0, 90, 0)))

  # #   # create labels for the assembly components
  # #   voxel.label = "i"
  # #   hook.label = "hook"

  # #   # Connect the hook to the voxel using the joints
  # #   hook.joints["hook_mount_hook"].connect_to(voxel.joints["hook_mount_voxel"])


  # with BuildPart() as front_tube:
  #   cd = os.path.dirname(
  #     os.path.realpath(__file__)
  #   )  # Get the current directory of the script
  #   tube_path_1 = os.path.join(cd, "tube.STEP")
  #   front_tube = import_step(tube_path_1)
    
  #   # bottom_face = voxel.faces().group_by(Axis.Y)[
  #   #   -3
  #   # ]  # Identify the bottom face of the voxel for hook placement
  #   # Create the hook side joint for hook mounting
  #   RigidJoint("tube_front_mount_tube", front_tube, Location((0, 0, 0), (180, 0, 180)))

  #   # create labels for the assembly components
  #   voxel.label = "voxel"
  #   # hook.label = "hook"
  #   front_tube.label = "front_tube"

  #   # Connect the hook to the voxel using the joints
  #   front_tube.joints["tube_front_mount_tube"].connect_to(voxel.joints["tube_front_mount_voxel"])
    
  
  # with BuildPart() as back_tube:
  #   cd = os.path.dirname(
  #     os.path.realpath(__file__)
  #   )  # Get the current directory of the script
  #   tube_path_2 = os.path.join(cd, "tube_2.STEP")
  #   back_tube = import_step(tube_path_2)
    
  #   # bottom_face = voxel.faces().group_by(Axis.Y)[
  #   #   -3
  #   # ]  # Identify the bottom face of the voxel for hook placement
  #   # Create the hook side joint for hook mounting
  #   RigidJoint("tube_back_mount_tube", back_tube, Location((0, 0, 0), (0, 0, 0)))

  #   # create labels for the assembly components
  #   voxel.label = "voxel"
  #   # hook.label = "hook"
  #   back_tube.label = "back_tube"

  #   # Connect the hook to the voxel using the joints
  #   back_tube.joints["tube_back_mount_tube"].connect_to(voxel.joints["tube_back_mount_voxel"])
  
  # with BuildPart() as tubes:
  #   cd = os.path.dirname(
  #     os.path.realpath(__file__)
  #   )  # Get the current directory of the script
  #   tube_path = os.path.join(cd, "tube.STEP")
  #   front_tube = import_step(tube_path)
  #   back_tube = import_step(tube_path)
    
  #   # bottom_face = voxel.faces().group_by(Axis.Y)[
  #   #   -3
  #   # ]  # Identify the bottom face of the voxel for hook placement
  #   # Create the hook side joint for hook mounting
    
  #   RigidJoint("tube_front_mount_tube", front_tube, Location((50, 0, 0), (0, 0, 0)))
  #   RigidJoint("tube_back_mount_tube", back_tube, Location((0, 0, 0), (0, 0, 0)))

  #   # create labels for the assembly components
  #   voxel.label = "voxel"
  #   # hook.label = "hook"
  #   front_tube.label = "front_tube"
  #   back_tube.label = "back_tube"

  #   # Connect the hook to the voxel using the joints
  #   front_tube.joints["tube_front_mount_tube"].connect_to(voxel.joints["tube_front_mount_voxel"])  
  #   back_tube.joints["tube_back_mount_tube"].connect_to(voxel.joints["tube_back_mount_voxel"])  
    
    
  # # voxel_assy = Compound(label=f"voxel_{i}", children=[voxel.part, hook])
  # # voxel_assy = Compound(label=f"voxel_new", children=[voxel.part, front_tube])
  # # voxel_assy = Compound(label=f"voxel_{i}", children=[voxel.part, front_tube, back_tube])
  # # voxel_assy_2 = Compound(label=f"voxel_new2", children=[voxel_assy, front_tube])
  # voxel_assy = Compound(label=f"voxel_new", children=[voxel.part, tubes.part])

  
  # show(voxel_assy)
  # return voxel_assy
  # show(voxel_assy_2)
  # return voxel_assy_2
  show(voxel)
  return voxel
  
  

def export_assy(assy):
  """
  Exports the voxel in both STEP and STL format.

  :param voxel: The voxel assembly to be exported.
  :type voxel: Compound
  :param path: The directory path to save the exported files.
  :type path: str
  :param cd: The current directory of the script.
  :type cd: str
  """
  cd = os.path.dirname(
    os.path.realpath(__file__)
  )  # Get the current directory of the script
  i = assy.label
  print(f"Exporting {i} to {cd}/cad_files/")
  filename_STEP = f"{cd}/cad_files/{assy.label}.STEP"
  # export_step(assy, filename_STEP)
  assy.export_step(filename_STEP)  # Export the voxel as a .STEP file
  filename_STL = f"{cd}/cad_files/{assy.label}.STL"
  assy.export_stl(filename_STL)  # Export the voxel as an .STL file


def create_voxels(s_i, d_i, t_b, t_c, h_c):
  """
  Creates and exports a series of voxels based on the given parameters and a list of s_i values.

  :param s_i: Side length of the inside of the hollow cube.
  :type s_i: float
  :param d_i: Inside diameter of plug cylinder, "cut".
  :type d_i: float
  :param t_b: Box wall 3DP wall thickness.
  :type t_b: float
  :param t_c: Cylinder wall 3DP thickness.
  :type t_c: float
  :param h_c: Distance from inside cube that the cylinder extends.
  :type h_c: float
  :param cd: The current directory of the script.
  :type cd: str
  """

  cd = os.path.dirname(
    os.path.realpath(__file__)
  )  # Get the current directory of the script
  i = 1
  us = [5.5, 7.5, 10, 12.5, 15, 17.5, 20, 21.5, 22.5, 25, 27.5, 40, 50, 75, 100]
  for s_i in us:
    # Create the voxel
    voxel = create_voxel(s_i, d_i, t_b, t_c, h_c, i)
    export_assy(voxel)
    # filename = f"{cd}//voxel_{s_i}.STL"
    # voxel.export_step(filename)                                   # Export the voxel as a .STEP file
    # voxel.export_stl(filename)                                    # Export the voxel as an .STL file
    show(voxel)
    i += 1


def connect_voxels(voxel_1, voxel_2):
  voxel_1_plug_face = voxel_1.faces().group_by(Axis.X)[
    -1
  ]  # Identify the front, back, and top faces of the cube
  voxel_2_socket_face = voxel_2.faces().group_by(Axis.X)[
    2
  ]  # back_face = voxel_1.faces().sort_by(Axis.Z).last

  # Create the voxel 1 plug joint for hook mounting
  RigidJoint(
    "voxel_1_plug",
    voxel_1,
    Location(voxel_1_plug_face[0].center(), (0, 0, 0)),
  )

  # Create the voxel 2 socket joint for hook mounting
  RigidJoint(
    "voxel_2_socket",
    voxel_2,
    Location(voxel_2_socket_face[0].center(), (0, 0, 0)),
  )

  # mate the plug and socket joints into an assembly
  voxel_1.joints["voxel_1_plug"].connect_to(voxel_2.joints["voxel_2_socket"])
  voxels_assy = Compound(label=f"voxels_assy", children=[voxel_1, voxel_2])

  show(voxels_assy)
  return voxels_assy


def chain_voxels_recursive(n, prev_voxel=None, counter=1, path=None):
  """
  Recursively chain n voxels together.

  :param n: Number of voxels left to create and chain.
  :type n: int
  :param prev_voxel: The previous voxel to which the new voxel will be chained.
  :type prev_voxel: Compound or None
  :param counter: The current counter for the voxel creation (used for labeling).
  :type counter: int
  :param path: The directory path to save the exported files.
  :type path: str
  :return: The assembly of the chained voxels.
  :rtype: Compound or None
  """
  if n == 0:
    return prev_voxel

  s_i = random.uniform(5.5, 100)  # Randomly generate s_i between 5.5 and 100 mm
  voxel = create_voxel(s_i, d_i, t_b, t_c, h_c, counter)
  export_assy(voxel)

  if prev_voxel:
    voxels_assy = connect_voxels(prev_voxel, voxel)
    export_assy(voxels_assy)
  else:
    voxels_assy = (
      voxel  # If it's the first voxel, there's no previous voxel to connect to.
    )

  return chain_voxels_recursive(n - 1, voxels_assy, counter + 1, path)


### Parameters ###
s_i = 30  # side length of the inside of the hollow cube
d_i = 5  # inside diameter of plug cylinder, "cut"
t_b = 5  # box wall 3DP wall thickness
t_c = 2.5  # cylinder wall 3DP thickness
h_c = (
  20 + t_b
)  # distance from inside cube that the cylinder extends (includes box wall thickness)
# h_c_a = h_c - t_b                                              # actual cylinder height from outside wall


### Function calls ###

### single test voxel
voxel_1 = create_voxel(
  s_i, d_i, t_b, t_c, h_c, 1
)  # creates cad model of voxel with build123d
# export_assy(
#   voxel_1
# )  # exports build123d assy to .STEP and .STL, each individual voxel is an assembly of the voxel and hook
# show(voxel_1)  # displays the voxel in the viewer

### creates and exports a series of voxels
# create_voxels(s_i, d_i, t_b, t_c, h_c)

### creates and exports a 2 voxel assembly ###
# voxel_2 = create_voxel(s_i, d_i, t_b, t_c, h_c, 1)            # creates cad model of voxel with build123d
# voxel_3 = create_voxel(s_i, d_i, t_b, t_c, h_c, 2)            # creates cad model of voxel with build123d
# voxels_assy = connect_voxels(voxel_2, voxel_3)
# export_assy(voxels_assy)

### recursive voxel assembly builder
# num_voxels = 10
# final_assy = chain_voxels_recursive(num_voxels)
