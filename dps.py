import os
from os import path
import re
import sys
import shutil
import urllib.request
import zipfile
import imageio
import asyncio
import random
from PIL import Image, ImageSequence, ImageEnhance, ImageDraw, ImageFont
import imagetools

class Pirate(object):
    def __init__(self, token_id, artwork_root):
        self.token_id = token_id
        self.artwork_root = artwork_root

    @property
    def spritesheet(self):
        return "{}/spritesheets/{}.png".format(self.artwork_root, self.token_id)

    @property
    def walkcycle(self):
        return "{}/{}-walkcycle.gif".format(self.artwork_root, self.token_id)
  

class PirateFactory:
    @staticmethod
    def get_pirate(token_id):
        path_artwork = "{}/artwork".format(os.getcwd())
        pirate = Pirate(token_id, path_artwork)
        try:
            imagetools.walkcycle(pirate)
        except Exception as e:
            print("Error loading {}: {}".format(token_id, str(e)))
            return None
        return pirate

async def get_pirates(pirates):
    for pirate in pirates:
        PirateFactory.get_pirate(pirate)

async def main(argv):
    if len(argv) == 0:
        print("Supply token id")
    else:
        if argv[0] == "--all":
            all_pirates = map(lambda i: str(i), range(1, 3001))
            await get_pirates(all_pirates)
        else:
            await get_pirates(argv)
            

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(main(sys.argv[1:]))
