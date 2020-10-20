import PySimpleGUI as sg
from pathlib import Path

START_SCRIPT=""";start script
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

END_SCRIPT = """;end script
M107 ; turn fan off
M104 S0 T1 ; cool left extruder
M104 S0 T0 ; cool right extruder
M140 S0 ; cool build plate
G1 Z150 F900 ; lower build plate
G28 X Y ; home XY axes
M84 ; disable motors"""

def index_startswith(lines, s, rev=False):
    index = [i for i, line in enumerate(lines) if line.startswith(s)]
    if rev:
        return index[-1]
    else:
        return index[0]

def translate(gcode):
    gcode = Path(gcode)
    parent = gcode.parent
    
    with open(gcode) as f:
        lines = f.readlines()

    start_index = index_startswith(lines, "G21")
    end_index = index_startswith(lines, ";skirt") + 1
    lines[start_index:end_index] = START_SCRIPT.split("\n")

    start_index = index_startswith(lines, "M107", rev=True)
    end_index = None
    lines[start_index:end_index] = END_SCRIPT.split("\n")
    
    new_gcode = parent / Path(gcode.stem + "-xpro.gcode")
    with open(new_gcode, "w") as f:
        for line in lines:
            f.write(f"{line.strip()}\n")
    
def main():
    filenames = sg.popup_get_file("Select Gcode File", file_types=(("Gcode Files", "*.gcode"),), multiple_files=True)
    
    if filenames is None:
        filenames = []
    elif isinstance(filenames, str):
        filenames = filenames.split(";")
    
    for gcode in filenames:
        try:
            translate(gcode)
        except Exception as e:
            print(f"Error occured while processing {gcode}")
            print(f"{e.__class__} {e}")

        else:
            print(f"Successfully translated {gcode}.")

        
        
if __name__ == "__main__":
    main()