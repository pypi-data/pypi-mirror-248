import os

from PIL import Image, ImageDraw, ImageFont

class Recipe:
    def find_texture(self, items, item_resource_location):
        for items_path in reversed(items):
            item_path = item_resource_location.replace(':', '/')
            item_full_path = os.path.join(items_path, item_path + '.png')
            if os.path.exists(item_full_path):
                return item_full_path

        raise FileNotFoundError(fr'{item_resource_location}')


class CraftingRecipe(Recipe):
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
    RESULT = [
        968, 257,
        1070, 330,
    ]
    SLOT_SIZE = 120

    def __init__(self, **params):
        self.type = str(params['type'])
        self.pattern = list(params['pattern']) if 'pattern' in params else None
        self.key = dict(params['key']) if 'key' in params else None
        self.ingredients = list(params['ingredients']) if 'ingredients' in params else None
        self.result = CraftingRecipeResult(**params['result'])

    def save_png(self, background_path, items, path):
        background = Image.open(background_path)
        image = Image.new('RGBA', size=background.size)
        image.paste(background, (0, 0))

        if self.type == 'minecraft:crafting_shaped':
            for i, line in enumerate(self.pattern):
                for j, char in enumerate(line):
                    if not char or char == ' ':
                        continue

                    slot = i * 3 + j
                    x = self.SLOTS[slot * 2]
                    y = self.SLOTS[slot * 2 + 1]

                    item_full_path = self.find_texture(items, str(self.key[char]['item']))

                    item_texture = Image.open(item_full_path).convert('RGBA')
                    item_texture = item_texture.resize((self.SLOT_SIZE, self.SLOT_SIZE), resample=Image.BILINEAR)

                    image.paste(item_texture, (x, y), mask = item_texture)
        elif self.type =='minecraft:crafting_shapeless':
            for i, ingredient in enumerate(self.ingredients):
                x = self.SLOTS[i * 2]
                y = self.SLOTS[i * 2 + 1]

                item_full_path = self.find_texture(items, str(ingredient['item']))

                item_texture = Image.open(item_full_path).convert('RGBA')
                item_texture = item_texture.resize((self.SLOT_SIZE, self.SLOT_SIZE), resample=Image.BILINEAR)

                image.paste(item_texture, (x, y), mask = item_texture)

        result_full_path = self.find_texture(items, str(self.result.item))
        result_texture = Image.open(result_full_path).convert('RGBA')
        result_texture = result_texture.resize((self.SLOT_SIZE, self.SLOT_SIZE), resample=Image.BILINEAR)

        image.paste(result_texture, (self.RESULT[0], self.RESULT[1]), mask = result_texture)

        if self.result.count > 1:
            draw = ImageDraw.Draw(image)
            font_path = os.path.join(os.path.dirname(__file__),'./font/Minecraft.ttf')
            font = ImageFont.truetype(font=font_path, size=72)
            draw.text((self.RESULT[2], self.RESULT[3]), str(self.result.count), (255, 255, 255), font=font)

        image = image.resize((484,256))
        image.save(path, optimize=True)

class CraftingRecipeResult:
    def __init__(self, item, count = 1):
        self.item = item
        self.count = count

class SmeltingRecipe(Recipe):
    SLOT = [
        360, 100
    ]
    RESULT = [
        985, 257,
    ]
    SLOT_SIZE = 120

    def __init__(self, **params):
        self.type = str(params['type'])
        self.ingredient = dict(params['ingredient'])
        self.result = str(params['result'])

    def save_png(self, background_path, items, path):
        background = Image.open(background_path)
        image = Image.new('RGBA', size=background.size)
        image.paste(background, (0, 0))

        x = self.SLOT[0]
        y = self.SLOT[1]

        item_full_path = self.find_texture(items, str(self.ingredient['item']))

        item_texture = Image.open(item_full_path).convert('RGBA')
        item_texture = item_texture.resize((self.SLOT_SIZE, self.SLOT_SIZE), resample=Image.BILINEAR)

        image.paste(item_texture, (x, y), mask = item_texture)

        result_full_path = self.find_texture(items, str(self.result))
        result_texture = Image.open(result_full_path).convert('RGBA')
        result_texture = result_texture.resize((self.SLOT_SIZE, self.SLOT_SIZE), resample=Image.BILINEAR)

        image.paste(result_texture, (self.RESULT[0], self.RESULT[1]), mask = result_texture)

        image = image.resize((484,256))
        image.save(path, optimize=True)