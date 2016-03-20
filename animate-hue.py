#!/usr/bin/env python

from gimpfu import *

def krzysiu_animate_hue(image, drawable, in_steps, in_min, in_max, in_speed, in_speed_type, in_sat, in_light, in_type, in_reverse) :
    gimp.context_push()
    image.undo_group_start()
    basename = drawable.name
    
    step_length = (in_max - in_min) / in_steps
    current_step = 1
    hue = in_min
    in_sat = int(in_sat)
    in_light = int(in_light)
    
    if in_reverse == 1:
        hue = in_max
        step_length *= -1
        
    if in_speed_type == 1:
        in_speed = in_speed / in_steps
    
    name_type = '(' + ("Combine","Replace")[bool(in_type)] + ') (' + str(int(in_speed)) + 'ms)'
    
    while (current_step <= in_steps):
        layer = pdb.gimp_layer_new_from_drawable(drawable, image)
        layer.name = basename + ' [h: ' + str(int(hue)) + '] ' + name_type
        pdb.gimp_image_add_layer(image, layer, -1)
        pdb.gimp_colorize(layer, int(hue), in_sat, in_light)
        hue += step_length
        current_step += 1
        
    image.undo_group_end()
    gimp.displays_flush()
    gimp.context_pop()

    return

register(
    "krzysiu_animate_hue",    
    "Animate hue",   
    "Animate hue",
    "Krzysztof Blachnicki", 
    "krzysiu.net", 
    "March 2016",
    "<Image>/Filters/Krzysiu/Animate hue...", 
    "*", 
    [
        (PF_SPINNER, "in_steps", "Steps:", 10, (1, 360, 1)),
        (PF_SLIDER, "in_min", "Minimum hue (deg.):", 0, (0, 360, 1)),
        (PF_SLIDER, "in_max", "Maximum hue (deg.):", 360, (0, 360, 1)),
        (PF_SPINNER, "in_speed", "Animation speed (ms):", 100, (1, 10000, 50)),
        (PF_OPTION, "in_speed_type", "Given speed is:", 0, ["Delay between frames","Total time"]),
        (PF_SLIDER, "in_sat", "Saturation (%):", 50, (0, 100, 1)),
        (PF_SLIDER, "in_light", "Lightness (%):", 0, (-100, 100, 1)),
        (PF_OPTION, "in_type", "Animation type:", 0, ["Combine","Replace"]),
        (PF_TOGGLE, "in_reverse", "Reverse animation:", 0)
    ], 
    [],
    krzysiu_animate_hue,
    )

main()
