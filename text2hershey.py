#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Convert Text to Hershey - a font substitution hack to make properly layouted text using "Hershey" fonts for plotters

Copyright 2018 Jürgen Weigert <juergen@fabmail.org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

------------------------

CAUTION: keep the version numnber in sync with text2hershey.inx about page

"""
import sys
import inkex
import simplestyle
try:
  import hersheydata          #data file w/ Hershey font data
except:
  inkex.errormsg("ERROR: hersheydata.py not found. Is the 'Hershey-Text' extension missing?")
  sys.exit(1)


Debug = False
FONT_GROUP_V_SPACING = 45

# INKSCAPEDIR="C:/Program Files (x86)/Inkscape/"
INKSCAPEDIR=""

# FROM: visicut_export.py
# find executable in the PATH
def which(program, extraPaths=[]):
    pathlist = extraPaths + os.environ["PATH"].split(os.pathsep) + [""]
    if "nt" in os.name: # Windows
        if not program.lower().endswith(".exe"):
            program += ".exe"
        programfiles=os.environ.get("ProgramFiles","C:\\Program Files\\")
        programfiles86=os.environ.get("ProgramFiles(x86)","C:\\Program Files (x86)\\")
        # also look in %ProgramFiles%/yourProgram/yourProgram.exe
        pathlist+= [programfiles+"\\"+program+"\\", programfiles86+"\\"+program+"\\"]
    def is_exe(fpath):
        return os.path.isfile(fpath) and (os.access(fpath, os.X_OK) or fpath.endswith(".exe"))
    for path in pathlist:
      exe_file = os.path.join(path, program)
      if is_exe(exe_file):
        return exe_file
    raise Exception("Cannot find executable {0} in PATH={1}.\n\n"
                    "For a quick fix: Set INKSCAPEDIR in "
                    "{2}"
                    .format(str(program), str(pathlist), os.path.realpath(__file__)))

INKSCAPEBIN=which("inkscape",[INKSCAPEDIR])


def inkscape_batch_text2path(svgfile, id):
    '''
    Windows code from https://stackoverflow.com/questions/7647167/check-if-a-process-is-running-in-python-in-linux-unix
    Windows has a strange order: read, close, wait. With darwin and linux we try a more natural: wait, read, close.
    '''
    import subprocess
    ## inspired by visicut_export.py
    batchcmd = (INKSCAPEBIN, "--select="+id, "--verb=ObjectToPath", "--verb=FileSave", "--verb=FileQuit", svgfile)
    ## nicer version according to usage, but segfaults!
    # batchcmd = (INKSCAPEBIN, "--without-gui", "--select="+id, "--export-id="+id, "--export-id-only", "--export-text-to-path", "--export-plain-svg="+svgfile+".out.svg")
    sys_platform = sys.platform.lower()
    output = ""
    if sys_platform.startswith('win'):

        ps = subprocess.Popen(r' '.join(batchcmd)), shell=True, stdout=subprocess.PIPE)
        output = ps.stdout.read()
        ps.stdout.close()
        ps.wait()
    else:
        # OSX sys_platform.startswith('darwin'):
        # and Linux
        ps = subprocess.Popen(r' '.join(batchcmd), shell=True, stdout=subprocess.PIPE)
        ps.wait()
        output = ps.stdout.read()
        ps.stdout.close()

    if output == "":
        inkex.errormsg("ERROR: failed convert text object to path: id=%d \n Please do that manually, then try again" % id)
        sys.exit(1)

    return output


sys.exit(0)

def draw_svg_text(char, face, offset, vertoffset, parent):
    style = { 'stroke': '#000000', 'fill': 'none' }
    pathString = face[char]
    splitString = pathString.split()
    midpoint = offset - float(splitString[0])
    splitpoint = pathString.find("M")
    # Space glyphs have just widths with no moves, so their splitpoint is 0
    # We only want to generate paths for visible glyphs where splitpoint > 0
    if splitpoint > 0:
        pathString = pathString[splitpoint:] #portion after first move
        trans = 'translate(' + str(midpoint) + ',' + str(vertoffset) + ')'
        text_attribs = {'style':simplestyle.formatStyle(style), 'd':pathString, 'transform':trans}
        inkex.etree.SubElement(parent, inkex.addNS('path','svg'), text_attribs)
    return midpoint + float(splitString[1])   #new offset value

def svg_text_width(char, face, offset):
    pathString = face[char]
    splitString = pathString.split()
    midpoint = offset - float(splitString[0])
    return midpoint + float(splitString[1]) #new offset value
	
class Text2Hershey( inkex.Effect ):
    def __init__( self ):
        inkex.Effect.__init__( self )
        self.OptionParser.add_option( "--tab",  #NOTE: value is not used.
            action="store", type="string",
            dest="tab", default="splash",
            help="The active tab when Apply was pressed" )
        self.OptionParser.add_option( "--text",
            action="store", type="string",
            dest="text", default=
				     y Text for Inkscape",
            help="The input text to render")
        self.OptionParser.add_option( "--action",
            action="store", type="string",
            dest="action", default="render",
            help="The active option when Apply was pressed" )
        self.OptionParser.add_option( "--fontface",
            action="store", type="string",
            dest="fontface", default="rowmans",
            help="The selected font face when Apply was pressed" )

    def effect( self ):

        OutputGenerated = False

        # Embed text in group to make manipulation easier:
        g_attribs = {inkex.addNS('label','inkscape'):'Hershey Text' }
        g = inkex.etree.SubElement(self.current_layer, 'g', g_attribs)

        scale = self.unittouu('1px')    # convert to document units
        font = eval('hersheydata.' + str(self.options.fontface))
        clearfont = hersheydata.futural
        #Baseline: modernized roman simplex from JHF distribution.

        w = 0  #Initial spacing offset
        v = 0  #Initial vertical offset
        spacing = 3  # spacing between letters

        if self.options.action == "render":
            #evaluate text string
            letterVals = [ord(q) - 32 for q in self.options.text]
            for q in letterVals:
                if (q <= 0) or (q > 95):
                    w += 2*spacing
                else:
                    w = draw_svg_text(q, font, w, 0, g)
                    OutputGenerated = True
        elif self.options.action == 'sample':
            w,v = self.render_table_of_all_fonts( 'group_allfonts', g, spacing, clearfont )
            OutputGenerated = True
            scale *= 0.4	#Typically scales to about A4/US Letter size
        elif self.options.action == 'sampleHW':
            w,v = self.render_table_of_all_fonts( 'group_hwfonts', g, spacing, clearfont )
            OutputGenerated = True
            scale *= 0.5	#Typically scales to about A4/US Letter size
        else:
            #Generate glyph table
            wmax = 0;
            for p in range(0,10):
                w = 0
                v = spacing * (15*p - 67 )
                for q in range(0,10):
                    r = p*10 + q
                    if (r <= 0) or (r > 95):
                        w += 5*spacing
                    else:
                        w = draw_svg_text(r, clearfont, w, v, g)
                        w = draw_svg_text(r, font, w, v, g)
                        w += 5*spacing
                if w > wmax:
                    wmax = w
            w = wmax
            OutputGenerated = True
        #  Translate group to center of view, approximately
        t = 'translate(' + str( self.view_center[0] - scale*w/2 ) + ',' + str( self.view_center[1]  - scale*v/2 ) + ')'
        if scale != 1:
            t += ' scale(' + str(scale) + ')'
        g.set( 'transform',t)

        if not OutputGenerated:
            self.current_layer.remove(g)    #remove empty group, if no SVG was generated.

    def render_table_of_all_fonts( self, fontgroupname, parent, spacing, clearfont ):
        v = 0
        wmax = 0
        wmin = 0
        fontgroup = eval( 'hersheydata.' + fontgroupname )

        # Render list of font names in a vertical column:
        nFontIndex = 0
        for f in fontgroup:
            w = 0
            letterVals = [ord(q) - 32 for q in (f[1] + ' -> ')]
            # we want to right-justify the clear text, so need to know its width
            for q in letterVals:
                w = svg_text_width(q, clearfont, w)

            w = -w  # move the name text left by its width
            if w < wmin:
                wmin = w
            # print the font name
            for q in letterVals:
                w = draw_svg_text(q, clearfont, w, v, parent)
            v += FONT_GROUP_V_SPACING
            if w > wmax:
                wmax = w

        # Next, we render a second column. The user's text, in each of the different fonts:
        v = 0                   # back to top line
        wmaxname = wmax + 8     # single space width
        for f in fontgroup:
            w = wmaxname
            font = eval('hersheydata.' + f[0])
            #evaluate text string
            letterVals = [ord(q) - 32 for q in self.options.text]
            for q in letterVals:
                if (q <= 0) or (q > 95):
                    w += 2*spacing
                else:
                    w = draw_svg_text(q, font, w, v, parent)
            v += FONT_GROUP_V_SPACING
            if w > wmax:
                wmax = w
        return wmax + wmin, v


if __name__ == '__main__':
    e = Text2Hershey()
    e.affect()

# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
