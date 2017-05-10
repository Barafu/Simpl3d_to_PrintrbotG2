# Simplify3D to PrintrbotG2 converter
A simple script to convert GCODE produced by Simplify3D and other slicers to a dialect thatis used by g2core based Printbot G2 board.
# Warning
The probing process snippet uses hard-coded coordinates. The default one assumes you have Printrbot Simple with upgraded table. For other printrbots, edit `start/40-probe.gcode` to insert proper probing coordinates. 
# How to use
First, set up your Simplify3D profile. On the `Other` tab, set `XY Axis movement speed` to 777mm/min. That is a *magic value* that will indicate that movement should be replaced by G0 command. On the `G-code` tab, untic every option on the left except `5D firmware` that should be on. On the scripts tab, set start script to a single line 

    ;SIMPL_START
and the end script to 

    ;SIMPL_END
You may add other commands too if you are sure they are g2core-compatible. A better way would be to create a snippet in the `start` folder. 
```
python3 transform.py input.gcode output.gcode
```
Then send the result gcode to printer. To tune the process, edit the snippet files in `start` and `fin` folders. 
# Future plans
This project will not be developed anymore because Printrbot G2 boards are being shipped with Marlin compatibility mode now, so tools like Octoprint should just work. 
