# Buoyancy Simulator for AirshipACE

The idea is for this to be the quick-make prototype in Python of certain mechanics that may be hard to work out on the Amiga given its weird toolchain and limitations. This will slowly expand to include all the airship mechanics so I have a godbook to use when implementing in the amiga version and what I can cut if needed.

Currently, under tablesim.py the code is successfully replicating a simple International Standard Atmosphere.

It now integrates drag into its force calculations but the airship doesn't 'feel' quite right. It's not losing enough energy when traveling around as quickly as I would have thought, particularly in the Y-axis movement, it can oscillate between 0-1083m for a lot longer than I thought possible with drag acting on it.

It's more than enough for AirshipACE purposes so anything further would be more for curiosity than anything.

Under the default figures the airship likes to hover around the 600m range. 

## Controls ##
Up Arrow - Increase Y-axis velocity
Down Arrow - Decrease Y-axis velocity
Left Arrow - Increase  X-Axis Velocity
Right Arrow - Decrease X-Axis Velocity
