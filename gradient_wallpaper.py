#! /usr/bin/python3 -B

import sys
import matplotlib.pyplot as plt
import numpy as np

###############################################################################

def show_help():
    message = f'''\
Usage:
  python3 {sys.argv[0]} <h> <w> <r> <g> <b>
where <h> and <w> are the height and width of the image in pixels, and <r>, <g>
and <b> are integers in the range [0, 255], representing the intensities of the
red, green and blue components at the top left of the image.\
'''
    raise SystemExit(message)

###############################################################################

def main():
    try:
        (height, width, red, green, blue) = map(int, sys.argv[1 :])
    except ValueError:
        show_help()
    if height <= 0 or width <= 0 or not all(0 <= arg <= 255 for arg in (red, green, blue)):
        show_help()

    # Create a mask which fades from white at the top left to black at the top
    # right, bottom right and bottom left.
    (rows, cols) = (height, width)
    layer = np.zeros((0, cols))
    for start in np.linspace(1, 0, rows):
        layer = np.vstack((layer, np.linspace(start, 0, cols)))

    # Create a three-channel image from the mask.
    img = np.dstack((layer * red / 255, layer * green / 255, layer * blue / 255))
    plt.imshow(img)
    plt.show()

    message = '''\
Enter the name of the file to write the image to. Alternatively, press Enter
without typing anything to abort.
> \
'''
    response = input(message)
    if not response or response.isspace():
        print('Aborted.')
        return
    plt.imsave(response, img)

###############################################################################

if __name__ == '__main__':
    main()
