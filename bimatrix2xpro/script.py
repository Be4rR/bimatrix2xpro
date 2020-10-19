import PySimpleGUI as sg
from pathlib import Path

REPLACE_START=""";start script
G90
M82
M106 S0
M140 S60
M190 S60
M104 S215 T0
M104 S215 T1
M109 S215 T0
M109 S215 T1
G28 ; home all axes
T0 ; switch to right extruder
G1 X0 Y0 F3600 ; move to wait position
G92 A0 B0 ; zero independent axes
G92 E0 ; zero extruder
G1 Y3 Z0.3 F3600 ; prepare to purge
G1 X230 E18 F2400 ; purge
G92 E0 ; zero extruder
T1 ; switch to left extruder
G92 E0 ; zero extruder
G1 X0 Y4 F3600 ; prepare to purge
G1 X230 E18 F2400 ; purge"""

REPLACE_END = """;end script
M107 ; turn fan off
M104 S0 T1 ; cool left extruder
M104 S0 T0 ; cool right extruder
M140 S0 ; cool build plate
G1 Z150 F900 ; lower build plate
G28 X Y ; home XY axes
M84 ; disable motors"""

def index_startswith(lines, s, rev=False):
    if rev:
        return [i for i, line in enumerate(lines) if line.startswith(s)][-1]
    else:
        return [i for i, line in enumerate(lines) if line.startswith(s)][0]

def main():
    if gcode := sg.popup_get_file("Select Gcode File", file_types=(("Gcode Files", "*.gcode"),),):
        gcode = Path(gcode)
        parent = gcode.parent
        
        try:
            with open(gcode) as f:
                lines = f.readlines()
        except:
            print("Can't open file.")
            

        start = index_startswith(lines, "G21")
        end = index_startswith(lines, ";skirt") + 1
            
            
        
        rstart = REPLACE_START.split("\n")
        rend = REPLACE_END.split("\n")
        
        lines[start:end] = rstart
        
        end_start = index_startswith(lines, "M107", rev=True)
        lines[end_start:] = rend
        
        new_gcode = parent / Path(gcode.stem + "-xpro.gcode")
        with open(new_gcode, "w") as f:
            for line in lines:
                f.write(f"{line.strip()}\n")
        
        sg.popup("Successfully translated!")
        
if __name__ == "__main__":
    main()