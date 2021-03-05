bl_info = {
    "name": "GEN Photometric Camera",
    "blender": (2, 80, 0),
    "category": "Camera",
}

import bpy

def genISO_EVset (context):
    C = context
    scene = context.scene
    scene.camera.data['ISO'] = 400
    scene.camera.data['EV'] = 0.0
    return {'FINISHED'}

def genSetCamera (context):
    C = context

    scene = context.scene

    C.scene.view_settings.driver_remove('exposure')
    myfcurve = C.scene.view_settings.driver_add('exposure')

    driver = myfcurve.driver
                
    # aperture
    var = driver.variables.new()
    var.type = 'SINGLE_PROP'
    var.name = "aperture"
    # variables have one or two targets 
    target = var.targets[0]
    target.id_type = 'CAMERA'
    target.id = C.scene.camera.data.id_data
    target.data_path = "dof.aperture_fstop"

    # speed
    var = driver.variables.new()
    var.type = 'SINGLE_PROP'
    var.name = "speed"
    # variables have one or two targets 
    target = var.targets[0]
    target.id_type = 'SCENE'
    target.id = C.scene.id_data
    target.data_path = "render.motion_blur_shutter"

    # fps
    var = driver.variables.new()
    var.type = 'SINGLE_PROP'
    var.name = "fps"
    # variables have one or two targets 
    target = var.targets[0]
    target.id_type = 'SCENE'
    target.id = C.scene.id_data
    target.data_path = "render.fps"

    # ISO
    var = driver.variables.new()
    var.type = 'SINGLE_PROP'
    var.name = "iso"
    # variables have one or two targets 
    target = var.targets[0]
    target.id_type = 'CAMERA'
    target.id = C.scene.camera.data.id_data
    target.data_path = '["ISO"]'
    
    # EV
    var = driver.variables.new()
    var.type = 'SINGLE_PROP'
    var.name = "ev"
    # variables have one or two targets 
    target = var.targets[0]
    target.id_type = 'CAMERA'
    target.id = C.scene.camera.data.id_data
    target.data_path = '["EV"]'

    driver.expression = "log (( 1/aperture ) ** 2 / (1/(1/fps * speed) )   , 2)  + log (iso) + ev + 2.564"

    return {'FINISHED'}
    
    
class SetupGenCam(bpy.types.Operator):
    """Links the exposure of the active camera to the aperture, speed, ISO, and EV values following real world formulas"""
    bl_idname = "render.setup_gencam"
    bl_label = "Set up the Gen cam"

    @classmethod
    def poll(cls, context):
        return context.scene is not None 

    def execute(self, context):
        genISO_EVset (context)
        genSetCamera(context)
        
        context.scene.camera.data.dof.aperture_fstop = 2.8

        return {'FINISHED'}


class genCamPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the gen cam addon"""
    bl_label = "gen Cam"
    bl_idname = "SCENE_PT_gencam"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = "gen CAM"
    bl_options = {'HEADER_LAYOUT_EXPAND'} 
    

    def draw(self, context):

        layout = self.layout
        layout.use_property_split = True

        scene = context.scene

        # Different sizes in a row
        layout.label(text="Set camera Exposure:")
        row = layout.row(align=True)
        #row.operator("render.render") 
        row.operator("render.setup_gencam")
        # Create a simple row.
        layout.label(text=scene.camera.name)
        
        col = layout.column()
        col.prop(scene.camera.data.dof, "aperture_fstop" )
        col.prop(scene.render, "motion_blur_shutter")
        col.prop(scene.camera.data, '["ISO"]' )
        col.prop(scene.camera.data, '["EV"]' )

        col.prop(scene.view_settings, "view_transform" )

def register():
    bpy.utils.register_class(SetupGenCam)
    bpy.utils.register_class(genCamPanel)
    


def unregister():
    bpy.utils.unregister_class(SetupGenCam)
    bpy.utils.unregister_class(genCamPanel)
    


if __name__ == "__main__":
    genISO_EVset (context)
    register()
