import bpy
from mathutils import Vector
import math

bl_info = {
    "name": "My Camera Info Addon",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (3, 4, 0),
    "location": "View3D",
    "description": "Displays the position and rotation of the camera in the scene",
    "warning": "",
    "doc_url": "",
    "category": "Object"
}

class GenerateKeyframeOperator(bpy.types.Operator):
    """Generate Keyframe on Cuts"""
    bl_idname = "object.generate_keyframe"
    bl_label = "Generate Keyframe on Cuts"

    tolerance_magnitude : bpy.props.FloatProperty(name="Magnitude Tolerance", default=1.0)
    tolerance_angle : bpy.props.FloatProperty(name="Angle Tolerance", default= math.pi * 3/4)

    def execute(self, context):
        scene = context.scene
        cam = scene.camera
        prev_pos = None
        prev_diff = None
        prev_direction = None
        consecutive_cut = False
        for frame in range(scene.frame_start, scene.frame_end + 1):
            scene.frame_set(frame)
            pos = cam.matrix_world.to_translation()
            if prev_pos is not None:
                diff = (pos - prev_pos).length
                direction = pos - prev_pos
                if prev_diff is not None:
                    magnitude_change = diff > (prev_diff + (prev_diff * self.tolerance_magnitude)) or diff < (prev_diff - (prev_diff * self.tolerance_magnitude))
                    if prev_direction is not None:
                        angle_change = direction.dot(prev_direction) < self.tolerance_angle
                        if magnitude_change and angle_change:
                            self.report({'INFO'}, f'Frame: {frame} Camera Position: {pos} Magnitude Difference: {diff} Angle Change: {angle_change} Cut')
                            if not consecutive_cut:
                                consecutive_cut = True
                                context.scene.cycles.motion_blur_position = "START"
                                scene.keyframe_insert(data_path="cycles.motion_blur_position", frame=frame)
                                context.scene.cycles.motion_blur_position = "END"
                                scene.keyframe_insert(data_path="cycles.motion_blur_position", frame=frame-1)
                                scene.keyframe_insert(data_path="cycles.motion_blur_position", frame=frame+1)
                        else:
                            consecutive_cut = False
                    prev_direction = direction
                prev_diff = diff
            prev_pos = pos
        return {'FINISHED'}


class MyCameraPanel(bpy.types.Panel):
    """Creates a Panel in the Camera properties window"""
    bl_label = "My Camera Panel"
    bl_idname = "OBJECT_PT_my_camera_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_category = "Camera"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.generate_keyframe", text="Generate Keyframe on Cuts")

def register():
    bpy.utils.register_class(GenerateKeyframeOperator)
    bpy.utils.register_class(MyCameraPanel)

def unregister():
    bpy.utils.unregister_class(GenerateKeyframeOperator)
    bpy.utils.unregister_class(MyCameraPanel)

if __name__ == "__main__":
    register()
