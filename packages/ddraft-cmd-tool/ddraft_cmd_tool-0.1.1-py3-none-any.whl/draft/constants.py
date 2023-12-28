import os

TYPES = [
    'cave',
    'light',
    'material',
    'object',
    'path',
    'normal-pattern',
    'colorable-pattern',
    'portal',
    'roof',
    'terrain',
    'simple-tileset',
    'smart-tileset',
    'smart-double-tileset',
    'wall',
]
CWD = os.getcwd()
ASSET_FILETYPE_SUFFIXES = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".dungeondraft_wall",
    ".dungeondraft_tileset",
    ".dungeondraft_tags",
    ".json"
)

# The order of this is used ot establish preference when intended asset filetype is ambiguous
ASSET_TEXTURE_FILETYPE_SUFFIXES = (
    ".png",
    ".webp",
    ".jpg",
    ".jpeg",
)
