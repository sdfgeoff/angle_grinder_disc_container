import os
import sys
import traceback
import argparse
try:
    import bpy
    IN_BLENDER = True
except ImportError:
    IN_BLENDER = False

SCRIPT_FILE = os.path.abspath(__file__)
SCRIPT_FOLDER = os.path.dirname(SCRIPT_FILE)

BLEND_FILE = os.path.join(SCRIPT_FOLDER, "AngleGrinderDiscCase.blend")
EXPORT_FOLDER = os.path.join(SCRIPT_FOLDER, "AngleGrinderDiscCase")
PARAMETER_OBJECT = "Parameters"

PARAMETER_OPTIONS = {
    "115x20": {"disc_diameter": 115, "container_height": 20, "circle_resolution": 64},
    "115x40": {"disc_diameter": 115, "container_height": 40, "circle_resolution": 64},
    "115x60": {"disc_diameter": 115, "container_height": 60, "circle_resolution": 64},
    "125x20": {"disc_diameter": 125, "container_height": 20, "circle_resolution": 64},
    "125x40": {"disc_diameter": 125, "container_height": 60, "circle_resolution": 64},
    "125x60": {"disc_diameter": 125, "container_height": 60, "circle_resolution": 64},
    "150x40": {"disc_diameter": 150, "container_height": 40, "circle_resolution": 64},
}




def export(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-folder', help="Output all data to here", required=True)
    config = parser.parse_args(args)
    
    for parameter_key in PARAMETER_OPTIONS:
        settings = PARAMETER_OPTIONS[parameter_key]
        
        # Set the parameters
        for setting_key in settings:
            bpy.data.objects[PARAMETER_OBJECT][setting_key] = settings[setting_key]
        
        # update the scene
        bpy.data.objects[PARAMETER_OBJECT].update_tag()
        
        stls = [obj for obj in bpy.data.objects if obj.name.endswith(".stl")]
        
        for stl in stls:
            
            # Ensure we select only the object we want
            for obj in bpy.data.objects:
                obj.select_set(obj == stl)
            
            output_name = parameter_key + "_" + stl.name
            output_path = os.path.join(config.output_folder, output_name)
            if not os.path.exists(config.output_folder):
                os.makedirs(config.output_folder)
            
            bpy.ops.export_mesh.stl(
                filepath=output_path,
                check_existing=False,
                filter_glob='*.stl',
                use_selection=True,
                global_scale=1.0,
                use_scene_unit=False,
                ascii=False,
                use_mesh_modifiers=True,
                batch_mode='OFF',
                axis_forward='Y',
                axis_up='Z'
            )
    

def run_function_with_args(function):
    arg_pos = sys.argv.index('--') + 1
    try:
        function(sys.argv[arg_pos:])
    except:
        print("ERROR")
        traceback.print_exc()
        sys.exit(1)

    print("SUCCESS")
    sys.exit(0)


if __name__ == "__main__":
    if IN_BLENDER:
        run_function_with_args(export)
    else:
        command = "blender -b {} --python {} -- --output-folder {}".format(BLEND_FILE, SCRIPT_FILE, EXPORT_FOLDER)
        print(command)
        assert os.system(command) == 0
    
