print("Complete Folder damage check?\n******Warning******\nThis test may result in low preformance and in some cases may slow down this device. This test imports all files in this package.")
try:
	from GameWidgets.GameWidgets import *
	print("GameWidgets.GameWidgets Test Succsess")
except:
	print("GameWidgets.GameWidgets has an error inside it.")
try:
	from GameWidgets.SetUp import *
	print("GameWidgets.SetUp Test Succsess")
except:
	print("GameWidgets.SetUp has an error inside it.")
try:
	from GameWidgets.Widgets import *
	print("GameWidgets.Widgets Test Succsess")
except:
	print("GameWidgets.Widgets has an error inside it.")
try:
	from GameWidgets.Engine import *
	print("GameWidgets.Engine Test Succsess")
except:
	print("GameWidgets.Engine has an error inside it. ")
try:
	from GameWidgets.Engine.Special import *
	print("GameWidgets.Engine.Special Test Succsess")
except:
	print("GameWidgets.Engine.Special has an error inside it.")
try:
	from GameWidgets.Engine.PhysicsLib import *
	print("GameWidgets.Engine.PhysicsLib Test Succsess")
except:
	print("GameWidgets.Engine.PhysicsLib has an error inside it.")
try:
	from GameWidgets.Engine.PhysicsLib.PhysicsConfig import *
	print("GameWidgets.Engine.PhysicsLib.PhysicsConfig Test Succsess")
except:
	print("GameWidgets.Engine.PhysicsLib.PhysicsConfig has an error inside it.")
try:
	from GameWidgets.Engine.PhysicsLib.PhysicsObjects import *
	print("GameWidgets.Engine.PhysicsLib.PhysicsObject Test Succsess")
except:
	print("GameWidgets.Engine.PhysicsLib.PhysicsObject has an error inside it.")
try:
	from GameWidgets.Tools import *
	print("GameWidgets.Tools Test Succsess")
except:
	print("GameWidgets.Tools has an error inside it.")