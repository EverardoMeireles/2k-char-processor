from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from collections import Counter
import glob
import os
import time


def close_window_and_exit():
    window.destroy()
    print('Program is exiting...')
    exit()


def browse_files():
    global path
    path = filedialog.askdirectory(initialdir="/", title="Select a path")
    path = path + '/'
    pathEntry.delete(0, END)
    pathEntry.insert(END, path)
    update_transparency()
    print("Path: " + " " + path)
    # if " " in path:
    #     messagebox.showwarning("Invalid path", "the path can't contain spaces or the character '-'")
    #     #pathEntry.delete(0, END)


def show_user_info():
    text = "This program lets you port rm2k/2k3 charsets into other engines while conserving their aspect ratio and " \
           "pixelation. Just choose the path of your charset files and use the options.\n\n" \

    messagebox.showinfo("User info", text)


def update_transparency():
    img = Image.open(glob.glob(pathEntry.get() + "*.png")[0])
    img = img.convert("RGBA")
    image_data = img.getdata()
    print(image_data)
    red.delete(0, END)
    red.insert(END, image_data[0][0])
    green.delete(0, END)
    green.insert(END, image_data[0][1])
    blue.delete(0, END)
    blue.insert(END, image_data[0][2])
    print(image_data[0][0])
    print(image_data[0][1])
    print(image_data[0][2])


window = Tk()
window.title("2k-char-processor")
window.configure()

print('initialized')
path = ""
unixT = time.time()
loopCycle = 0
choice = StringVar()
vxChoice = StringVar()
transparentChoice = StringVar()
multiplier = StringVar()
r = StringVar()
g = StringVar()
b = StringVar()
twoOrThree = StringVar()
transparentAuto = StringVar()


def click():
    global path
    print("choice: "+str(choice))
    if choice.get() == "cut":
        charset_cut_into_pieces(path)
    else:
        if choice.get() == "resize":
            print("sds")
            resize_png(multiplier.get(), path)

        else:
            if choice.get() == "to_mv":
                resize_png(twoOrThree.get(), path)
                convert_to_vx(path)

    if vxChoice.get() == "on":
        convert_to_vx(path)

    if transparentChoice.get() == "on":
        if r.get() != "" and g.get() != "" and b.get() != "":
            arg_r = r.get()
            arg_g = g.get()
            arg_b = b.get()
        else:
            arg_r = '0'
            arg_g = '0'
            arg_b = '0'
        remove_background(path, arg_r, arg_g, arg_b)


def disable_entries_transparent_auto():
    if transparentAuto.get() == 'on':
        red.configure(state='disabled')
        green.configure(state='disabled')
        blue.configure(state='disabled')
    else:
        red.configure(state='normal')
        green.configure(state='normal')
        blue.configure(state='normal')


def interface_changed():
    if choice.get() in ["to_mv", "cut"]:
        checkVX.deselect()
        checkVX["state"] = 'disabled'
        if choice.get() == "to_mv":
            check2["state"] = 'normal'
            check3["state"] = 'normal'
        else:
            check2["state"] = 'disabled'
            check3["state"] = 'disabled'

    else:
        checkVX["state"] = 'normal'

    if choice.get() == "resize":
        resizeMultiplier["state"] = 'normal'
    else:
        resizeMultiplier["state"] = 'disabled'


button_explore = Button(window, text="Info", command=show_user_info)
button_explore.grid(row=0, column=0)

button_explore = Button(window, text="Choose your path", command=browse_files)
button_explore.grid(row=1, column=0)
pathEntry = Entry(window, width=100, textvariable=path)
pathEntry.grid(row=2, column=0, sticky=W, pady=5)


Label(window, text="What do you want to do?", fg="black", font="none 12 bold") .grid(row=4, column=0, sticky=W)
Label(window, text="(will affect all png files in the folder)", fg="black", font="none 10") .grid(row=5, column=0,
                                                                                                  sticky=W, pady=(0, 8))


# To mv
checkToMV = Radiobutton(window, text="Convert to rpg maker MV's format", variable=choice, value="to_mv", state='normal',
                        command=interface_changed)
checkToMV.grid(row=6, column=0, sticky=W)
checkToMV.select()
frameToMV = Frame(window, borderwidth=2, relief="groove", pady=5)
frameToMV.grid(row=7, sticky=W)
Label(frameToMV, text="scale by: ", fg="black", font="none 12 bold", state='normal') .grid(row=0, column=0, sticky=W)
check2 = Radiobutton(frameToMV, text="2", variable=twoOrThree, value="2", state='normal')
check2.grid(row=0, column=1, sticky=W)
check2.select()
check3 = Radiobutton(frameToMV, text="3", variable=twoOrThree, value="3", state='normal')
check3.grid(row=0, column=2, sticky=W)

# mini line break
Label(window, text="") .grid(row=8, column=0, sticky=W)

# cut
checkCut = Radiobutton(window, text="Cut charsets into individual character sprites", variable=choice, value="cut",
                       command=interface_changed, state='normal')
checkCut.grid(row=9, column=0, sticky=W)
frameCut = Frame(window, borderwidth=2, relief="groove", pady=5)
frameCut.grid(row=10, sticky=W)

# resize
checkResize = Radiobutton(window, text="Resize", variable=choice, value="resize", state='normal',
                          command=interface_changed) .grid(row=15, column=0, sticky=W)
frameResize = Frame(window, width=20, borderwidth=2, relief="groove", pady=5)
frameResize.grid(row=16, sticky=W)
Label(frameResize, text="Character size multiplier: ", fg="black", font="none 12 bold") .grid(row=0, column=0, sticky=W)
resizeMultiplier = Entry(frameResize, width=5, textvariable=multiplier, state='disabled')
resizeMultiplier.grid(row=0, column=1, sticky=W)

# to vx
checkVX = Checkbutton(window, text="Convert to VX", variable=vxChoice, onvalue='on', state='disabled')
checkVX.grid(row=17, column=0, sticky=W)
checkVX.deselect()
frameVX = Frame(window, width=20, borderwidth=2, relief="groove", pady=5)
frameVX.grid(row=18, sticky=W)

# mini line break
Label(window, text="") .grid(row=19, column=0, sticky=W)

# transparent
checkTransparent = Checkbutton(window, text="Make transparent", onvalue='on', offvalue='off',
                               variable=transparentChoice, state='normal')
checkTransparent.grid(row=20, column=0, sticky=W)
checkTransparent.deselect()
frameTransparent = Frame(window, width=20, borderwidth=2, relief="groove", pady=5)
frameTransparent.grid(row=21, sticky=W)
Label(frameTransparent, text="Background color to remove: ", fg="black", font="none 10 bold") .grid(row=1, column=0,
                                                                                                    sticky=W)
Label(frameTransparent, text="R", fg="black", font="none 8 bold") .grid(row=1, column=1, sticky=E)
red = Entry(frameTransparent, width=10, textvariable=r, state='disabled')
red.grid(row=1, column=2, sticky=W)
Label(frameTransparent, text="G", fg="black", font="none 8 bold").grid(row=1, column=3, sticky=W)
green = Entry(frameTransparent, width=10, textvariable=g, state='disabled')
green.grid(row=1, column=4, sticky=W)
Label(frameTransparent, text="B", fg="black", font="none 8 bold") .grid(row=1, column=5, sticky=W)
blue = Entry(frameTransparent, width=10, textvariable=b, state='disabled')
blue.grid(row=1, column=6, sticky=W)
checkAutoTransparent = Checkbutton(frameTransparent, text="auto", onvalue='on', offvalue='off',
                                   variable=transparentAuto, command=disable_entries_transparent_auto)
checkAutoTransparent.grid(row=1, column=7, sticky=W)
checkAutoTransparent.select()

# buttons
Button(window, text="SUBMIT", width=6, command=click) .grid(row=22, column=0, pady=5)

Button(window, text="EXIT", width=6, command=close_window_and_exit) .grid(row=23, column=0)


# Cuts charset into individual character png files.
def charset_cut_into_pieces(local_path):
    i = 0
    print("THE PATH: " + local_path)
    for infile in glob.glob(local_path + "*.png"):
        img = Image.open(infile)
        w, h = img.size
        # crop : left, upper, right, lower
        img_temp1 = img.crop((0, 0, w/4, h / 2))
        img_temp2 = img.crop((w/4, 0, w/2, h / 2))
        img_temp3 = img.crop((w/2, 0, ((w/2) + (w/4)), h / 2))
        img_temp4 = img.crop((((w/2) + (w/4)), 0, w, h / 2))
        img_temp5 = img.crop((0, h/2, w/4, h))
        img_temp6 = img.crop((w/4, h/2, w/2, h))
        img_temp7 = img.crop((w/2, h/2, ((w/2) + (w/4)), h))
        img_temp8 = img.crop((((w/2) + (w/4)), h/2, w, h))

        # save individual character sprites
        img_temp1.save(local_path + str(i) + '_' + '1' + '.png', img_temp1.format, quality='keep')
        img_temp2.save(local_path + str(i) + '_' + '2' + '.png', img_temp2.format, quality='keep')
        img_temp3.save(local_path + str(i) + '_' + '3' + '.png', img_temp3.format, quality='keep')
        img_temp4.save(local_path + str(i) + '_' + '4' + '.png', img_temp4.format, quality='keep')
        img_temp5.save(local_path + str(i) + '_' + '5' + '.png', img_temp1.format, quality='keep')
        img_temp6.save(local_path + str(i) + '_' + '6' + '.png', img_temp2.format, quality='keep')
        img_temp7.save(local_path + str(i) + '_' + '7' + '.png', img_temp3.format, quality='keep')
        img_temp8.save(local_path + str(i) + '_' + '8' + '.png', img_temp4.format, quality='keep')
        os.remove(infile)
        i += 1


# Resize pngs
def resize_png(local_multiplier, local_path):
    local_multiplier = int(local_multiplier)

    print("debug path: " + local_path)
    for infile in glob.glob(local_path + "*.png"):
        img = Image.open(infile)
        x, y = img.size

        x = int(x * local_multiplier)
        y = int(y * local_multiplier)
        print(x)
        print(y)
        name = img.filename

        print((x, y))
        img = img.resize((x, y))
        img.save(name, img.format, quality='keep')


# make background transparent
def remove_background(source_path, local_red, local_green, local_blue):
    print("debug source_path: " + source_path)
    for infile in glob.glob(source_path + "*.png"):
        img = Image.open(infile)
        img = img.convert("RGBA")
        x, y = img.size
        print(infile)
        image_data = img.getdata()
        new_data = []
        corner_pixels = []
        if transparentAuto.get() == 'on':
            for right_side_pixels in range(y):
                corner_pixels.append([image_data[(x - 1) * right_side_pixels][0],
                                      image_data[(x - 1) * right_side_pixels][1],
                                      image_data[(x - 1) * right_side_pixels][2]])

            [[result]] = [
                [list(el) for el, freq in Counter(map(tuple, lst)).most_common(1)]
                for lst in [corner_pixels]
            ]

            local_red = result[0]
            local_green = result[1]
            local_blue = result[2]

        print("removing background color:(" + str(local_red) + ", " + str(local_green) + ", " + str(local_blue)+")")
        for item in image_data:
            if item[0] == int(local_red) and item[1] == int(local_green) and item[2] == int(local_blue):
                new_data.append((int(local_red), int(local_green), int(local_blue), 0))
            else:
                new_data.append(item)

        img.putdata(new_data)
        img.save(infile, 'png')


def convert_to_vx(source_path):
    global path
    charset_cut_into_pieces(path)
    cut_char_list = []
    final_images_list = []
    i = 0
    iteration_limit = 8
    x_scale = 0
    y_scale = 0
    canvas_width = 0
    canvas_height = 0
    image_final = Image.new('RGB', (0, 0))
    for infile in glob.glob(source_path+"*.png"):
        img = Image.open(infile)
        w, h = img.size
        if i == 0:
            canvas_width = w * 4
            canvas_height = h * 2
            image_final = Image.new('RGB', (canvas_width, canvas_height))

        cut_char_list.append(infile)

        img_temp1 = img.crop((0, 0, w, h/4))
        img_temp2 = img.crop((0, h/4, w, h/2))
        img_temp3 = img.crop((0, h/2, w, ((h/2) + (h/4))))
        img_temp4 = img.crop((0, ((h/2) + (h/4)), w, h))

        img.paste(img_temp3, (0, 0))
        img.paste(img_temp4, (0, int((h/4))))
        img.paste(img_temp2, (0, int((h/2))))
        img.paste(img_temp1, (0, int(((h/2) + (h/4)))))

        # Resize the character and paste it to the canvas.
        # img = img.resize((int(xSizeToScale), int(ySizeToScale)))
        image_final.paste(img, (int(x_scale), y_scale))
        # x_scale += xSizeToScale
        # image_final.show()
        x_scale = x_scale + canvas_width/4

        if x_scale == canvas_width:
            x_scale = 0
            y_scale = int(y_scale + canvas_height/2)
        i += 1

        if i == iteration_limit:
            final_images_list.append(image_final)
            i = 0
            for cut_char in cut_char_list:
                os.remove(cut_char)

            cut_char_list = []
            x_scale = 0
            y_scale = 0

    e = 0
    for final_image in final_images_list:
        final_image.save(source_path + 'char_resized' + str(e) + '.png', image_final.format, quality='keep')
        e = e + 1


loopCycle = loopCycle+1

window.mainloop()
