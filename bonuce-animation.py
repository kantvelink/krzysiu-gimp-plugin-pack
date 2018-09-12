#!/usr/bin/env python

from gimpfu import *
import gtk

def bounce_animation(image, drawable, name_prefix, name_suffix) :

    if len(image.layers) < 3:
        kgpp_msgbox("Insufficient number of layers", "This script needs at least three layers, so it can turn <tt>1 2 3</tt> into <tt>1 2 3 2</tt>, which results loop <tt>1 2 3 2 1 2 (...)</tt>. One or two layers are already bouncing.", gtk.MESSAGE_ERROR)
        return
    
    gimp.context_push()
    image.undo_group_start()
    
    original_count = len(image.layers)
    
    for layer_id, layer in enumerate(image.layers):
        if not (layer_id == 0 or layer_id == original_count - 1):
            new_layer_name = name_prefix + layer.name + name_suffix
            copied_layer = pdb.gimp_layer_copy(layer, True)
            pdb.gimp_item_set_name(copied_layer, new_layer_name)
            pdb.gimp_image_insert_layer(image, copied_layer, None, -1)

    image.undo_group_end()
    gimp.displays_flush()
    gimp.context_pop()

    return

register(
    "bounce_animation",    
    "Bonuce animation",   
    "Bonuce animation",
    "Krzysztof Blachnicki", 
    "krzysiu.net", 
    "September 2018",
    "<Image>/Filters/Krzysiu/Bonuce animation...", 
    "*", 
    [
    (PF_STRING, "name_prefix", "Name prefix of copied layers", ""),
    (PF_STRING, "name_suffix", "Name suffix of copied layers", " (bounced)")    
    ], 
    [],
    bounce_animation,
    )
    
def kgpp_msgbox(msg1, msg2, type):
    msgbox = gtk.MessageDialog(
        None, 
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
        type, 
        gtk.BUTTONS_OK,
        msg1
    )

    msgbox.format_secondary_markup(msg2)
    msgbox.set_title("KGPP - bounce animation")
    msgbox.set_position(gtk.WIN_POS_CENTER)
    msgbox.run()
    return
    
main()
