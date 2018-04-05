#!/usr/bin/env python

from gimpfu import *

def watermark_from_svg(image, drawable, in_file_name, in_watermark_width, in_watermark_margin, in_placement, in_opacity, in_invert):
    gimp.context_push()
    image.undo_group_start()
    
    
    water = pdb.gimp_file_load_layer(image, in_file_name)    
    pdb.gimp_image_insert_layer(image, water, None, -1)
    
    pdb.gimp_item_set_name(water, "SVG watermark")
    pdb.gimp_layer_set_opacity(water, in_opacity)
    
    pdb.gimp_context_set_interpolation(INTERPOLATION_LANCZOS)
    water_new_width = int(image.width * (in_watermark_width / 100))
    water_new_height = int(water_new_width * water.height / water.width)    
    pdb.gimp_item_transform_scale(water, 0,0,water_new_width,water_new_height)
    
    img_space_x = int(image.width * (in_watermark_margin / 100))
    img_space_y = int(image.height * (in_watermark_margin / 100))
    if in_placement==0:
        water_space_x = img_space_x
        water_space_y = img_space_y
    elif in_placement==1:
        water_space_x = image.width - (img_space_x + water.width)
        water_space_y = img_space_y
    elif in_placement==2:
        water_space_x = img_space_x
        water_space_y = image.height - (img_space_y + water.height)
    elif in_placement==3:
        water_space_x = image.width - (img_space_x + water.width)
        water_space_y = image.height - (img_space_y + water.height)
        
    pdb.gimp_layer_set_offsets(water, water_space_x, water_space_y)
    
    if in_invert:
        pdb.gimp_invert(water)
    
    image.undo_group_end()
    gimp.displays_flush()
    gimp.context_pop()

    return

register(
    "watermark_from_svg",    
    "Watermark file with SVG",   
    "Watermark file with SVG",
    "Krzysztof Blachnicki", 
    "krzysiu.net", 
    "Novermber 2016",
    "<Image>/Filters/Krzysiu/Watermark file with SVG...", 
    "*", 
    [
        (PF_FILE, "in_file_name", "Watermark file:", "C:\watermark-image-default.svg"),
        (PF_SPINNER, "in_watermark_width", "Watermark width (% of image):", 20, (1, 100, 1)),
        (PF_SPINNER, "in_watermark_margin", "Margin (% of image):", 1, (0, 50, 1)),
        (PF_OPTION, "in_placement", "Border type:", 3, ["Top left","Top right","Bottom left","Bottom right"]),
        (PF_SPINNER, "in_opacity", "Opacity (%):", 60, (0, 100, 1)),
        (PF_TOGGLE, "in_invert", "Invert colors:", 0)
    ], 
    [],
    watermark_from_svg,
    )

main()

