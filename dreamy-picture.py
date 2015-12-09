#!/usr/bin/env python

from gimpfu import *

def krzysiu_dreamy_picture(image, drawable, in_strength, in_iterations) :
    gimp.context_push()
    image.undo_group_start()

    blur_radius = min(drawable.width, drawable.height) / 10
    
    for iter in range(0, int(in_iterations)):
        layer = pdb.gimp_layer_new_from_drawable(drawable, image)
        pdb.gimp_image_add_layer(image, layer, -1)
    
        layer_temp = pdb.gimp_layer_new_from_drawable(drawable, image)
        pdb.gimp_image_add_layer(image, layer_temp, -1)
        pdb.gimp_layer_set_mode(layer_temp, SCREEN_MODE)
        pdb.gimp_layer_set_opacity(layer, in_strength)
    
        layer_screen = pdb.gimp_image_merge_down(image, layer_temp, EXPAND_AS_NECESSARY)
    
        pdb.plug_in_gauss(image, layer_screen, blur_radius, blur_radius, 0)
        pdb.gimp_layer_set_mode(layer_screen, OVERLAY_MODE)
    
        drawable = pdb.gimp_image_merge_down(image, layer_screen, EXPAND_AS_NECESSARY)
    
    image.undo_group_end()
    gimp.displays_flush()
    gimp.context_pop()

    return

register(
    "krzysiu_dreamy_picture",    
    "Dreamy picture",   
    "Dreamy picture",
    "Krzysztof Blachnicki", 
    "krzysiu.net", 
    "September 2013",
    "<Image>/Filters/Krzysiu/Dreamy picture...", 
    "RGB*", 
    [
        (PF_SPINNER, "in_strength", "Effect strength:", 70, (1, 100, 1)),
        (PF_SPINNER, "in_iterations", "Iterations:", 2, (1, 10, 1)),
    ], 
    [],
    krzysiu_dreamy_picture,
    )

main()
