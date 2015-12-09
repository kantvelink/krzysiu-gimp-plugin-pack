#!/usr/bin/env python

from gimpfu import *
from random import randint
from math import fmod


def krzysiu_cloudy_background(image, drawable, in_bg_color, in_blur_strength, in_bg_layer):
    MAXINT32 = 2147483647
    MAXBYTE = 255

    gimp.context_push()
    image.undo_group_start()

    if in_bg_layer:
        pdb.gimp_selection_none(image)
        workspace = pdb.gimp_layer_new(
            image, image.width, image.height, RGB_IMAGE, "Cloudy background", 100, NORMAL_MODE)
        pdb.gimp_image_insert_layer(image, workspace, None, -1)
        pdb.gimp_image_lower_item_to_bottom(image, workspace)
    else:
        workspace = drawable

    pdb.plug_in_plasma(image, workspace, randint(0, MAXINT32), 0.2)
    if in_blur_strength > 0:
        pdb.plug_in_gauss(image, workspace, in_blur_strength, in_blur_strength, 1)

    bg_color_r = float(in_bg_color[0]) / MAXBYTE
    bg_color_g = float(in_bg_color[1]) / MAXBYTE
    bg_color_b = float(in_bg_color[2]) / MAXBYTE

    bg_color_max = max(bg_color_r, bg_color_g, bg_color_b)
    bg_color_min = min(bg_color_r, bg_color_g, bg_color_b)
    bg_color_delta = bg_color_max - bg_color_min
    bg_color_l = (bg_color_max + bg_color_min) / 2

    if bg_color_delta == 0:
        bg_color_h = 0
        bg_color_s = 0
        else:
        bg_color_s = bg_color_delta / (1 - abs(2 * bg_color_l - 1)) * 100

        if bg_color_max == bg_color_r:
            bg_color_h = 60 * fmod(((bg_color_g - bg_color_b) / bg_color_delta), 6)
            if bg_color_b > bg_color_g:
                bg_color_h += 360

        if bg_color_max == bg_color_g:
            bg_color_h = 60 * ((bg_color_b - bg_color_r) / bg_color_delta + 2)

        if bg_color_max == bg_color_b:
            bg_color_h = 60 * ((bg_color_r - bg_color_g) / bg_color_delta + 4)

    bg_color_l = (bg_color_l * 200) - 100

    pdb.gimp_colorize(workspace, bg_color_h, bg_color_s, bg_color_l)

    image.undo_group_end()
    gimp.displays_flush()
    gimp.context_pop()

    return

register(
    "krzysiu_cloudy_background",
    "Render cloudy background...",
    "Renders plasma and colorize it",
    "Krzysztof Blachnicki",
    "krzysiu.net",
    "September 2014",
    "<Image>/Filters/Krzysiu/Render cloudy background",
    "*",
    [
        (PF_COLOR, "in_bg_color", "Color:", (40, 134, 222)),
        (PF_SLIDER, "in_blur_strength", "Blur strength (px; 0=off):", 30, (0, 300, 1)),
        (PF_TOGGLE, "in_bg_layer", "Create background layer:", 0)
    ],
    [],
    krzysiu_cloudy_background,
)

main()
