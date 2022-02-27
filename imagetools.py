import os
import random
from PIL import Image, ImageSequence, ImageEnhance, ImageDraw, ImageFont
from itertools import product

def tile(img, x, y):
    w, h = img.size
    dx = int(w / x)
    dy = int(h / y)
    grid = product(range(0, h-h%dy, dy), range(0, w-w%dx, dx))
    tiles = []
    for i, j in grid:
        box = (j, i, j+dx, i+dy)
        tiles.append(img.crop(box))
    return tiles

def desaturate(img):
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.46)
    return img

def find_font_size(text, font, image, target_width_ratio):
    def get_text_size(text, image, font):
        im = Image.new('RGB', (image.width, image.height))
        draw = ImageDraw.Draw(im)
        return draw.textsize(text, font)
    tested_font_size = 24
    tested_font = ImageFont.truetype(font, tested_font_size)
    observed_width, observed_height = get_text_size(text, image, tested_font)
    estimated_font_size = tested_font_size / (observed_width / image.width) * target_width_ratio
    return round(estimated_font_size)

def text(text, dimensions, y_pos, font="resources/veil/rip/alagard.ttf", font_size=24, font_color=(82,64,50,255)):
    fnt = ImageFont.truetype(font, font_size)
    txt = Image.new("RGBA", dimensions, (255,255,255,0))
    d = ImageDraw.Draw(txt)
    w, h = d.textsize(text)
    d.text((dimensions[0]/2, y_pos), text, font=fnt, fill=font_color, anchor="mm")
    return txt

def gif(frames, target, background=None, overlay=None, dim=(100, 100), transparent=False, duration=600):
    images = []
    icc = None
    for image in frames:
        image = image.convert('RGBA', dither=None)
        if background is not None:
            bg = Image.open(background).convert('RGBA', dither=None)
            bg.paste(image, (-4, 3), image)
        else:
            bg = image
        if overlay is not None:
            fg = Image.open(overlay).convert('RGBA', dither=None)
            bg.paste(fg, (0, 0), fg)
        final_image = bg if not None else image
        final_image = final_image.resize(dim, Image.NEAREST)
        images.append(final_image)
    if transparent:
        images[0].save(target, save_all=True, append_images=images[1:], optimize=False, quality=100, duration=duration, loop=0, transparency=0, disposal=2)
    else:
        images[0].save(target, save_all=True, append_images=images[1:], optimize=False, quality=100, duration=duration, loop=0)

def overlay(images, scale=1):
    bg = None
    for img, offset in images:
        if bg is not None:
            bg.paste(img, offset, img)
        else:
            size = (img.size[0]*scale, img.size[1]*scale)
            bg = img
    bg.resize(size, Image.NEAREST)
    return bg

def all_png(path):
    return [f for f in sorted(os.listdir(path)) if f.endswith('.png')]


###########################################################################################


def walkcycle(pirate):
    sprites = tile(Image.open(pirate.spritesheet), 4, 4)
    gif(sprites, pirate.walkcycle, duration=150, dim=(200,200), transparent=True)
