# Course: VIN Project
# Login: xdobis01
# Title: Matikolaz

from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

import numpy as np
import os  

# Root widget declaration and image shape definition
root = Tk()
root.title("Matikola")
monitor_width, monitor_height = 1280, 960
root.geometry(str(int(monitor_width))+"x"+str(int(monitor_height*0.9)))
img_shape = (int(monitor_width/3), int(monitor_width/3))
img_width, img_height = img_shape


# Working directory
base_path = os.getcwd() + "/"

## Image manipulation

# Swaps left and right image
def swap_images():
    global left_image
    global right_image
    left_image, right_image = right_image, left_image
    
    global left_example
    global right_example
    left_example, right_example = right_example, left_example
    
    left_label = Label(image=left_example, width=img_width, height=img_height).grid(row=1, column=0)
    right_label = Label(image=right_example, width=img_width, height=img_height).grid(row=1, column=1)
    process_image()

# Opens dialog to select image and after selection loads it into left image widget or right image widget
def open_image(base_path, img_shape, side):

    root.filename = filedialog.askopenfilename(initialdir=base_path, title="Select image", filetypes=(("png files","*.png"), ("jpg files", "*.jpg"), ("all files", "*")))
    image = Image.open(root.filename).resize(img_shape)
    
    if side == 0:
        global left_image
        global left_example
        global left_label
        left_image = image
        left_example = ImageTk.PhotoImage(image)
        left_label = Label(image=left_example, width=img_shape[0], height=img_shape[1]).grid(row=1, column=0)
    elif side == 1:
        global right_image
        global right_example
        global right_label
        right_image = image
        right_example = ImageTk.PhotoImage(image)
        right_label = Label(image=right_example, width=img_shape[0], height=img_shape[1]).grid(row=1, column=1)
    else:
        print("Incorrect image placement")

# Save collage image to results directory, image filename is incremented count of files in results directory
def save_image(base_path):
    global collage_example
    _, _, files = next(os.walk(base_path + "results"))
    ImageTk.getimage(collage_example).save(base_path + f"/result_id_{len(files) + 1}.png", "PNG")

## Sliders and values

# Read slider change, show it on to equation text in bottom part and apply to collage image
def slider_update(slider_value, var="constant", func="sin"):

    if var == "constant":
        if func == "sin":
            global constant_sin
            constant_sin = np.float32(slider_value)
        elif func == "tan":
            global constant_tan
            constant_tan = np.float32(slider_value)
        else:
            global constant_lin
            constant_lin = np.float32(slider_value)
    elif var == "scale":
        if func == "sin":
            global scale_sin
            scale_sin = np.float32(slider_value)
        elif func == "tan":
            global scale_tan
            scale_tan = np.float32(slider_value)
        else:
            global scale_lin
            scale_lin = np.float32(slider_value)
    elif var == "freq":
        if func == "sin":
            global freq_sin
            freq_sin = np.float32(slider_value)
        else:
            global freq_tan
            freq_tan = np.float32(slider_value)
    elif var == "trans":
        if func == "sin":
            global trans_sin
            trans_sin = np.float32(slider_value)
        else:
            global trans_tan
            trans_tan = np.float32(slider_value)
    else:
        global rotation
        global reverse
        rotation = int(slider_value) % 4
        reverse = int(slider_value) > 3
        
    slider_visual_change(func)
    process_image()

# Show slider change on to equation text in bottom part
def slider_visual_change(func="sin"):
    if func == "sin":
        global scale_sin
        global freq_sin
        global trans_sin
        global constant_sin
        global func_sin_label
        del func_sin_label
        func_sin_label = Label(text=f"Sin function: {np.around(scale_sin,0)}*sin({np.around(freq_sin,0)/100}*x + {np.around(trans_sin,0)}) + {np.around(constant_sin,0)}")
        func_sin_label.grid(row=12, column=0)
    elif func == "tan":
        global scale_tan
        global freq_tan
        global trans_tan
        global constant_tan
        global func_tan_label
        del func_tan_label
        func_tan_label = Label(text=f"Tan function: {np.around(scale_tan,0)}*sin({np.around(freq_tan,0)/100}*x + {np.around(trans_tan,0)}) + {np.around(constant_tan,0)}")
        func_tan_label.grid(row=12, column=1)
    else:
        global scale_lin
        global constant_lin
        global func_lin_label
        del func_lin_label
        func_lin_label = Label(text=f"Lin function: {np.around(scale_lin,0)/100}*x + {np.around(constant_lin,0)}")
        func_lin_label.grid(row=12, column=2)   
 
# Initialize slider values
constant_sin = 0
scale_sin = 0
freq_sin = 0
trans_sin = 0

constant_tan = 0
scale_tan = 0
freq_tan = 0
trans_tan = 0

scale_lin = 0
constant_lin = 0

rotation = 0
reverse = False

# Initialize Sin function sliders
slider_constant_sin = Scale(root, from_ =-img_height/2, to=img_height/2, length=img_width*0.9, command=lambda x: slider_update(x,"constant","sin"), resolution=0.1, orient=HORIZONTAL)
slider_scale_sin = Scale(root, from_ =-1000, to=1000, length=img_width*0.9, command=lambda x: slider_update(x,"scale","sin"), resolution=0.1, orient=HORIZONTAL)
slider_freq_sin = Scale(root, from_ =-30, to=30, length=img_width*0.9, command=lambda x: slider_update(x,"freq","sin"), resolution=0.1, orient=HORIZONTAL)
slider_trans_sin = Scale(root, from_ =-30, to=30, length=img_width*0.9, command=lambda x: slider_update(x,"trans","sin"), resolution=0.1, orient=HORIZONTAL)

# Initialize Tan function sliders
slider_constant_tan = Scale(root, from_ =-img_height/2, to=img_height/2, length=img_width*0.9, command=lambda x: slider_update(x,"constant","tan"), resolution=0.1, orient=HORIZONTAL)
slider_scale_tan = Scale(root, from_ =-1000, to=1000, length=img_width*0.9, command=lambda x: slider_update(x,"scale","tan"), resolution=0.1, orient=HORIZONTAL)
slider_freq_tan = Scale(root, from_ =-30, to=30, length=img_width*0.9, command=lambda x: slider_update(x,"freq","tan"), resolution=0.1, orient=HORIZONTAL)
slider_trans_tan = Scale(root, from_ =-30, to=30, length=img_width*0.9, command=lambda x: slider_update(x,"trans","tan"), resolution=0.1, orient=HORIZONTAL)

# Initialize Geometric transform slider
slider_geo_transform = Scale(root, from_ = 0, to=7, length=img_width*0.9, command=lambda x: slider_update(x,"geo-transform","rot-rev"), resolution=1, orient=HORIZONTAL)

# Initialize Lin function slider
slider_constant_lin = Scale(root, from_ =-img_height/2, to=img_height/2, length=img_width*0.9, command=lambda x: slider_update(x,"constant","lin"), resolution=0.1, orient=HORIZONTAL)
slider_scale_lin = Scale(root, from_ =-1000, to=1000, length=img_width*0.9, command=lambda x: slider_update(x,"scale","lin"), resolution=0.1, orient=HORIZONTAL)


# Place sliders onto root widget
slider_constant_sin.grid(row=4, column=0)
slider_scale_sin.grid(row=6, column=0)
slider_freq_sin.grid(row=8, column=0)
slider_trans_sin.grid(row=10, column=0)

slider_constant_tan.grid(row=4, column=1)
slider_scale_tan.grid(row=6, column=1)
slider_freq_tan.grid(row=8, column=1)
slider_trans_tan.grid(row=10, column=1)

slider_geo_transform.grid(row=6, column=2)

slider_constant_lin.grid(row=8, column=2)
slider_scale_lin.grid(row=10, column=2)

# Reset Sin sliders
def reset_sin():
    global scale_sin
    global freq_sin
    global trans_sin
    global constant_sin
    global func_sin_label
    slider_scale_sin.set(0)
    slider_freq_sin.set(0)
    slider_trans_sin.set(0)
    slider_constant_sin.set(0)
    scale_sin = 0
    freq_sin = 0
    trans_sin = 0
    constant_sin = 0
    func_sin_label = Label(text=f"Sin function: {np.around(scale_sin,0)}*sin({np.around(freq_sin,0)}*x + {np.around(trans_sin,0)}) + {np.around(constant_sin,0)}")
    func_sin_label.grid(row=12, column=0)

# Reset Tan sliders
def reset_tan():
    global scale_tan
    global freq_tan
    global trans_tan
    global constant_tan
    global func_tan_label
    slider_scale_tan.set(0)
    slider_freq_tan.set(0)
    slider_trans_tan.set(0)
    slider_constant_tan.set(0)
    scale_tan = 0
    freq_tan = 0
    trans_tan = 0
    constant_tan = 0
    func_tan_label = Label(text=f"Tan function: {np.around(scale_tan,0)}*tan({np.around(freq_tan,0)}*x + {np.around(trans_tan,0)}) + {np.around(constant_tan,0)}")
    func_tan_label.grid(row=12, column=0)

# Reset Lin sliders
def reset_lin():
    global scale_lin
    global constant_lin
    global func_lin_label
    slider_scale_lin.set(0)
    slider_constant_lin.set(0)
    scale_lin = 0
    constant_lin = 0
    func_lin_label = Label(text=f"Lin function: {np.around(scale_lin,0)/100}*x + {np.around(constant_lin,0)}")
    func_lin_label.grid(row=12, column=2) 

## Image processing

# Create collage image from left and right images, by dividing them using sum of Sin, Tan and Lin functions
def process_image():
    global left_image
    global right_image
    
    w = left_image.width
    h = left_image.height 
    
    # Compute Sin, Tan, Lin functions and sum them into SUM function
    x_line = np.linspace(start=-w/2,stop=w/2, num=w)
    y_line = np.linspace(start=-h/2,stop=h/2, num=h)
    func_line = np.round(get_sin_line(x_line) + get_tan_line(x_line) + get_lin_line(x_line)).astype(np.int16)
    
    # Compute collage mask: Above SUM function is Left image, and below SUM is right image
    collage_mask = np.flip(np.array([y_line > func_val for func_val in func_line]), 1).T
    
    # Apply geometric transformations of rotation and reverse on collage mask
    collage_mask = np.rot90(collage_mask, k=rotation)
    collage_mask = np.flip(collage_mask, 1) if reverse else collage_mask
    
    # Segment out left and right image into collage, by using collage mask
    left_array = np.array(left_image)
    left_array[collage_mask == False] = 0
    right_array = np.array(right_image)
    right_array[collage_mask == True] = 0
    collage_array = left_array + right_array
    collage_image = Image.fromarray(np.uint8(collage_array)).convert('RGB')
    
    # Show image
    global collage_example
    global collage_label
    collage_example = ImageTk.PhotoImage(collage_image)
    collage_label = Label(image=collage_example, width=w, height=h).grid(row=1, column=2)

# Compute sin value
def get_sin_line(x_line):
    func_line = scale_sin*np.sin((freq_sin/100)*x_line + trans_sin) + constant_sin
    return func_line

# Compute tan value
def get_tan_line(x_line):
    func_line = scale_tan*np.tan((freq_tan/100)*x_line + trans_tan) + constant_tan
    return func_line

# Compute linear value
def get_lin_line(x_line):
    func_line = (scale_lin/100)*x_line + constant_lin
    return func_line

# Image widgets

left_image = Image.fromarray(np.uint8(np.ones((img_width, img_height))*255)).convert('RGB')
right_image = Image.fromarray(np.uint8(np.zeros((img_width, img_height)))).convert('RGB')

left_example = ImageTk.PhotoImage(left_image)
right_example = ImageTk.PhotoImage(right_image)
collage_example = right_example

left_label = Label(image=left_example, width=img_width, height=img_height).grid(row=1, column=0)
right_label = Label(image=right_example, width=img_width, height=img_height).grid(row=1, column=1)
collage_label = Label(image=collage_example, width=img_width, height=img_height).grid(row=1, column=2)
process_image()

## Text widgets

# Sin text labels
constant_sin_label = Label(text="Sin function constant").grid(row=3, column=0)
scale_sin_label = Label(text="Sin function scale").grid(row=5, column=0)
freq_sin_label = Label(text="Sin function frequency").grid(row=7, column=0)
trans_sin_label = Label(text="Sin function translation").grid(row=9, column=0)
func_sin_label = Label(text=f"Sin function: {scale_sin}*sin({freq_sin}*x + {trans_sin}) + {constant_sin}")
func_sin_label.grid(row=12, column=0)

# Tan text labels
constant_tan_label = Label(text="Tan function constant").grid(row=3, column=1)
scale_tan_label = Label(text="Tan function scale").grid(row=5, column=1)
freq_tan_label = Label(text="Tan function frequency").grid(row=7, column=1)
trans_tan_label = Label(text="Tan function translation").grid(row=9, column=1)
func_tan_label = Label(text=f"Tan function: {scale_tan}*tan({freq_tan}*x + {trans_tan}) + {constant_tan}")
func_tan_label.grid(row=12, column=1)

# Geometric transformations text labels
geo_transf_label = Label(text="Rotation and reverse: \n 0,4 - 0°; 1,5 - 90°; 2,6 - 180°, 3,7 - 270° \n 0-3 no reverse; 4-7 reverse").grid(row=5, column=2)

# Lin text labels
constant_lin_label = Label(text="Lin function constant").grid(row=7, column=2)
scale_lin_label = Label(text="Lin function scale").grid(row=9, column=2)
func_lin_label = Label(text=f"Lin function: {np.around(scale_lin,0)}*x + {np.around(constant_lin,0)}")
func_lin_label.grid(row=12, column=2)

# Reference equation text label
equation_label = Label(text=f"Left image > (Sin + Tan + Lin) > Right image")
equation_label.grid(row=3, column=2)

# Buttons
button_left_image = Button(root, text="Pick left image", command=lambda:open_image(base_path, img_shape, side=0)).grid(row=2, column=0)
button_right_image = Button(root, text="Pick right image", command=lambda:open_image(base_path, img_shape, side=1)).grid(row=2, column=1)

button_sin_reset = Button(root, text="Reset Sin", command=reset_sin).grid(row=11, column=0)
button_tan_reset = Button(root, text="Reset Tan", command=reset_tan).grid(row=11, column=1)
button_lin_reset = Button(root, text="Reset Lin", command=reset_lin).grid(row=11, column=2)

button_exit = Button(root, text="Exit program", command=root.quit).grid(row=0, column=0)
button_swap = Button(root, text="Swap images", command=swap_images).grid(row=0, column=1)
button_save = Button(root, text="Save result", command=lambda:save_image(base_path)).grid(row=0, column=2)

# Main loop
root.mainloop()

