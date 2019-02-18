# Charset processing
#
# there are hundreds of thousands of rm2k/2k3 charsets available for free on the internet and
# it would be a shame to put all of that to waste, even if the standard very old and is no longer in use
#
# this program lets you:
# - Convert rm2k/2k3 charsets to other engines with no loss of image quality
# It should look roughly the same as the charsets from the very first old rm from 1995 which supported a
# screen resolution of 320x240
# - -charset: make a charset from the chars's pngs
#   - (MANDATORY) char size                     (integer)
#   - (MANDATORY) canvas x size                 (integer)
#   - (MANDATORY) canvas y size                 (integer)
#   - (OPTIONAL) -char_size     :   char size
#       -(MANDATORY) individual char size(x)    (integer)
#       -(MANDATORY) individual char size(y)    (integer)
#   - (OPTIONAL) -canvas_size   :   canvas size
#       -(MANDATORY) individual canvas size(x)  (integer)
#       -(MANDATORY) individual canvas size(y)  (integer)
#
# - -VX: Converts rm2k char format to vx char format(down, left, right, up)
#
# - resize: resize pngs in folder
#   - (MANDATORY) resize multiplier (integer)
#   - (OPTIONAL) replace (text: replace)
#
#
# CONSTRAINTS:
# //Only the png file format is supported.
#
# //The first sub-parameter of '-charset' should not be a decimal number, as it could resoult on some sprites
# overflowing out of the canvas.
#
# //All of the png files in the folder must be the same size.
#
# //-resize is meant to be used by itself, example : Python Processor.py -resize 2.
# But if you want to combine -resize with other parameters, then use a second, optional sub-parameter 'replace'.
# for example:
# Python Processor.py -resize 2 replace -charset 3 3 3 -char_size 144 256 -canvas_size 576 512
# with this command, the program will resize the chars on the folder, make the charset, and scale it by 3, don't forget
# to specify the new chars's XxY resolution and the new canvas's XxY resolution as you increase the value of -resize,
# for example if you use -resize 3 replace, -char_size and canvas_scale must be 3 times as high.
#
#
#
# KNOWN BUGS:
# - Sometimes the pngs are saved starting by the index of 1 instead of 0
#
# - when using -canvas_size, the canvas doesnt scale and insteas adopts the value of the first parameter

from PIL import Image
from PIL import ImageDraw
import glob
import os
import sys
import time

# Check if parameter exists
# Valid parameters:charset, chipset, faceset

def parameterIterate(argvCompare):
    i = 0
    matchCheck = 0
    while len(sys.argv) > i:
        #print(i)
        if sys.argv[i] == argvCompare:
            matchCheck = sys.argv[i]
            #print('check = '+ matchCheck)
            break

        i += 1
    return matchCheck

def stringConvertToIntFloat(strSample):
    temp = strSample
    if '.' in temp:
        final = float(temp)
    else:
        final = float(temp)
        final = int(temp)
    return final

def argHierarchyProcess(parentArgument):
    indexArg = 0
    parentFound = False
    childArgArray = []

    for currentArg in sys.argv:

        if parentFound:
            childArgArray.append(currentArg)
            if '-' in currentArg:
                break

        if currentArg == parentArgument:
            parentFound = True

    return childArgArray


def charsetConvert(scaleMultiplier = 3, xScaleMultiplier = 3, yScaleMultiplier = 3):
    #Parameters:
    # charset scale
    # canvas scale x
    # canvas scale y

    # this function takes all charset pngs in the folder and converts it to another size and/or canvas shape.

    # the parameter scaleMultiplier should not be a float, it would make the sprites overflow out of the canvas
    # the iteration process starts at the top-left of the image

    xScale = 0
    yScale = 0

    scaleMultiplier = stringConvertToIntFloat(scaleMultiplier)
    xScaleMultiplier = stringConvertToIntFloat(xScaleMultiplier)
    yScaleMultiplier = stringConvertToIntFloat(yScaleMultiplier)

    # character resize tuple arguments
    # 72: single charset base width(rm2K, 320x240 screen resolution)
    # 128: single charset base height(rm2K 320x240 screen resolution)
    # sets the width and height of the base chars with the parameter -char_size
    # if there's no '-char_size' parameter, it defaults to the base rm2k dimensions
    if parameterIterate('-char_size'):
        xSizeToScale = int(argHierarchyProcess('-char_size')[0]) * scaleMultiplier
        ySizeToScale = int(argHierarchyProcess('-char_size')[1]) * scaleMultiplier
    else:
        xSizeToScale = 72 * scaleMultiplier
        ySizeToScale = 128 * scaleMultiplier


    # canvas resize tuple arguments
    # 288: canvas base width (rm2K, 320x240 resolution)
    # 256: canvas base height(rm2K, 320x240 resolution)
    # sets the width and height of the canvas with the parameter -canvas_size
    # if there's no '-canvas_size' parameter, it defaults to the base rm2k dimensions
    if parameterIterate('-canvas_size'):
        xSizeCanvasScale = int(argHierarchyProcess('-canvas_size')[0]) * xScaleMultiplier
        ySizeCanvasScale = int(argHierarchyProcess('-canvas_size')[1]) * yScaleMultiplier
        print(xSizeCanvasScale)
        print(ySizeCanvasScale)

    else:
        xSizeCanvasScale = 288 * xScaleMultiplier
        ySizeCanvasScale = 256 * yScaleMultiplier
        print(xSizeCanvasScale)
        print(ySizeCanvasScale)

    sizeToScaleCanvas = xSizeCanvasScale, int(ySizeCanvasScale)



    # number of iterations before new file is created
    iterationLimit = int((xSizeCanvasScale / xSizeToScale) * (ySizeCanvasScale / ySizeToScale))
    try:
        imageFinal = Image.new('RGB', sizeToScaleCanvas)

    except TypeError as e:
        print('################################################')
        print('ERROR: dimensions of png must be both integers')
        print('################################################')
        raise TypeError('integer argument expected, got float')
    i = 0
    e = 0
    draw = ImageDraw.Draw(imageFinal)

    if not os.path.exists('Generated'):
        os.makedirs('Generated')



    for infile in glob.glob("*.png"):

        img = Image.open(infile)

        if parameterIterate('-VX'):
            w, h = img.size
            # w = stringConvertToIntFloat(w)
            # h = stringConvertToIntFloat(h)
            imgTemp1 = img.crop((0, 0, w, h/4))
            imgTemp2 = img.crop((0, h/4, w, h/2))
            imgTemp3 = img.crop((0, h/2, w, ((h/2) + (h/4)) ))
            imgTemp4 = img.crop((0, ((h/2) + (h/4)), w, h))

            img.paste(imgTemp3, (0, 0))
            img.paste(imgTemp4, (0, int((h/4))))
            img.paste(imgTemp2, (0, int((h/2))))
            img.paste(imgTemp1, (0, int(((h/2) + (h/4))) ))

        # if parameterIterate('-VX'):
        #     imgTemp1 = img.crop((0, 0, 72, 32))
        #     imgTemp2 = img.crop((0, 32, 72, 64))
        #     imgTemp3 = img.crop((0, 64, 72, 97))
        #     imgTemp4 = img.crop((0, 97, 72, 128))
        #
        #     img.paste(imgTemp3, (0, 0))
        #     img.paste(imgTemp4, (0, 32))
        #     img.paste(imgTemp2, (0, 64))
        #     img.paste(imgTemp1, (0, 97))





        img = img.resize((int(xSizeToScale), int(ySizeToScale)))
        imageFinal.paste(img, (int(xScale), int(yScale)))
        xScale += xSizeToScale
        if xScale == xSizeCanvasScale:
            xScale = 0
            yScale = yScale + ySizeToScale
        i += 1
        #print('charset processed...')
        #print(iterationLimit)
        if i == iterationLimit:
            #print('iterationlimit:' + str(iterationLimit))

            imageFinal.save('Generated/char_resized'+str(e)+'.png', imageFinal.format, quality='keep')
            #print('png created...')
            draw.rectangle([(0, 0), imageFinal.size], fill=(32, 156, 0))
            #print('template wipe...')
            e += 1
            i = 0
            yScale = 0
            xScale = 0
        #time.sleep(1)





    e += 1
    if i%8 != 0:
        imageFinal.save('Generated/char_resized' + str(e) + '.png', imageFinal.format, quality='keep')
        # print('png created...')
        # print('template wipe...')

    # mageFinal.show()

def resizePng(multiplier, replace):
    multiplier = int(multiplier)
    for infile in glob.glob("*.png"):
        img = Image.open(infile)
        x,y = img.size
        #print(type(x), type(y)) # 72 128
        #x = stringConvertToIntFloat(x)
        #y = stringConvertToIntFloat(y)

        x = int(x * multiplier)
        y = int(y * multiplier)
        print(x)
        print(y)# 222222222 2222222
        name = img.filename

        print((x, y))
        img = img.resize((x, y))
        if replace == 'replace':
            img.save(name, img.format, quality='keep')
        else:
            img.save('Resized_'+name, img.format, quality='keep')

#resize all pngs inside folder
if parameterIterate('-resize'):
    multiplier = argHierarchyProcess('-resize')[0]

    if len(argHierarchyProcess('-resize')) > 1:
        replace = argHierarchyProcess('-resize')[1]
    else:
        replace = 'replaceNot'

    resizePng(multiplier, replace)

#charset processor
if parameterIterate('-charset'):

    print('DFDFDFFDFD')
    scaleMultiplier = argHierarchyProcess('-charset')[0]
    xScaleMultiplier = argHierarchyProcess('-charset')[1]
    yScaleMultiplier = argHierarchyProcess('-charset')[2]


    charsetConvert(scaleMultiplier, xScaleMultiplier, yScaleMultiplier)


elif len(sys.argv) != 5:
    print('Error: 5 parameters are needed in total')
    print('the 3 optional parameters are:')
    print('argv[3]: base single charset scaling multiplier')
    print('argv[4]: base canvas width multiplier')
    print('argv[5]: base canvas height multiplier')
    print('argv[6]:OPTIONAL parameter VX, converts charset to rmvx and later formats')
    print('use these parameters or simply type Python ImageProcessing.py charset for default values of 3 3 3')
else:
    charsetConvert()
