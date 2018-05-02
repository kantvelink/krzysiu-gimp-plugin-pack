#!/usr/bin/env python

from gimpfu import *
import os
import gtk

from array import array

def svg_to_multisize_icon(image, drawable, in_file_name, icon_16, icon_32, icon_48, icon_64, icon_256, icon_custom):
    if not in_file_name:
        kgpp_msgbox("No input SVG file given", "You must provide existing SVG image", gtk.MESSAGE_ERROR)
        return
    if os.path.isfile(in_file_name)==False:
        kgpp_msgbox("The SVG file doesn't exist", "Following file doesn't exist:\n<tt>%s</tt>" % (in_file_name), gtk.MESSAGE_ERROR)
        return
    
    sizes = array('I')
    wrong_sizes = []
    
    if icon_16:
        sizes.append(16)
    if icon_32:
        sizes.append(32)
    if icon_48:
        sizes.append(48)
    if icon_64:
        sizes.append(64)
    if icon_256:
        sizes.append(256)
    
    custom_sizes = list(filter(lambda s: s.strip() != "", icon_custom.split(",")))

    if len(custom_sizes)>0:        
        for csize in custom_sizes:
            csize = csize.strip()
            csize_val = validate_size(csize)
            if csize_val==False:
                wrong_sizes.append(" &#8226; <tt>%s</tt>\n" % (csize));
            else:
                sizes.append(csize_val)
    
        if len(wrong_sizes) > 0:
            kgpp_msgbox("Warning: can't recognize custom size data", "Plugin has encountered wrong value%(prefix)s in custom size list.\n\n<b>Following value%(prefix)s will be ignored</b>:\n%(list)s\n<small>Possible reasons:\n &#8226; Non-numeric characters\n &#8226; Separation by other character than comma\n &#8226; Negative numbers</small>"  % {"prefix": ("s" if len(wrong_sizes)>1 else ""), "list": ''.join(wrong_sizes)}, gtk.MESSAGE_WARNING)
        
    if len(sizes) == 0:
        kgpp_msgbox("You must choose at least one size", "At least one size must be given to proceed", gtk.MESSAGE_ERROR)
        return
        
    sizes = sorted(sizes, reverse=True)

    gimp.context_push()
    
    icoimg = gimp.Image(sizes[0], sizes[0], RGB)
        
    for size in sizes:
        try:
            icon = pdb.file_svg_load(in_file_name, in_file_name, 90, size, size, 0)
        except:
            kgpp_msgbox("Can't load SVG file", "SVG file can't be loaded. Check if the file is SVG image. If it is, try to open the file directly in Gimp. If there are errors, this way you should get more details.", gtk.MESSAGE_ERROR)
            return
        
        [svg_layer] = icon.layers
        icon_layer = pdb.gimp_layer_new_from_drawable(svg_layer, icoimg)
        pdb.gimp_image_insert_layer(icoimg, icon_layer, None, -1)
        pdb.gimp_item_set_name(icon_layer, "%(size)dx%(size)d" % {"size": size})
    
    gimp.Display(icoimg)

    gimp.displays_flush()
    gimp.context_pop()

    return


def validate_size(size):
    try:
        val = int(size)
        if val<1:
            return False
        return val
    except ValueError:
        return False


def kgpp_msgbox(msg1, msg2, type):
    msgbox = gtk.MessageDialog(
        None, 
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
        type, 
        gtk.BUTTONS_OK,
        msg1
    )

    msgbox.format_secondary_markup(msg2)
    msgbox.set_title("KGPP - SVG to multisize icon")
    msgbox.set_position(gtk.WIN_POS_CENTER)
    msgbox.run()
    return

register(
    "svg_to_multisize_icon",    
    "SVG to multisize icon",   
    "SVG to multisize icon",
    "Krzysztof Blachnicki", 
    "krzysiu.net", 
    "May 2018",
    "<Image>/Filters/Krzysiu/SVG to multisize icon...", 
    "*", 
    [
        (PF_FILE, "in_file_name", "Watermark file:", ""),
        (PF_BOOL, "icon_16", "Include 16x16:", True),
        (PF_BOOL, "icon_32", "Include 32x32:", True),
        (PF_BOOL, "icon_48", "Include 48x48:", True),
        (PF_BOOL, "icon_64", "Include 64x64:", True),
        (PF_BOOL, "icon_256", "Include 256x256:", True),
        (PF_STRING, "icon_custom", "Custom sizes (comma separated; e.g. \"128,512\"):", ""),
    ], 
    [],
    svg_to_multisize_icon,
    )

main()

