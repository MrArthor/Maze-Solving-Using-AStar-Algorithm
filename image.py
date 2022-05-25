from PIL import Image
import time, sys,random
from collections import deque
from maze_solver import *
# -------------------------------------- Drawing the path onto an image ----------------------------------------------------------------------------
start_t = time.time()

colourful_path = True # Change this if you want a single-color path
single_color = (255,0,0) # Change this to the single color you want
colour_range = (0,256)
max_total_intensity = 300 # Change to None if you don't want to use it
min_total_intensity = 200 # Same as above

r,g,b = random.randrange(*colour_range),random.randrange(*colour_range),random.randrange(*colour_range)
r2,g2,b2 = random.randrange(*colour_range),random.randrange(*colour_range),random.randrange(*colour_range)
if min_total_intensity != None and max_total_intensity != None:
    while r2+g2+b2 < min_total_intensity or r2+g2+b2 > max_total_intensity:
        r2,g2,b2 = random.randrange(*colour_range),random.randrange(*colour_range),random.randrange(*colour_range)
elif min_total_intensity == None and max_total_intensity != None:
     while r2+g2+b2 > max_total_intensity:
        r2,g2,b2 = random.randrange(*colour_range),random.randrange(*colour_range),random.randrange(*colour_range)
elif min_total_intensity != None and max_total_intensity == None:
     while r2+g2+b2 < min_total_intensity:
        r2,g2,b2 = random.randrange(*colour_range),random.randrange(*colour_range),random.randrange(*colour_range) 
if not colourful_path:
    r,g,b = single_color

img = img.convert(mode="RGB") # Was in black/white mode presumably
for i in range(len(a.finished_path)-1):
    start_x,start_y, end_x, end_y = a.finished_path[i][0],a.finished_path[i][1],a.finished_path[i+1][0],a.finished_path[i+1][1]
    xstep,ystep = 0,0
    if start_x < end_x:
        xstep = 1
    elif start_x > end_x:
        xstep = -1
    elif start_y < end_y:
        ystep = 1
    elif start_y > end_y:
        ystep = -1
    while abs(start_x-end_x) > 0 or abs(start_y-end_y) > 0:
        img.putpixel((start_x,start_y),(r,g,b))
        if colourful_path:
            if r < r2:
                r+=1
            elif r > r2:
                r-=1
            else:
                r2 = random.randrange(*colour_range)
                if min_total_intensity != None and max_total_intensity != None:
                    while r2+g2+b2 < min_total_intensity or r2+g2+b2 > max_total_intensity:
                        r2 = random.randrange(*colour_range)
                elif min_total_intensity == None and max_total_intensity != None:
                    while r2+g2+b2 > max_total_intensity:
                        r2 = random.randrange(*colour_range)
                elif min_total_intensity != None and max_total_intensity == None:
                    while r2+g2+b2 < min_total_intensity:
                        r2 = random.randrange(*colour_range)

            if g < g2:
                g+=1
            elif g > g2:
                g-=1
            else:
                g2 = random.randrange(*colour_range)
                if min_total_intensity != None and max_total_intensity != None:
                    while r2+g2+b2 < min_total_intensity or r2+g2+b2 > max_total_intensity:
                        g2 = random.randrange(*colour_range)
                elif min_total_intensity == None and max_total_intensity != None:
                    while r2+g2+b2 > max_total_intensity:
                        g2 = random.randrange(*colour_range)
                elif min_total_intensity != None and max_total_intensity == None:
                    while r2+g2+b2 < min_total_intensity:
                        g2 = random.randrange(*colour_range)

            if b < b2:
                b+=1
            elif b > b2:
                b-=1
            else:
                b2 = random.randrange(*colour_range)
                if min_total_intensity != None and max_total_intensity != None:
                    while r2+g2+b2 < min_total_intensity or r2+g2+b2 > max_total_intensity:
                        b2 = random.randrange(*colour_range)
                elif min_total_intensity == None and max_total_intensity != None:
                    while r2+g2+b2 > max_total_intensity:
                        b2 = random.randrange(*colour_range)
                elif min_total_intensity != None and max_total_intensity == None:
                    while r2+g2+b2 < min_total_intensity:
                        b2 = random.randrange(*colour_range)
        start_x += xstep
        start_y += ystep

img.putpixel((START_X,START_Y),(r,g,b))

img.show()
end_t = time.time()
print("Drawing path complete, time elapsed:")
print(end_t-start_t,"s")