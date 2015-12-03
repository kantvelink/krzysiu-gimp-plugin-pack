# gimp-selection-highlight
Gimp plugin which allows to fill selection with color and border it in a simple fashion. It could be used to create tutorials ("click here" highlight), highlight the important part of PDF document etc.

## Result
![Example use](http://download.krzysiu.net/select-highlight-example.jpg)

## Installation
1. Download [select-highlight.py](https://github.com/Krzysiu/gimp-selection-highlight/blob/master/select-highlight.py)
2. Copy to plugin directory.<br><sup>If you are unsure where's your plugin directory, choose from menu item `Edit`>`Preferences` and select in the tree on the left `Folders`>`Plug-Ins`.</sup>

### Requiments
+ GIMP 2.8 (earlier versions aren't tested)
+ Python module for GIMP<br><sup>If you don't have it, reinstall GIMP and choose Python. It's worth it and you won't loose your settings.</sup>

## Usage
+ Choose plugin from menu: `Filters`>`Krzysiu`>`Highlight selection`<br><sup>Protip! To move it, edit line  `"<Image>/Filters/Krzysiu/Highlight selection"`<br>Protip 2! You can create a new layer to keep original image intact.</sup>
+ Set your settings or rely on default
+ To repeat, select another part of image and press `CTRL+F` (repeat last filter)

## Preferences
+ Color and opacity of the background
+ Color, opacity, round radius and size of the border
+ Border type - position relative to the selection<br><sup>*Outer* is outside selection, *Inner* is inside and *Middle* makes the selection middle of the border (in 4 px wide middle border it will be 2 px outside selection and 2 px inside)</sup>

## Known limitations
+ It won't work on multiple selections
+ In indexed images alpha won't work, so if opacity of background or border >50, it will be 100% opaque and if lesser, it will be off
+ It won't work if the border is inner or middle and the border would render bigger than selection

## Planned
+ Ability to add label inside highlight
+ Different blend modes
