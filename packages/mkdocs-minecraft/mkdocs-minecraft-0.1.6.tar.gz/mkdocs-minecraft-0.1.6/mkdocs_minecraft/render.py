import os

from PIL import Image, ImageDraw, ImageFont

SLOTS = [
    217, 115,
    363, 115,
    506, 115,
    217, 257,
    363, 257,
    506, 257,
    217, 404,
    363, 404,
    506, 404
]

RESULT= [
    968, 257,
    1070, 330,
]

SLOT_SIZE = 120

class Recipe:
    pass


class CraftingRecipe(Recipe):
    def __init__(self, type, pattern, key, result):
        self.type = str(type)
        self.pattern = list(pattern)
        self.key = dict(key)
        self.result = CraftingRecipeResult(**result)

    def save_png(self, background_path, items_path, path):
        background = Image.open(background_path)
        image = Image.new('RGBA', size=background.size)
        image.paste(background, (0, 0))

        for i, line in enumerate(self.pattern):
            for j, char in enumerate(line):
                if not char or char == ' ':
                    continue

                slot = i * 3 + j
                x = SLOTS[slot * 2]
                y = SLOTS[slot * 2 + 1]

                item_resource_location = str(self.key[char]['item'])
                item_path = item_resource_location.replace(':', '/')
                item_full_path = os.path.join(items_path, item_path + '.png')

                item_texture = Image.open(item_full_path).convert('RGBA')
                item_texture = item_texture.resize((SLOT_SIZE, SLOT_SIZE), resample=Image.BILINEAR)

                image.paste(item_texture, (x, y), mask = item_texture)

        result_resource_location = str(self.result.item)
        result_path = result_resource_location.replace(':', '/')
        result_full_path = os.path.join(items_path, result_path + '.png')
        result_texture = Image.open(result_full_path).convert('RGBA')
        result_texture = result_texture.resize((SLOT_SIZE, SLOT_SIZE), resample=Image.BILINEAR)

        image.paste(result_texture, (RESULT[0], RESULT[1]), mask = result_texture)

        if self.result.count > 1:
            draw = ImageDraw.Draw(image)
            font_path = os.path.join(os.path.dirname(__file__),'./font/Minecraft.ttf')
            font = ImageFont.truetype(font=font_path, size=72)
            draw.text((RESULT[2], RESULT[3]), str(self.result.count), (255, 255, 255), font=font)

        image = image.resize((484,256))
        image.save(path, optimize=True)

class CraftingRecipeResult:
    def __init__(self, item, count = 1):
        self.item = item
        self.count = count