# -*- coding: utf-8 -*-
#
# Copyright 2019 Christoph Wagner
#     https://www.tu-ilmenau.de/it-ems/
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
#  PURPOSE
#  =======
#  The purpose of Picasso is to modify images using a template or entering
#  modifications manually to make them more readable for example.
#
#  Requires: numpy, PIL
#
#  Author: Christoph Wagner, 04.01.2019, EMS Research Group TU Ilmenau
#  Coauthor: Johannes van Reimersdahl, 04.01.2019, EMS Research Group TU Ilmenau

import os
import sys
import ast
import re
import numpy
from PIL import Image
import PIL.ImageOps

def Picasso(imageref, outputname, commands, v):
    """
    Picasso is the slave to execute the steps given in the template or via
    cli inputs.

    Parameters:
    -----------
    imageref : str
        path of file
    outputname : str
        path of outputfile
    commands : list or tuple
        list of functions to be executed
    verbose : boolean
        boolean describing verbose set/unset

    Returns:
    -----------
    Nothing.
    """
    # Preparation
    if v: print("Preparation.")
    if os.path.isfile(imageref) != True:
        sys.exit("Sourcefile not found.")

    image = Image.open(imageref)
    name,ext = os.path.splitext(imageref)
    width,height = image.size
    if v: print("Width, Height: " + str(width) + " x " + str(height))
    rgb_image,a = detectimagemode(image)

    # Expand templates
    commands_expanded = []
    for i in commands:
        if os.path.isfile(i.strip()):
            print("Expanding template %s"% (i, ))
            with open(i, 'r') as template:
                commands_expanded.extend(template.read().splitlines())
        else:
            commands_expanded.append(i)

    # Executing commands
    if v: print("Processing commands %s"% (commands_expanded, ))

    for i in commands_expanded:
        # Remove leading and trailing whitespace characters (incl. tab, ...)
        i = i.strip()
        if "=" in i:
            tokens = [tt.strip() for tt in i.split('=')]
            if v and len(tokens) > 2:
                print("Excess arguments in command '%s'"% (i,))

            rgb_image = replacecolor(
                rgb_image, tokens[0], tokens[1], width, height
            )
        elif i == "invert" or i == "i":
            rgb_image = invert(rgb_image)
        elif i == "crop" or i == "c":
            image = merge(rgb_image,a)
            image = crop(image)
            width,height = image.size
            rgb_image, a = detectimagemode(image)
        else:
            if v: print("Command not understood: %s" %(i, ))

    # Steps to finish
    if v: print("Starting to save and name the output file.")
    if a != None:
        image = merge(rgb_image,a)
    else:
        image = rgb_image

    if outputname == "None" :
        outputname = name + "_modified" + ext

    image.save(outputname)
    image.close()
    print("Finished.")
    print("Saved & Closed.")
    if v: print("Filename: " + outputname)

def detectimagemode(image):
    """
    function to check the image mode and if the mode is RGB/RGBA returns
    variables to continue working with. Furthermore it splits an RGBA image
    into a RGB image and the alpha channel.

    Parameters:
    -----------
    imageref: str
        path to given image

    Returns:
    -----------
    rgb_image: tuple of (:py:class:`PIL.Image`, :py:class:`PIL.Image`)
        the (separated) RGB image to continue working with
    a: tuple of (:py:class:`PIL.Image`, :py:class:`PIL.Image`)
        the separated alpha channel or if non existent "None"
    """
    if v: print("Detecting image mode...")
    if image.mode == 'RGBA':
        r,g,b,a = image.split()
        rgb_image = Image.merge('RGB',(r,g,b))
    elif image.mode == 'RGB':
        rgb_image = imageref
        a = None
    else:
        sys.exit('Image is '+ image.mode + '. Needs to be RGB/RGBA.')
    print("Image mode: " + image.mode)
    return rgb_image,a

def invert(image):
    """"
    checks for image mode, then depending on result uses different
    algorithms to invert the image.

    Parameters:
    -----------
    image : tuple of (:py:class:`PIL.Image`, :py:class:`PIL.Image`)
        uninverted image

    Returns:
    -----------
    image : tuple of (:py:class:`PIL.Image`, :py:class:`PIL.Image`)
        inverted image
    """
    print("Inverting...")
    inverted_image = PIL.ImageOps.invert(image)
    image = inverted_image
    if v: print("Inverting finished.")
    return image

def replacecolor(image,color1,color2,width,height):
    """
    replaces a given color in an image with another color1

    Parameters:
    -----------
    image : tuple of (:py:class:`PIL.Image`, :py:class:`PIL.Image`)
        image to be modifed
    color1 : tuple or str
        color specifier of the color to be replaced
    color2 : tuple or str
        color specifier of the color to be replaced with
    Returns:
    -----------
    image : tuple of (:py:class:`PIL.Image`, :py:class:`PIL.Image`)
        image to be modifed
    """
    print("Replacing colors...")
    color1,color2 = translatecolors(color1,color2)
    px = image.load()
    for x in range(width):
        for y in range(height):
            if px[x,y] == color1:
                px[x,y] = color2
    rgb_image = image
    return image

def merge(rgb_image,a):
    """
    Merge merges the modified RGB image with the previously separated alpha
    channel.

    Parameters:
    -------------
    rgb_image : tuple of (:py:class:`PIL.Image`, :py:class:`PIL.Image`)
        previously modifed image
    a : tuple or str
        color specifier of the color to changed to to be replaced with

    Returns:
    ------------
    image : tuple of (:py:class:`PIL.Image`, :py:class:`PIL.Image`)
        merged RGBA image
    """
    if v: print("Merging...")
    r,g,b = rgb_image.split()
    image = Image.merge('RGBA',(r,g,b,a))
    return image

def translatecolors(color1,color2):
    """
    This function detects the format in which the color codes are given
    and translates them to an rgb tuple.

    Parameters:
    -------------
    color1 : tuple or str
        color specifier of the color to be changed to be translated
    color2 : tuple or str
        color specifier of the color to changed to to be replaced with

    Returns:
    ------------
    color1 : tuple
        color specifier of the color to be replaced
    color2 : tuple
        color specifier of the color to be replaced with
    """
    getcolor = PIL.ImageColor.getrgb
    if v:
        print("Colors before translating:" + str(color1) + ", " + str(color2))
    if isinstance(color1,tuple):
        rgbcolor1 = color1
    elif isinstance(color2,tuple):
        rgbcolor2 = color2
    else:
        rgbcolor1 = getcolor(color1)
        rgbcolor2 = getcolor(color2)
    if v:
        print("Translated colors:" + str(rgbcolor1) + ", " + str(rgbcolor2))
    return rgbcolor1,rgbcolor2

def crop(image):
    """
    This function crops the image to a square concentric to the border of the
    image.

    Parameters:
    -------------
    image : tuple of (:py:class:`PIL.Image`, :py:class:`PIL.Image`)
        image to be cropped

    Returns:
    ------------
    image_out : tuple of (:py:class:`PIL.Image`, :py:class:`PIL.Image`)
        cropped image
    """
    px = image.load()
    picture = numpy.array(image)
    # reduce to RGB (discard extra channels like alpha, etc.) and determine max
    intensity = picture[:, :, :3].max(axis=2)
    # now determine row and column intensities and fild out which of them lie
    # above a specified threshold _in pixel average_
    threshold = intensity.max() // 2
    idxX = numpy.where(numpy.mean(intensity, axis=1) > threshold)[0]
    idxY = numpy.where(numpy.mean(intensity, axis=0) > threshold)[0]
    if idxX.size < 2 or idxY.size < 2:
        raise ValueError("Threshold too high for cropping.")

    picture_out = picture[
        idxX.min():idxX.max() + 1, idxY.min():idxY.max() + 1, :
    ]

    image_out = Image.fromarray(picture_out)
    return image_out
