# Change Log
- 2020.07.23 
  - support Inkscape 0.92 and 1.0
- 2020.07.25
  - grayscale_type [0.21R + 0.71G + 0.07B] bugfix
- 2020.08.27
  - Halftone, Halftone row, Halftone column bugfix
  - B/W conversion add 3 Halftone algorithm (Error diffusion,Ordered diffusion,Patterning 3x3 : source code from https://github.com/abhishek-sehgal954/Inkscape_extensions_for_halftone_filters )

********************
Original description
********************

# Various Inkscape extensions

 - Raster 2 Laser GCode generator
 - 
 
#Descriptions
- Raster 2 Laser GCode generator is an extension to generate Gcode for a laser cutter/engraver (or pen plotter), it can generate various type of outputs from a simple B&W (on/off) to a more detailed Grayscale (pwm)


#Installing:

Simply copy all the files in the folder "Extensions" of Inkscape

>Windows ) "C:\<...>\Inkscape\share\extensions"

>Linux ) "/usr/share/inkscape/extensions"

>Mac ) "/Applications/Inkscape.app/Contents/Resources/extensions"


for unix (& mac maybe) change the permission on the file:

>>chmod 755 for all the *.py files

>>chmod 644 for all the *.inx files



#Usage of "Raster 2 Laser GCode generator":

[Required file: png.py / raster2laser_gcode.inx / raster2laser_gcode.py]

- Step 1) Resize the inkscape document to match the dimension of your working area on the laser cutter/engraver (Shift+Ctrl+D)

- Step 2) Draw or import the image

- Step 3) To run the extension go to: Extension > 305 Engineering > Raster 2 Laser GCode generator

- Step 4) Play!




#Note
I have created all the file except for png.py , see that file for details on the license
