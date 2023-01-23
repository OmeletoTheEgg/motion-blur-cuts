import bpy
import math

bl_info = {
    "name": "My Camera Info Addon",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
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

    tolerance = bpy.props.FloatProperty(name="Tolerance", default=0.1)

    def execute(self, context):
        scene = context.scene
        cam = scene.camera
        prev_pos = None
        prev_diff = None
        prev_yaw = None
        prev_pitch = None
        consecutive_cut = False
        for frame in range(scene.frame_start, scene.frame_end + 1):
            scene.frame_set(frame)
            pos = cam.matrix_world.to_translation()
            if prev_pos is not None:
                diff = (pos - prev_pos).length
                if prev_diff is not None:
                    magnitude_change = diff > prev_diff + prev_diff * self.tolerance or diff < prev_diff - prev_diff * self.tolerance
                    direction = pos - prev_pos
                    yaw = math.atan2(direction.y, direction.x)
                    pitch = math.asin(direction.z / direction.length)
                    if prev_yaw is not None and prev_pitch is not None:
                        yaw_change = abs(yaw - prev_yaw) * self.tolerance > 1
                        pitch_change = abs(pitch - prev_pitch) * self.tolerance > 1
                        if magnitude_change and (yaw_change or pitch_change):
                            self.report({'INFO'}, f'Frame: {frame} Camera Position: {pos} Magnitude Difference: {diff} Yaw: {yaw} Pitch: {pitch} Cut')
                            if not consecutive_cut:
                                consecutive_cut = True
                                context.scene.cycles.motion_blur_position = "START"
                                scene.keyframe_insert(data_path="cycles.motion_blur_position", frame=frame, keyframe_type='CONSTANT')
                                context.scene.cycles.motion_blur_position = "END"
                                scene.keyframe_insert(data_path="cycles.motion_blur_position", frame=frame-1, keyframe_type='CONSTANT')
                                scene.keyframe_insert(data_path="cycles.motion_blur_position", frame=frame+1, keyframe_type='CONSTANT')
                        else:
                            consecutive_cut = False
                    prev_yaw = yaw
                    prev_pitch = pitch
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
