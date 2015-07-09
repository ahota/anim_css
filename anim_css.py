#!/usr/bin/env python
# Use CSS3 Animation to display animated GIFs the right way
# Alok
from PIL import Image
import sys, os

# Extract the frames from the GIF
def get_frames(file_path):
    print 'Extracting frames...'
    cur_frame = Image.open(file_path)
    palette   = cur_frame.getpalette()
    num_frame = 0
    frames = []
    while cur_frame:
        cur_frame.putpalette(palette)
        temp = Image.new('RGB', cur_frame.size)
        temp.paste(cur_frame)
        frames.append(temp)
        num_frame += 1
        try:
            cur_frame.seek(num_frame)
        except EOFError:
            break
    print 'Extracted', num_frame, 'frame' + 's' if num_frame > 1 else ''
    return frames

# Get the color for the pixel at x,y and convert to 6 digit hex string
def get_color(frame, x, y):
    color_tuple = frame.getpixel((x, y))
    result = ''.join([hex(v)[2:].zfill(2) for v in color_tuple])
    return result


if len(sys.argv) != 4:
    print 'Usage:', sys.argv[0], 'img_filename pixel_size fps'
    exit()

img_filename = sys.argv[1]
pixel_size = int(sys.argv[2])
fps = int(sys.argv[3])

frames = get_frames(img_filename)  # List of GIF's frames as Image objects
width, height = frames[0].size
duration = len(frames)/float(fps)  # Duration of animation based on user fps
delta = 100/len(frames)            # Percentage per frame (max 100 frames?)

print 'Building HTML file...'

# Build HTML header and open tags
of = os.path.splitext(img_filename)[0]
output = open(of+'.html', 'w')
output.write('<!DOCTYPE html>\n')
output.write('<html>\n')
output.write('<head>\n')
output.write('<style>\n')

# Base class for pixels
output.write('.pixel { width:'+str(pixel_size)+'px;\n')
output.write('height:'+str(pixel_size)+'px;\n')
output.write('background-color:white;\n')
output.write('-webkit-animation-duration: '+str(duration)+'s;\n')
output.write('-webkit-animation-iteration-count: infinite;\n')
output.write('animation-duration: '+str(duration)+'s;\n')
output.write('animation-iteration-count: infinite;\n')
output.write('}\n')

# Unique id for each pixel containing the colors to change to
for x in range(width):
    for y in range(height):
        name = 'x'+str(x)+'y'+str(y)
        output.write('#'+name+' {\n')
        output.write('position:absolute;\n')
        output.write('top:'+str(y*pixel_size)+'px;\n')
        output.write('left:'+str(x*pixel_size)+'px;\n')
        output.write('-webkit-animation-name: '+name+';\n')
        output.write('animation-name: '+name+';\n')
        output.write('}\n')

#webkit: chrome, safari, opera
for x in range(width):
    for y in range(height):
        name = 'x'+str(x)+'y'+str(y)
        output.write('@-webkit-keyframes '+name+' {\n')
        for i, f in enumerate(frames):
            output.write(str(i*delta)+'% {background-color:#'+
            get_color(f, x, y)+ ';}\n')
        output.write('}\n')

#standard: firefox, ie?
for x in range(width):
    for y in range(height):
        name = 'x'+str(x)+'y'+str(y)
        output.write('@keyframes '+name+' {\n')
        for i, f in enumerate(frames):
            output.write(str(i*delta)+'% {background-color:#'+
            get_color(f, x, y)+ ';}\n')
        output.write('}\n')

# Closing tags
output.write('</style>\n')
output.write('</head>\n')
output.write('<body>\n')

# Place the divs in the body
for x in range(width):
    for y in range(height):
        name = 'x'+str(x)+'y'+str(y)
        output.write('<div class=\"pixel\" id=\"'+name+'\"></div>\n')

# Close the HTML file
output.write('</body>\n')
output.write('</html>\n')
output.close()

print 'Done!'
