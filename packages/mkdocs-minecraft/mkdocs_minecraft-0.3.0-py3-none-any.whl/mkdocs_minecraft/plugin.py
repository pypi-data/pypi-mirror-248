import concurrent.futures
import hashlib
import os.path
import re
import json

from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, event_priority

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    pass

from .config import MinecraftConfig
from .render import CraftingRecipe, SmeltingRecipe


class MinecraftPlugin(BasePlugin[MinecraftConfig]):

    def __init__(self):
        self._executor = concurrent.futures.ThreadPoolExecutor(4)

    def on_config(self, config):
        self.docs_dir = config.docs_dir
        self.language_plugin = "i18n" in config.plugins
        self.background = os.path.abspath(os.path.join(os.path.dirname(__file__), 'textures', 'background.png'))
        self.background_smelting = os.path.abspath(os.path.join(os.path.dirname(__file__), 'textures', 'background_smelting.png'))
        self.items = [os.path.abspath(os.path.join(os.path.dirname(__file__), 'textures'))]

        if self.config.background_path:
            self.background = self.config.background_path

        if self.config.background_smelting_path:
            self.background_smelting = self.config.background_smelting_path

        if self.config.items_path:
            self.items.append(self.config.items_path)

        if "Image" not in globals():
            raise PluginError(
                "Required dependencies of \"minecraft\" plugin not found. "
                "Install with: pip install \"mkdocs-material[imaging]\""
            )

    @event_priority(100)
    def on_page_markdown(self, markdown, page, config, files):
        if not self.config.enabled:
            return

        pattern = re.compile(r'!\[(.*?)\]\(((.*?)\.json)\)', flags=re.IGNORECASE)

        directory = self.config.images_dir
        file, _ = os.path.splitext(page.file.src_path)

        page_directory = os.path.dirname(page.file.abs_src_path)

        def replace(reference):
            json_file_path = reference.group(2)

            reference_path = ''
            if not self.language_plugin:
                json_file_full_path = os.path.join(page_directory, json_file_path)
            else:
                json_file_full_path = os.path.join(page_directory, '../' + json_file_path)
                reference_path = '../'

            json_file_real_path = os.path.realpath(json_file_full_path)
            json_file = open(json_file_real_path, 'r')
            json_file_content = json_file.read()
            json_content = json.loads(json_file_content)
            json_file.close()

            hash = hashlib.md5(json_file_content.encode('utf-8')).hexdigest()
            reference_path = os.path.join(reference_path, directory, hash + '.png')
            image_path = os.path.join(config.site_dir, directory, hash + '.png')
            image_dir = os.path.dirname(image_path)
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            type = str(json_content.get('type'))
            if not os.path.exists(image_path):
                if type.startswith('minecraft:crafting'):
                #try:
                    recipe = CraftingRecipe(**json_content)
                    recipe.save_png(self.background, self.items, image_path)
                #except TypeError:
                    #pass
                elif type.startswith('minecraft:smelting'):
                    recipe = SmeltingRecipe(**json_content)
                    recipe.save_png(self.background_smelting, self.items, image_path)

            return f'![{hash}](../{reference_path})'

        markdown = re.sub(pattern, replace, markdown)

        return markdown