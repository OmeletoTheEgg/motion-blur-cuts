import bpy

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
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        cam = context.scene.camera
        pos = cam.matrix_world.to_translation()
        rot = cam.matrix_world.to_euler()
        self.report({'INFO'}, f'Camera Position: {pos} Rotation: {rot}')
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
