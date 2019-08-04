#HOW TO USE:
#Put the individual character pngs on the 'Characters' folder and the charsets on the 'Generated' folder and start 
#using the program
#
#
# Charset processing
#
# there are tens of thousands of rm2k/2k3 charsets available for free on the internet and
# it would be a shame to put all of that to waste, even if the standard very old and is no longer in use
#
# this program lets you:
# - Convert rm2k/2k3 charsets to other engines with no loss of image quality
# It should look roughly the same as the charsets from the very first old rm from 1995 which supported a
# screen resolution of 320x240
#
#
# CONSTRAINTS:
# //Only the png file format is supported.
#
# //The first sub-parameter of '-charset' should not be a decimal number, as it could result on some sprites
# overflowing out of the canvas.
#
# //All of the png files in the character folder must be the same size.
#
# //You can only resize by increasing the size, not decreasing it(for now)
#
#
#TIPS:
#
#The green background on the sample charsets is R:32 G:156 B:0
#
#To convert from the rm2k charset format to the vx format use the cut option, then the make charset option(make sure to mark the 'convert to VX' box.
#
#'charset canvas size multiplier' means just by how much do you want to resize the canvas, it works the same way as the resize option
# unless you are using another engine then rpg maker, just use two identical values for x and y, x:1 and y:1 if you don't want to resize and only want to assemble a
# spritesheet or convert to VX.