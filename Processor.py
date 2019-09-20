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
#
#COMMANDS:

# - -charset: make a charset from the chars's pngs
#   - (MANDATORY) char size multiplier          (integer)
#   - (MANDATORY) canvas x size multiplier      (integer)
#   - (MANDATORY) canvas y size multiplier      (integer)
#   - (OPTIONAL) -char_size     :   char size if you're using a charset format other than the standard rm2k format
#       -(MANDATORY) individual char size(x)    (integer)
#       -(MANDATORY) individual char size(y)    (integer)
#   - (OPTIONAL) -canvas_size   :   canvas size if you're using a charset format other than the standard rm2k format
#       -(MANDATORY) individual canvas size(x)  (integer)
#       -(MANDATORY) individual canvas size(y)  (integer)
#
# - -VX: Converts rm2k char format to vx char format(down, left, right, up)
#
# - resize: resize pngs in folder
#   - (MANDATORY) resize multiplier (integer)
#   - (MANDATORY) resize characters or charsets?(text = charset or character)
#
# - -cut: Cuts a full charset into individual character sprites
#
# - -transparent : makes the generated charset transparent
#    - (MANDATORY) path to the png to make transparent(not using this parameter will make the individual character pngs
#                 in the root folder transparent (text)
#    - (MANDATORY) background color red (integer)
#    - (MANDATORY) background color green (integer)
#    - (MANDATORY) background color blue (integer)
#
# - -help
#
# CONSTRAINTS:
# //Only the png file format is supported.
#
# //The first sub-parameter of '-charset' should not be a decimal number, as it could result on some sprites
# overflowing out of the canvas.
#
# //All of the png files in the character folder must be the same size.
#
#
#
#
# command tested for -transparent: Python Processor.py -transparent .\Generated\
#
#
# KNOWN BUGS:
# - Sometimes the pngs are saved starting by the index of 1 instead of 0
#
# - when using -canvas_size, the canvas doesnt scale and instead adopts the value of the first parameter
#
#
# os.system("start /wait cmd /c Python Processor.py")
from tkinter import *
from PIL import Image
from PIL import ImageDraw
import glob
import os
import sys
import time

def closeWindow():
    window.destroy()

def closeWindowAndExit():
    window.destroy()
    print('Program is exiting...')
    exit()

def check1Changed():
    checklC = ""

window = Tk()
window.title("2k-char-processor")
window.configure()

#
# frame3 = Frame(window, width=20, borderwidth=2, relief = "groove", pady=5)
# frame3.grid(row=7, sticky=W)
#
# frame3 = Frame(window, width=20, borderwidth=2, relief = "groove", pady=5)
# frame3.grid(row=8, sticky=W)
print ('initialized')
unixT = time.time()
unixT2 = unixT
loopCycle = 0
path = ""
choice = StringVar()
charSize= StringVar()
canvasSizeX= StringVar()
canvasSizeY= StringVar()
checkVXValue = StringVar()
charsetOrCharacterResize = StringVar()
multiplier=StringVar()
charsetOrCharacterTransparent = StringVar()
optional1CharSizeX = StringVar()
optional1CharSizeY = StringVar()
optiona12CanvasSizeX = StringVar()
optional2CanvasSizeY = StringVar()
r = StringVar()
g = StringVar()
b = StringVar()

def click():
    print("choice: "+str(choice))
    commandString = "Python Processor.py "
    if choice.get() == "cut":
        print("AOAOAOAOAOAO")
        commandString = commandString + "-cut ./Generated/"
    else:
        if choice.get() == "charset":
            commandString = commandString + "-charset "+charSize.get()+" "+canvasSizeY.get()+" "+canvasSizeY.get()+ " ./characters/"
            # Python Processor.py -resize 2 replace -charset 3 3 3 -char_size 144 256 -canvas_size 576 512
            if(len(optional1CharSizeX.get())!=0 and len(optional1CharSizeY.get())!=0 and len(optiona12CanvasSizeX.get())!=0 and len(optional2CanvasSizeY.get())!=0):
                commandString = commandString + " -char_size "+optional1CharSizeX.get()+" "+ optional1CharSizeY.get()+" -canvas_size "+optiona12CanvasSizeX.get()+" "+optional2CanvasSizeY.get()
            if checkVXValue.get() == "on":
                commandString = commandString + " -VX"
        else:
            if choice.get() == "resize":
                commandString = commandString + "-resize "+multiplier.get()+" "+charsetOrCharacterResize.get()
            else:
                if choice.get() == "transparent":
                    commandString = commandString + "-transparent"
                    # if charsetOrCharacterTransparent.get() == "characters":
                    #     commandString = commandString + " ./characters/"
                    # else:
                    #     commandString = commandString + " ./Generated/"
                    commandString = commandString + " "+charsetOrCharacterTransparent.get()
                    commandString = commandString + " "+r.get()+" "+g.get()+" "+b.get()

    print("choice is :"+choice.get())
    print("String: "+commandString)
    closeWindow()
    os.system("start /wait cmd /c "+commandString)


Label(window, text="2k char processor", fg="black", font="none 12 bold") .grid(row=1, column=0, sticky=W)
Label(window, text="Put your charsets in the 'Generated' folder, and your individual character sprites in the root folder and select one of the options below", fg="black", font="none 9 bold") .grid(row=2, column=0, sticky=W)
Label(window, text="What do you want to do?", fg="black", font="none 12 bold") .grid(row=3, column=0, sticky=W,pady=6)###############################################################################################################

#-cut
checkCut = Radiobutton(window, text="cut a charset into individual character spritesheets",variable=choice, value="cut") .grid(row=4, column=0, sticky=W)
frameCut = Frame(window, borderwidth=2, relief = "groove", pady=5)
frameCut.grid(row=5, sticky=W)#########################################################################################################################################################################################################

#line break
Label(window, text="\n", fg="black", font="none 12 bold") .grid(row=6, column=0, sticky=W)###############################################################################################################
#-charset
checkCharset = Radiobutton(window, text="Make a charset from individual char sprites and resize the charset",variable=choice, value="charset") .grid(row=7, column=0, sticky=W)
frameCharset = Frame(window, width=20, borderwidth=2, relief = "groove", pady=5)
frameCharset.grid(row=8, sticky=W)#####################################################################################################################################################################################################
Label(frameCharset, text="Character size multiplier", fg="black", font="none 12 bold") .grid(row=0, column=0, sticky=W)
charSizeEntry = Entry(frameCharset, width=5, textvariable=charSize) .grid(row=0, column=1, sticky=W)
Label(frameCharset, text="Charset canvas size multiplier", fg="black", font="none 12 bold") .grid(row=1, column=0, sticky=W)
Label(frameCharset, text="X", fg="black", font="none 6 bold") .grid(row=1, column=1, sticky=E)
canvasSizeXEntry = Entry(frameCharset, width=5,textvariable=canvasSizeX) .grid(row=1, column=2, sticky=W)
Label(frameCharset, text="Y", fg="black", font="none 6 bold") .grid(row=1, column=3, sticky=W)
canvasSizeYEntry = Entry(frameCharset, width=5,textvariable=canvasSizeY) .grid(row=1, column=4, sticky=W)
#optional 1
Label(frameCharset, text="(optional)Custom char size", fg="black", font="none 12 bold") .grid(row=2, column=0, sticky=W)
Label(frameCharset, text="X", fg="black", font="none 6 bold") .grid(row=2, column=1, sticky=E)
X1 = Entry(frameCharset, width=5, textvariable=optional1CharSizeX) .grid(row=2, column=2, sticky=W)
Label(frameCharset, text="Y", fg="black", font="none 6 bold") .grid(row=2, column=3, sticky=W)
Y1 = Entry(frameCharset, width=5, textvariable=optional1CharSizeY) .grid(row=2, column=4, sticky=W)
#optional 2
Label(frameCharset, text="(optional)Custom canvas size", fg="black", font="none 12 bold") .grid(row=3, column=0, sticky=W)
Label(frameCharset, text="X", fg="black", font="none 6 bold") .grid(row=3, column=1, sticky=E)
X2 = Entry(frameCharset, width=5, textvariable=optiona12CanvasSizeX) .grid(row=3, column=2, sticky=W)
Label(frameCharset, text="Y", fg="black", font="none 6 bold") .grid(row=3, column=3, sticky=W)
Y2 = Entry(frameCharset, width=5, textvariable=optional2CanvasSizeY) .grid(row=3, column=4, sticky=W)
checkVX = Checkbutton(frameCharset, text='Convert to VX format(Down, ,Left, Right, Up)', onvalue='on', offvalue='off',variable=checkVXValue) .grid(row=4, column=0, sticky=W)

#line break
Label(window, text="\n", fg="black", font="none 12 bold") .grid(row=9, column=0, sticky=W)###############################################################################################################

#-resize
checkResize = Radiobutton(window, text="Resize",variable=choice, value="resize") .grid(row=10, column=0, sticky=W)
frameResize = Frame(window, width=20, borderwidth=2, relief = "groove", pady=5)
frameResize.grid(row=11, sticky=W)######################################################################################################################################################################################################
Label(frameResize, text="Character size multiplier", fg="black", font="none 12 bold") .grid(row=0, column=0, sticky=W)
resizeMultiplier = Entry(frameResize, width=5, textvariable=multiplier) .grid(row=0, column=1, sticky=W)
Label(frameResize, text="Resize character or charset?", fg="black", font="none 12 bold") .grid(row=1, column=0, sticky=W)
R1 = Radiobutton(frameResize, text="characters", variable=charsetOrCharacterResize, value="character") .grid(row=1, column=1, sticky=W)
R2 = Radiobutton(frameResize, text="charsets", variable=charsetOrCharacterResize, value="charset") .grid(row=1, column=2, sticky=W)

#line break
Label(window, text="\n", fg="black", font="none 12 bold") .grid(row=12, column=0, sticky=W)###############################################################################################################

#-transparent
checkTransparent = Radiobutton(window, text="make transparent",variable=choice, value="transparent") .grid(row=13, column=0, sticky=W)
frameTransparent = Frame(window, width=20, borderwidth=2, relief = "groove", pady=5)
frameTransparent.grid(row=14, sticky=W)#################################################################################################################################################################################################
Label(frameTransparent, text="make characters or charsets transparent?", fg="black", font="none 12 bold") .grid(row=0, column=0, sticky=W)
R2 = Radiobutton(frameTransparent, text="characters",variable=charsetOrCharacterTransparent, value="./characters/") .grid(row=0, column=1, sticky=W)
R3 = Radiobutton(frameTransparent, text="charsets", variable=charsetOrCharacterTransparent, value="./Generated/") .grid(row=0, column=2, sticky=W)
Label(frameTransparent, text="Background color", fg="black", font="none 12 bold") .grid(row=1, column=0, sticky=W)
Label(frameTransparent, text="R", fg="black", font="none 8 bold") .grid(row=1, column=1, sticky=E)
red = Entry(frameTransparent, width=10, textvariable=r) .grid(row=1, column=2, sticky=W)
Label(frameTransparent, text="G", fg="black", font="none 8 bold") .grid(row=1, column=3, sticky=W)
green = Entry(frameTransparent, width=10, textvariable=g) .grid(row=1, column=4, sticky=W)
Label(frameTransparent, text="B", fg="black", font="none 8 bold") .grid(row=1, column=5, sticky=W)
blue = Entry(frameTransparent, width=10, textvariable=b) .grid(row=1, column=6, sticky=W)



#buttons
Button(window, text ="SUBMIT", width=6, command=click) .grid(row=15, column=0, sticky=W,pady=5)#########################################################################################################################################

Button(window, text ="EXIT", width=6, command=closeWindowAndExit) .grid(row=16, column=0, sticky=W)############################################################################################################################################



def parameterIterate(argvCompare):
    i = 0
    matchCheck = 0
    while len(sys.argv) > i:
        if sys.argv[i] == argvCompare:
            matchCheck = sys.argv[i]
            break

        i += 1
    return matchCheck

# converts a string either to a int or a float dynamically.
def stringConvertToIntFloat(strSample):
    temp = strSample
    if '.' in temp:
        final = float(temp)
    else:
        final = int(temp)
    return final

# Catch sub-parameters from the main parameter(the one that starts with a '-').
def argHierarchyProcess(parentArgument):
    parentFound = False
    childArgArray = []

    for currentArg in sys.argv:

        if parentFound:
            if '-' in currentArg:
                break
            childArgArray.append(currentArg)

        if currentArg == parentArgument:
            parentFound = True

    return childArgArray

# Cuts charset into individual character pngs.
def charsetCutIntoPieces(sourcePath):
    # if not os.path.exists('Characters'):
    #     os.makedirs('Characters')

    i = 0
    #sourcePath default value
    if(sourcePath == ""):
        sourcePath = "./Generated/"

    for infile in glob.glob(sourcePath + "*.png"):
        img = Image.open(infile)
        w, h = img.size
        # crop : left, upper, right, lower
        imgTemp1 = img.crop((0, 0, w/4, h / 2))
        imgTemp2 = img.crop((w/4, 0, w/2, h / 2))
        imgTemp3 = img.crop((w/2, 0, ((w/2) + (w/4)), h / 2))
        imgTemp4 = img.crop((((w/2) + (w/4)), 0, w, h / 2))
        imgTemp5 = img.crop((0, h/2, w/4, h))
        imgTemp6 = img.crop((w/4, h/2, w/2, h))
        imgTemp7 = img.crop((w/2, h/2, ((w/2) + (w/4)), h))
        imgTemp8 = img.crop((((w/2) + (w/4)), h/2, w, h))

        imgTemp1.save('Characters/'+str(i) + '_' + '1' + '.png', imgTemp1.format, quality='keep')
        imgTemp2.save('Characters/'+str(i) + '_' + '2' + '.png', imgTemp2.format, quality='keep')
        imgTemp3.save('Characters/'+str(i) + '_' + '3' + '.png', imgTemp3.format, quality='keep')
        imgTemp4.save('Characters/'+str(i) + '_' + '4' + '.png', imgTemp4.format, quality='keep')
        imgTemp5.save('Characters/'+str(i) + '_' + '5' + '.png', imgTemp1.format, quality='keep')
        imgTemp6.save('Characters/'+str(i) + '_' + '6' + '.png', imgTemp2.format, quality='keep')
        imgTemp7.save('Characters/'+str(i) + '_' + '7' + '.png', imgTemp3.format, quality='keep')
        imgTemp8.save('Characters/'+str(i) + '_' + '8' + '.png', imgTemp4.format, quality='keep')
        i += 1

# Resize pngs
def resizePng(multiplier, mode, replace):
    multiplier = int(multiplier)
    if mode == "charset":
        path = "./Generated/"
    else:
        path = "./characters/"
    for infile in glob.glob(path + "*.png"):
        img = Image.open(infile)
        x, y = img.size

        x = int(x * multiplier)
        y = int(y * multiplier)
        print(x)
        print(y)
        name = img.filename

        print((x, y))
        img = img.resize((x, y))
        if replace == 'replace':
            img.save(name, img.format, quality='keep')
        else:
            img.save(name, img.format, quality='keep')

# the main functionality of this program, converts the old rm2k charset format to a new format by resizing it.

#make background transparent
def removeBackground(sourcePath,r,g,b):
    print(sourcePath + "*.png")
    for infile in glob.glob(sourcePath + "*.png"):
        img = Image.open(infile)
        img = img.convert("RGBA")
        print(infile)
        datas = img.getdata()

        newData = []
        for item in datas:
            if item[0] == int(r) and item[1] == int(g) and item[2] == int(b):
                newData.append((int(r), int(g), int(b), 0))
            # if item[0] == 32 and item[1] == 156 and item[2] == 0:
            #     newData.append((32, 156, 0, 0))
            else:
                newData.append(item)

        img.putdata(newData)
        img.save(infile, 'png')

def charsetConvert(scaleMultiplier = 3, xScaleMultiplier = 3, yScaleMultiplier = 3, sourcePath = "./characters/"):
    # Parameters:
    # charset scale
    # canvas scale x
    # canvas scale y

    # this function takes all character pngs in the 'characters' folder and converts it to a charset of size and/or canvas shape.

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

    # Creates canvas
    try:
        imageFinal = Image.new('RGB', sizeToScaleCanvas)

    except TypeError:
        print('################################################')
        print('ERROR: dimensions of png must be both integers')
        print('################################################')
        raise TypeError('integer argument expected, got float')
    i = 0
    e = 0
    draw = ImageDraw.Draw(imageFinal)

    # creates the 'Generated' folder if it doesn't exists already.
    if not os.path.exists('Generated'):
        os.makedirs('Generated')

    # Main loop starts.
    for infile in glob.glob(sourcePath+"*.png"):

        img = Image.open(infile)

        # Converts character to the rmvx charset format.
        if parameterIterate('-VX'):
            w, h = img.size
            # w = stringConvertToIntFloat(w)
            # h = stringConvertToIntFloat(h)
            imgTemp1 = img.crop((0, 0, w, h/4))
            imgTemp2 = img.crop((0, h/4, w, h/2))
            imgTemp3 = img.crop((0, h/2, w, ((h/2) + (h/4))))
            imgTemp4 = img.crop((0, ((h/2) + (h/4)), w, h))

            img.paste(imgTemp3, (0, 0))
            img.paste(imgTemp4, (0, int((h/4))))
            img.paste(imgTemp2, (0, int((h/2))))
            img.paste(imgTemp1, (0, int(((h/2) + (h/4)))))

        # Resize the character and paste it to the canvas.
        img = img.resize((int(xSizeToScale), int(ySizeToScale)))
        imageFinal.paste(img, (int(xScale), int(yScale)))
        xScale += xSizeToScale

        # if 4 characters have been pasted to the canvas, set the y cursor down to print 4 more
        if xScale == xSizeCanvasScale:
            xScale = 0
            yScale = yScale + ySizeToScale
        i += 1
        #print('charset processed...')

        # Saves completed charset
        if i == iterationLimit:
            imageFinal.save('Generated/char_resized'+str(e)+'.png', imageFinal.format, quality='keep')
            #print('png created...')
            draw.rectangle([(0, 0), imageFinal.size], fill=(32, 156, 0))
            #print('canvas wipe...')
            e += 1
            i = 0
            yScale = 0
            xScale = 0
    e += 1

    # Saves the final charset if it has less then 8 sprites.
    if i % 8 != 0:
        imageFinal.save('Generated/char_resized' + str(e) + '.png', imageFinal.format, quality='keep')
        # print('png created...')
        # print('template wipe...')


# remove background(make transparent)
if parameterIterate('-transparent'):
    try:
        path = argHierarchyProcess('-transparent')[0]
    except IndexError as e:
        path = ""
        print("No source path specified, picking pngs from the local directory to make transparent")
    r = argHierarchyProcess('-transparent')[1]
    g = argHierarchyProcess('-transparent')[2]
    b = argHierarchyProcess('-transparent')[3]
    removeBackground(path,r,g,b)
    #removeBackground(path)

# Check if the parameter exists
if parameterIterate('-cut'):
    try:
        path = argHierarchyProcess('-cut')[0]
    except IndexError as e:
        path = "./Generated/"
        print("No source path specified, picking charset pngs from the 'Generated' folder")
    print(path)
    charsetCutIntoPieces(path)

# resize all pngs inside folder.
if parameterIterate('-resize'):
    multiplier = argHierarchyProcess('-resize')[0]
    mode = ""
    mode = argHierarchyProcess('-resize')[1]
    if len(argHierarchyProcess('-resize')) > 2:
        replace = argHierarchyProcess('-resize')[2]
    else:
        replace = 'replaceNot'
    resizePng(multiplier, mode, replace)

# charset processor.
if parameterIterate('-charset'):

    scaleMultiplier = argHierarchyProcess('-charset')[0]
    xScaleMultiplier = argHierarchyProcess('-charset')[1]
    yScaleMultiplier = argHierarchyProcess('-charset')[2]

    try:
        path = argHierarchyProcess('-charset')[3]
    except IndexError as e:
        path = ""
        print("No source path specified, picking character pngs from the local directory")

    print(argHierarchyProcess('-charset')[0])
    print(argHierarchyProcess('-charset')[1])
    print(argHierarchyProcess('-charset')[2])

    charsetConvert(scaleMultiplier, xScaleMultiplier, yScaleMultiplier, path)

# show the user how to use the command.
if parameterIterate('-help'):
    helpFile = open('help.txt', 'r')
    file_contents = helpFile.read()
    print(file_contents)
    helpFile.close()

if parameterIterate('-start'):
    window.mainloop()

unixT2 = time.time()
print('CLOCK:')
print(time.perf_counter())
if time.perf_counter() < 1.0:
    print('inside mainloop fct')

loopCycle = loopCycle+1

window.mainloop()
