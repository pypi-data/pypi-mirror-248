from mkdocs.config.base import Config
from mkdocs.config.config_options import Deprecated, Type


# Minecraft plugin configuration
class MinecraftConfig(Config):
    enabled = Type(bool, default=True)

    images_dir = Type(str, default="assets/images/minecraft")
    background_path = Type(str, default="")
    background_smelting_path = Type(str, default="")
    items_path = Type(str, default="")
