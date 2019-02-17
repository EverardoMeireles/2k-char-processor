# Charset processing

# there are hundreds of thousands of rm2k/2k3 charsets available for free on the internet and
# it would be a shame to put all of that to waste, even if the standard very old and is no longer in use
#
# this program lets you:
# - Convert rm2k/2k3 charsets to other engines with no loss of image quality
# It should look roughly the same as the charsets from the very first old rm from 1995 which supported a
# screen resolution of 320x240
#
# - resize
#
# CONSTRAINTS:
# Only the png file format is supported.
#
# The first sub-parameter of '-charset' should not be a decimal number, as it could resoult on some sprites
# overflowing out of the canvas.
#
# All of the png files in the folder must be the same size.

# KNOWN BUGS:
# - Sometimes the pngs are saved starting by the index of 1 instead of 0
#
# - when using -canvas_scale, the canvas doesnt scale and insteas adopts the value of the first parameter

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
    # sets the width and height of the base chars with the parameter -char_scale
    # if there's no '-char_scale' parameter, it defaults to the base rm2k dimensions
    if parameterIterate('-char_scale'):
        xSizeToScale = int(argHierarchyProcess('-char_scale')[0]) * scaleMultiplier
        ySizeToScale = int(argHierarchyProcess('-char_scale')[1]) * scaleMultiplier
    else:
        xSizeToScale = 72 * scaleMultiplier
        ySizeToScale = 128 * scaleMultiplier


    # canvas resize tuple arguments
    # 288: canvas base width (rm2K, 320x240 resolution)
    # 256: canvas base height(rm2K, 320x240 resolution)
    # sets the width and height of the canvas with the parameter -canvas_scale
    # if there's no '-canvas_scale' parameter, it defaults to the base rm2k dimensions
    if parameterIterate('-canvas_scale'):
        xSizeCanvasScale = int(argHierarchyProcess('-canvas_scale')[0]) * xScaleMultiplier
        ySizeCanvasScale = int(argHierarchyProcess('-canvas_scale')[1]) * yScaleMultiplier
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

# Python ImageIterate charset 3
if parameterIterate('-charset'):
    if len(sys.argv) > 2:
        scaleMultiplier = argHierarchyProcess('-charset')[0]
        xScaleMultiplier = argHierarchyProcess('-charset')[1]
        yScaleMultiplier = argHierarchyProcess('-charset')[2]

        # if scaleMultiplier == isinstance(scaleMultiplier, float):
        #     scaleMultiplier = float(scaleMultiplier)
        #
        # if xScaleMultiplier == isinstance(xScaleMultiplier, float):
        #     xScaleMultiplier = float(xScaleMultiplier)
        #
        # if yScaleMultiplier == isinstance(yScaleMultiplier, float):
        #     yScaleMultiplier = float(yScaleMultiplier)


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


elif parameterIterate('faceset'):
    print('&')