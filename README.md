# inkscape-text2hershey
Convert normal text lines or flow text into hershey fonts.
This inkscape extension is a hack. As of inkscape 0.92 the normal text tools can only work with outline fonts and not with vector fonts. The original Hershey-Text extension is very limited in its layouting capabilities. This new extension is an attempt to somewhat bridge the gap.


## WARNING
Code loss. The code here is incomplete.


## Installation
This inkscape extension requires the 'Hershey-Text' extension from https://wiki.evilmadscientist.com/Hershey_Text
If your inkscape is old, you may want to update your hershey fonts as described there. 

To install our inkscape-text2hershey, copy the two files `text2hershey.inx` and `text2hershey.py` from this repository into your local inkscape extensions folder. Make sure no subdirectories are created.

After restarting inkscape you should see a new menu entry

        Extensions -> Text -> Convert to Hershey

Note that the original 'Hershey-Text' extension is found under the more general `Render` submenu, instead of `Text`.


## Usage
Create normal text lines with the text tool (F8). Adjust font, size, etc -- or even convert to a text flow filling a 
shape (Alt-W). The selected font face should look similar to the desired hershey font. Character metrics remain unchanged.

Select the text object and open the 'Convert to Hershey' window.
Select a hershey font. For an overview of the available fonts use the action 'Generate font table: all fonts' of the original 'Hershey-Text' extension.

Choose 'Apply' to replace the fonts. On some systems you ma be asked to first convert the text to paths. If so use 

        Path -> Object to Path (Shift+Ctrl+C)

then try again. The conversion can be repeated multiple times, trying e.g. different hershey fonts ow adjusting the size percetage.  
Once the text was converted to paths with inkscape or with this extension, all the characters are kept in a group. This group has an important internal SVG Attribute `aria-label`. If you ungroup or import an SVG file from elsewhere, the attribute may be missing and inkscape-text2hershey will not work.


## Thank You
Thanks to EMS for bringing vector fonts to inkscape!

