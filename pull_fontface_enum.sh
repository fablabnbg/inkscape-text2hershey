# Note the _: syntax: this is needed with inx files as they all suffer from heavy usage of namespaces.
# 'xmlstarlet el' and all 'sel'-examples are silent about the namespace topic. It always cost hours of reverse engineering to find
# an accepable workaround. 
# Here is one that explains the existance of the '_:' prefix. It also explains that --no-doc-namespace does not do the obvious:
# http://xmlstar.sourceforge.net/doc/UG/xmlstarlet-ug.html#idm47077139529952

font_inx_outfile=param_fontface_enum.inx.in
font_inx_srcurl=https://github.com/evil-mad/EggBot/raw/master/inkscape_driver/hershey.inx
font_inx_reference=$HOME/.config/inkscape/extensions/hershey.inx
test -f $font_inx_reference || font_inx_reference=/usr/share/inkscape/extensions/hershey.inx

curl -L -s $font_inx_srcurl | xmlstarlet  sel -I -t -m '//_:*[@name="fontface"]' -c . > $font_inx_outfile
if [ -f $font_inx_reference ]; then
  xmlstarlet  sel -I -t -m '//_:*[@name="fontface"]' -c . $font_inx_reference | diff -Bbu - $font_inx_outfile
  
  if [ $? != 0 ]; then 
    echo ""
    echo "WARNING: $font_inx_outfile"
    echo "  Element <_param name=fontface ... differs from upstream"
    echo "  url: $font_inx_srcurl"
  fi
fi
