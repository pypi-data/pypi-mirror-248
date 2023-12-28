from __future__ import annotations

import configparser
import json
import logging
import os
import pathlib
import shutil
import struct
from hashlib import md5

from PIL import Image

from draft import utils
from draft.constants import TYPES, CWD, ASSET_FILETYPE_SUFFIXES, ASSET_TEXTURE_FILETYPE_SUFFIXES
from draft.exceptions import AssetNotFoundException, \
    UnknownAssetType, AssetCreationException, InvalidTagStructure

logger = logging.getLogger(__name__)


def gen_pack_id() -> bytes:
    import string
    from random import choices
    char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits
    id_length = 8
    pack_id = ''.join(choices(char_set, k=id_length)).encode(encoding="utf-8")
    return pack_id


def list_assets():
    asset_list = []
    project_root = utils.get_project_root(CWD)
    for asset_type in TYPES:
        asset_type_dir = pathlib.Path(os.path.join(project_root, 'unpacked-asset-tree',
                                                   'textures', type2dirname(asset_type)))
        for entry in asset_type_dir.iterdir():
            if entry.is_file():
                if entry.suffix not in ASSET_FILETYPE_SUFFIXES:
                    # Some other file that is not an asset, like .gitignore
                    continue
                if asset_type == "wall" and \
                        any([str(entry).endswith(f'_end{suffix}') for
                             suffix in ASSET_TEXTURE_FILETYPE_SUFFIXES]):
                    # A wall end
                    continue
                name = entry.stem
            else:
                name = entry.name

            asset_list.append({
                'asset_type': asset_type,
                'asset_name': name
            })

    return asset_list

def replace_asset(asset_type, asset_key_name, path_to_asset,
              color="ffffff", custom_color=False):
    if asset_type not in TYPES:
        raise UnknownAssetType(f"Error: Unknown Asset Type: {asset_type}")

    project_root = utils.get_project_root(CWD)
    path_to_asset = pathlib.Path(path_to_asset)

    if not path_to_asset.exists():
        raise AssetNotFoundException

    # There is a better, but much more verbose way of doing this which basically involves
    # only replacing the images and not the meta-data. But this would involve custom functions,
    # for various asset types. Might do that anyway at some poitn.
    remove_asset(asset_type, asset_key_name)
    add_asset(asset_type, asset_key_name, color=color, custom_color=custom_color)


def add_asset(asset_type, asset_key_name, path_to_asset,
              color="ffffff", custom_color=False):
    if asset_type not in TYPES:
        raise UnknownAssetType(f"Error: Unknown Asset Type: {asset_type}")

    project_root = utils.get_project_root(CWD)
    path_to_asset = pathlib.Path(path_to_asset)

    if not path_to_asset.exists():
        raise AssetNotFoundException

    def default_func():
        try:
            asset_type_dir = project_root / 'unpacked-asset-tree' / 'textures' / type2dirname(asset_type)
            asset = asset_type_dir / f'{asset_key_name}{path_to_asset.suffix}'
            shutil.copy(path_to_asset, asset)
        except OSError as e:
            logger.error(e)
            logger.error('Aborting operation.')
            raise AssetCreationException

    # def add_object(tag_name=None, colorable=False):
    #     # This is not a simple asset, since they are associated with tags
    #     try:
    #         asset_type_dir = project_root / 'unpacked-asset-tree' / 'textures' / type2dirname(asset_type)
    #         asset = asset_type_dir / f'{asset_key_name}{path_to_asset.suffix}'
    #         shutil.copy(path_to_asset, asset)
    #     except OSError as e:
    #         logger.error(e)
    #         logger.error('Aborting operation.')
    #         raise AssetCreationException
    #     default_func()
    #     if tag_name is not None:
    #         tag_objects(
    #             tag_name,
    #             [pathlib.Path(f'textures/{type2dirname(asset_type)}/{asset_key_name}{path_to_asset.suffix}')],
    #             colorable)

    def add_cave():
        # This is not a simple asset, since it is a directory
        asset_type_dir = project_root / 'unpacked-asset-tree' / 'textures' / type2dirname(asset_type)
        asset_dir = asset_type_dir / asset_key_name

        # There should be a wall image and a floor image, of some kind; ideally, only one of each kind.
        # But of course, we cannot depend on that, so we'll establish a preference order, implicit in the
        # order of the assets in constants; alternatively we could raise an exception.
        cave_asset = {
            'wall': {s: [] for s in ASSET_TEXTURE_FILETYPE_SUFFIXES},
            'floor': {s: [] for s in ASSET_TEXTURE_FILETYPE_SUFFIXES}
        }
        for entry in path_to_asset.iterdir():
            if entry.is_file() and \
                    entry.suffix in ASSET_TEXTURE_FILETYPE_SUFFIXES and \
                    entry.stem in ('wall', 'floor'):
                cave_asset[entry.stem][entry.suffix] = entry
        asset_found = False
        for filetype in ASSET_TEXTURE_FILETYPE_SUFFIXES:
            if cave_asset['wall'][filetype] and cave_asset['floor'][filetype]:
                source_wall = cave_asset['wall'][filetype]
                source_floor = cave_asset['floor'][filetype]
                asset_found = True
                break
        if not asset_found:
            raise AssetNotFoundException

        try:
            asset_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(source_floor, asset_dir / f'floor{source_floor.suffix}')
            shutil.copy(source_wall, asset_dir / f'wall{source_wall.suffix}')
        except (OSError, FileExistsError) as e:
            logger.error(e)
            logger.error('Aborting operation.')
            try:
                os.remove(asset_dir)
            except FileNotFoundError:
                pass
            raise AssetCreationException

    def add_material():
        asset_type_dir = project_root / 'unpacked-asset-tree' / \
                         'textures' / type2dirname(asset_type)
        dest_tile_asset = asset_type_dir / f'{asset_key_name}_tile{path_to_asset.suffix}'
        dest_border_asset = asset_type_dir / f'{asset_key_name}_border{path_to_asset.suffix}'

        # There should be a _tile and a _border pair of files; all of them in this directory.
        if path_to_asset.stem.endswith('_tile'):
            src_tile = path_to_asset
            src_border = path_to_asset.parent / \
                         f'{path_to_asset.stem[0:-5]}_border{path_to_asset.suffix}'
        if path_to_asset.stem.endswith('_border'):
            src_border = path_to_asset
            src_tile = path_to_asset.parent / \
                       f'{path_to_asset.stem[0:-7]}_tile{path_to_asset.suffix}'

        if not src_tile.exists() or not src_border.exists():
            raise AssetNotFoundException

        try:
            shutil.copy(src_tile, dest_tile_asset)
            shutil.copy(src_border, dest_border_asset)
        except OSError as e:
            logger.error(e)
            logger.error('Aborting operation')
            # Try to clean up
            for f in [dest_tile_asset, dest_border_asset]:
                try:
                    os.remove(f)
                except OSError:
                    pass
            raise AssetCreationException


    def add_wall():
        textures_path_fragment = pathlib.Path('textures') / type2dirname(asset_type)
        asset_type_dir = project_root / 'unpacked-asset-tree' / textures_path_fragment
        dest_wall = asset_type_dir / f'{asset_key_name}{path_to_asset.suffix}'
        dest_wall_end = os.path.join(asset_type_dir, f'{asset_key_name}_end{path_to_asset.suffix}')
        dest_meta_file = os.path.join(project_root, 'unpacked-asset-tree', 'data', type2dirname(asset_type),
                                      f'{asset_key_name}.dungeondraft_wall')

        if path_to_asset.stem.endswith('_end'):
            src_wall_end = path_to_asset
            src_wall = path_to_asset.parent / f'{path_to_asset.stem}{path_to_asset.suffix}'
        else:
            src_wall_end = path_to_asset.parent / f'{path_to_asset.stem}_end{path_to_asset.suffix}'
            src_wall = path_to_asset

        if not src_wall.exists() or not src_wall_end.exists():
            raise AssetNotFoundException

        try:
            shutil.copy(src_wall, dest_wall)
            shutil.copy(src_wall_end, dest_wall_end)
            with open(dest_meta_file, 'w') as fh:
                d = {
                    'path': str(textures_path_fragment / f'{asset_key_name}{path_to_asset.suffix}'),
                    'color': color
                }
                s = json.dumps(d, indent=4)
                print(s, file=fh)
        except (OSError, json.JSONDecodeError) as e:
            logger.error(e)
            logger.error('Aborting operation.')
            # We'll try to clean up
            for f in [dest_wall, dest_wall_end, dest_meta_file]:
                try:
                    os.remove(f)
                except OSError:
                    pass
            raise AssetCreationException(e)

    def add_tileset():
        textures_subpath = pathlib.Path('textures') / \
                                 type2dirname(asset_type) / f'{asset_key_name}{path_to_asset.suffix}'
        asset = pathlib.Path(project_root) / 'unpacked-asset-tree' / textures_subpath
        dest_meta_file = os.path.join(project_root, 'unpacked-asset-tree', 'data', 'tilesets',
                                      f'{asset_key_name}.dungeondraft_tileset')
        try:
            shutil.copy(path_to_asset, asset)
            with open(dest_meta_file, 'w') as fh:
                d = {
                    'path': str(textures_subpath),
                    'name': asset_key_name,
                    'type': 'custom_color' if custom_color else 'normal',
                    'color': color
                }
                s = json.dumps(d, indent=4)
                print(s, file=fh)
        except (OSError, json.JSONDecodeError) as e:
            logger.error(e)
            logger.error('Aborting operation.')
            # We'll try to clean up
            for f in [asset, dest_meta_file]:
                try:
                    os.remove(f)
                except OSError:
                    pass
            raise AssetCreationException

    # Run matching function
    {
        'cave': add_cave,
        'light': default_func,
        'material': add_material,
        'object': default_func,
        'path': default_func,
        'normal-pattern': default_func,
        'colorable-pattern': default_func,
        'portal': default_func,
        'roof': default_func,
        'terrain': default_func,
        'simple-tileset': add_tileset,
        'smart-tileset': add_tileset,
        'smart-double-tileset': add_tileset,
        'wall': add_wall,
    }[asset_type]()


def remove_asset(asset_type, asset_key_name):
    if asset_type not in TYPES:
        raise UnknownAssetType(f"Error: Unknown Asset Type: {asset_type}")

    project_root = utils.get_project_root(CWD)

    def default_func():
        asset_type_dir = project_root / 'unpacked-asset-tree' / \
                         'textures' / type2dirname(asset_type)
        assets = [asset_type_dir / f'{asset_key_name}{suffix}' for suffix
                  in ASSET_TEXTURE_FILETYPE_SUFFIXES]
        for asset in assets:
            try:
                os.remove(asset)
            except FileNotFoundError:
                # Not going to throw an exception, because if it is not there, it is not there
                # but since we don't know the suffix, we aren't going to log anything either.
                pass

    def rm_tileset():
        # Not a simple asset; first remove tileset image and then remove meta-data file
        asset = os.path.join(project_root, 'unpacked-asset-tree', 'textures',
                             type2dirname(asset_type), f'{asset_key_name}.png')
        try:
            os.remove(asset)
        except FileNotFoundError:
            logger.warning(f'File not found: {asset}')

        meta_file = (project_root / 'unpacked-asset-tree' / 'data' /
                     'tilesets' / f'{asset_key_name}.dungeondraft_tileset')
        try:
            os.remove(meta_file)
        except FileNotFoundError:
            logger.warning(f'File not found: {asset}')

    def rm_material():
        asset_type_dir = project_root / 'unpacked-asset-tree' / \
                         'textures' / type2dirname(asset_type)
        tile_assets = [asset_type_dir / f'{asset_key_name}_tile{suffix}' for suffix
                  in ASSET_TEXTURE_FILETYPE_SUFFIXES]
        border_assets = [asset_type_dir / f'{asset_key_name}_border{suffix}' for suffix
                       in ASSET_TEXTURE_FILETYPE_SUFFIXES]
        for tile_asset, border_asset in zip(tile_assets, border_assets):
            try:
                os.remove(tile_asset)
            except FileNotFoundError:
                pass
            try:
                os.remove(border_asset)
            except FileNotFoundError:
                pass



    def rm_cave():
        # This is not a simple asset, since it is a directory
        asset_type_dir = os.path.join(project_root, 'unpacked-asset-tree', 'textures',
                                      type2dirname(asset_type))
        asset = os.path.join(asset_type_dir, asset_key_name)
        # We use shutil.rmtree because a cave asset is a directory
        try:
            shutil.rmtree(asset)
        except FileNotFoundError:
            logger.warning(f'File not found: {asset}')

    def rm_wall():
        # This is not a simple asset; first remove wall files and then remove meta-data file
        asset_type_dir = os.path.join(project_root, 'unpacked-asset-tree', 'textures',
                                      type2dirname(asset_type))
        wall = os.path.join(asset_type_dir, f'{asset_key_name}.png')
        wall_end = os.path.join(asset_type_dir, f'{asset_key_name}_end.png')
        meta_file = os.path.join(project_root, 'data', type2dirname(asset_type),
                                 f'{asset_key_name}.dungeondraft_wall')
        try:
            os.remove(wall)
        except FileNotFoundError:
            logger.warning(f'File not found: {wall}')

        try:
            os.remove(wall_end)
        except FileNotFoundError:
            logger.warning(f'File not found: {wall_end}')

        try:
            os.remove(meta_file)
        except FileNotFoundError:
            logger.warning(f'File not found: {meta_file}')

    # Run matching function
    {
        'cave': rm_cave,
        'light': default_func,
        'material': rm_material,
        'object': default_func,
        'path': default_func,
        'normal-pattern': default_func,
        'colorable-pattern': default_func,
        'portal': default_func,
        'roof': default_func,
        'terrain': default_func,
        'simple-tileset': rm_tileset,
        'smart-tileset': rm_tileset,
        'smart-double-tileset': rm_tileset,
        'wall': rm_wall,
    }[asset_type]()


def type2dirname(asset_type):
    dirname = {
        'cave': 'caves',
        'light': 'lights',
        'material': 'materials',
        'object': 'objects',
        'path': 'paths',
        'normal-pattern': os.path.join('patterns', 'normal'),
        'colorable-pattern': os.path.join('patterns', 'colorable'),
        'portal': 'portals',
        'roof': 'roofs',
        'terrain': 'terrain',
        'simple-tileset': os.path.join('tilesets', 'simple'),
        'smart-tileset': os.path.join('tilesets', 'smart'),
        'smart-double-tileset': os.path.join('tilesets', 'smart_double'),
        'wall': 'walls',
    }[asset_type]
    return dirname


def init(new_project_root, pack_name='', author='', pack_id='', packed_assets_dir='', create_workspace=False):
    # Create and assign workspace directory
    new_project_root = pathlib.Path(new_project_root).expanduser().resolve()
    if create_workspace:
        workspace_dir = new_project_root / 'workspace'
        workspace_dir.mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'drafts' / 'caves').mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'drafts' / 'lights').mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'drafts' / 'materials').mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'drafts' / 'objects').mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'drafts' / 'paths').mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'drafts' / 'patterns' / 'normal').mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'drafts' / 'patterns' / 'colorable').mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'drafts' / 'portals').mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'drafts' / 'roofs').mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'drafts' / 'terrains').mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'drafts' / 'tilesets' / 'simple').mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'drafts' / 'tilesets' / 'smart').mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'drafts' / 'tilesets' / 'smart_double').mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'drafts' / 'walls').mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'resources').mkdir(parents=True, exist_ok=True)
        (workspace_dir / 'notes').mkdir(parents=True, exist_ok=True)
    else:
        workspace_dir = ''

    # Create directory tree structure scanned to create packs
    asset_root = new_project_root / 'unpacked-asset-tree'
    (asset_root / 'data' / 'tilesets').mkdir(parents=True, exist_ok=True)
    (asset_root / 'data' / 'walls').mkdir(parents=True, exist_ok=True)
    (asset_root / 'textures' / 'caves').mkdir(parents=True, exist_ok=True)
    (asset_root / 'textures' / 'lights').mkdir(parents=True, exist_ok=True)
    (asset_root / 'textures' / 'materials').mkdir(parents=True, exist_ok=True)
    (asset_root / 'textures' / 'objects').mkdir(parents=True, exist_ok=True)
    (asset_root / 'textures' / 'paths').mkdir(parents=True, exist_ok=True)
    (asset_root / 'textures' / 'patterns' / 'normal').mkdir(parents=True, exist_ok=True)
    (asset_root / 'textures' / 'patterns' / 'colorable').mkdir(parents=True, exist_ok=True)
    (asset_root / 'textures' / 'portals').mkdir(parents=True, exist_ok=True)
    (asset_root / 'textures' / 'roofs').mkdir(parents=True, exist_ok=True)
    (asset_root / 'textures' / 'terrain').mkdir(parents=True, exist_ok=True)
    (asset_root / 'textures' / 'tilesets' / 'simple').mkdir(parents=True, exist_ok=True)
    (asset_root / 'textures' / 'tilesets' / 'smart').mkdir(parents=True, exist_ok=True)
    (asset_root / 'textures' / 'tilesets' / 'smart_double').mkdir(parents=True, exist_ok=True)
    (asset_root / 'textures' / 'walls').mkdir(parents=True, exist_ok=True)

    # Create and assign directory to store packed assets
    if not packed_assets_dir:
        packed_assets_dir = new_project_root / 'packed-assets'
        json_packed_assets_path = 'packed-assets'
    else:
        # If caller proves an asset pack path this if it is a subdirectory of the project
        # we'll use a relative path (to avoid breaking paths if project is moved),
        # otherwise we'll use full path.
        proposed = pathlib.Path(packed_assets_dir).expanduser().resolve()
        if os.path.commonpath([new_project_root, proposed]) == str(new_project_root):
            relative_path = proposed.relative_to(new_project_root)
            packed_assets_dir = new_project_root / relative_path
            json_packed_assets_path = str(relative_path)
        else:
            packed_assets_dir = proposed
            json_packed_assets_path = str(packed_assets_dir)
    if not packed_assets_dir.exists():
        packed_assets_dir.mkdir(parents=True, exist_ok=True)

    # Create a config directory and file for this project
    draft_app_dir = os.path.join(new_project_root, '.draft')
    if not os.path.exists(draft_app_dir):
        os.mkdir(draft_app_dir)
    config = configparser.ConfigParser()
    config['PROJECT'] = {
        'name': pack_name,
        'id': pack_id,
        'author': author,
        'workspace': 'workspace' if create_workspace else '',
        'packed_assets_dir': json_packed_assets_path,
    }
    with open(os.path.join(new_project_root, '.draft', 'config.ini'), 'w') as fh:
        config.write(fh)


def call_pack(packed_assets_dir, name, pack_id, author, version_str):
    # Create a pack.json file
    # Scan source directory; ignore any pack.json file there; always overwrites.
    # Prepend pack.json to the file list.
    # Write file using struct
    #   Godot Engine's package format is specified as:
    #
    #     | Value/Type | Description                                                  |
    #     | ---------- | ------------------------------------------------------------ |
    #     | 0x43504447 | Magic number (GDPC)                                          |
    #     | 4 x Int32  | Engine version: version, major, minor, revision              |
    #     | 16 x Int32 | Reserved space, all 0s                                       |
    #     | Int32      | Number of files that going into the pack                     |
    #     |----- Begin of file index, each entry has the following structure     ---- |
    #     | Int32      | Length of path string                                        |
    #     | String     | e.g. res://packs/xnkiMHyh/data/default.dungeondraft_tags'    |
    #     | Int64      | File offset in bytes from beginning of pack file             |
    #     | Int64      | File size in bytes                                           |
    #     | 16 bytes   | MD5 (a hash isn't actually used; should be all 0s            |
    #     |            | ----- Begin of file contents -----                           |
    #     | append each file's binary data in order specified in index, at offsets    |
    #     | specified in file index                                                   |
    #     The source code of the .pck packer can be found [here](https://github.com/godotengine/godot/blob/master/core/io/pck_packer.cpp)

    project_root = utils.get_project_root(CWD)
    unpacked_assets_tree = os.path.abspath(os.path.expanduser(project_root / 'unpacked-asset-tree'))
    packed_assets_dir = os.path.abspath(os.path.expanduser(packed_assets_dir))
    base_prefix = 'res://packs'
    resource_path_prefix = os.path.join(base_prefix, pack_id)
    target_pack_file = os.path.join(packed_assets_dir, f'{name}-{pack_id}-{author}-{version_str}.dungeondraft_pack')
    target_source_json_file = os.path.join(unpacked_assets_tree, 'pack.json')
    if not os.path.exists(target_source_json_file):
        logger.debug('Creating new pack.json')
        with open(target_source_json_file, 'w') as fh:
            fh.write(json.dumps(
                {
                    'name': name,
                    'id': pack_id,
                    'version': version_str,
                    'author': author,
                    "keywords": "",
                    "allow_3rd_party_mapping_software_to_read": False,
                    "custom_color_overrides": {
                        "enabled": False,
                        "min_redness": 0.1,
                        "min_saturation": 0,
                        "red_tolerance": 0.04
                    }

                }, indent='\t') + '\n'
                     )
    else:
        logger.debug(f'Updating existing pack.json with name = {name}, '
                     f'author = {author}, id = {pack_id}, and '
                     f'version = {version_str}')
        with open(target_source_json_file, 'r') as fh:
            j = json.loads(fh.read())
        j['name'] = name
        j['author'] = author
        j['id'] = pack_id
        j['version'] = version_str
        with open(target_source_json_file, 'w') as fh:
            fh.write(json.dumps(j, indent='\t') + '\n')
    temp_offset = 0

    # Pack JSON files
    # Dungeondraft seems to add the JSON file twice, with different names, as follows.
    # I suspect only the first is actually required. But we'll keep it as similar as we can.
    logger.debug('Adding pack JSON files')
    in_pack_path = os.path.join(base_prefix, f'{pack_id}.json').replace('\\', '/')
    file_list = [
        {
            'source_path': target_source_json_file,
            'pack_path': in_pack_path,
            'length_of_path_string': len(in_pack_path),
            'file_size': os.path.getsize(target_source_json_file),
            'file_offset': temp_offset,
            'md5': bytes(16)
        }
    ]
    temp_offset += file_list[0]['file_size']

    in_pack_path = os.path.join(resource_path_prefix, 'pack.json').replace('\\', '/')
    file_list.append(
        {
            'source_path': target_source_json_file,
            'pack_path': in_pack_path,
            'length_of_path_string': len(in_pack_path),
            'file_size': os.path.getsize(target_source_json_file),
            'file_offset': temp_offset,
            'md5': bytes(16)
        }
    )
    temp_offset += file_list[1]['file_size']

    # Data files
    logger.debug('Adding data files')
    source_data_dir = os.path.join(os.path.join(unpacked_assets_tree, 'data'))
    for root, _, dir_files in os.walk(source_data_dir):
        for file in dir_files:
            _, ext = os.path.splitext(file)
            if ext not in ASSET_FILETYPE_SUFFIXES:
                continue
            p = os.path.join(root, file)
            asset_subpath = p[len(unpacked_assets_tree) + 1:]
            in_pack_path = os.path.join(resource_path_prefix, asset_subpath).replace('\\', '/')
            logger.debug(f'in_pack_path = {in_pack_path}')
            file_size = os.path.getsize(p)
            file_list.append(
                {
                    'source_path': os.path.join(root, file),
                    'pack_path': in_pack_path,
                    'length_of_path_string': len(in_pack_path),
                    'file_size': file_size,
                    'file_offset': temp_offset,
                    'md5': bytes(16)
                }
            )
            logger.debug(file_list[-1])
            temp_offset += file_size

    # Texture files
    logger.debug('Adding texture files')
    source_texture_dir = os.path.join(unpacked_assets_tree, 'textures')
    for root, _, dir_files in os.walk(source_texture_dir):
        for file in dir_files:
            _, ext = os.path.splitext(file)
            if ext not in ASSET_FILETYPE_SUFFIXES:
                continue
            p = os.path.join(root, file)
            logger.debug(f'p = {p}')
            asset_subpath = p[len(unpacked_assets_tree) + 1:]
            in_pack_path = os.path.join(resource_path_prefix, asset_subpath).replace('\\', '/')
            logger.debug(f'in_pack_path = {in_pack_path}')
            file_size = os.path.getsize(p)
            file_list.append(
                {
                    'source_path': p,
                    'pack_path': in_pack_path,
                    'length_of_path_string': len(in_pack_path),
                    'file_size': file_size,
                    'file_offset': temp_offset,
                    'md5': bytes(16)
                }
            )
            logger.debug(file_list[-1])
            temp_offset += file_size

    # Thumbnails
    # To generate the thumbnail file name:
    # hashlib.md5(in_pack_path).hexdigest() + file extension
    # where in_pack_path = e.g. 'res://packs/fQzpqQHC/textures/objects/sample_cauldron.png'
    # where fQzpgQHC is the pack-id.
    source_thumbnail_dir = os.path.join(unpacked_assets_tree, 'thumbnails')
    if os.path.exists(source_thumbnail_dir):
        logger.debug('Adding thumbnails')
    for root, _, dir_files in os.walk(source_thumbnail_dir):
        for file in dir_files:
            _, ext = os.path.splitext(file)
            if ext not in ASSET_FILETYPE_SUFFIXES:
                continue
            p = os.path.join(root, file)
            logger.debug(f'p = {p}')
            asset_subpath = p[len(unpacked_assets_tree) + 1:]
            in_pack_path = os.path.join(resource_path_prefix, asset_subpath).replace('\\', '/')
            logger.debug(f'in_pack_path = {in_pack_path}')
            file_size = os.path.getsize(p)
            file_list.append(
                {
                    'source_path': p,
                    'pack_path': in_pack_path,
                    'length_of_path_string': len(in_pack_path),
                    'file_size': file_size,
                    'file_offset': temp_offset,
                    'md5': bytes(16)
                }
            )
            logger.debug(file_list[-1])
            temp_offset += file_size

    # Calculate offsets in prep for writing
    pre_file_offset = sum([
        4,  # MAGIC
        16,  # Version
        64,  # Reserved
        4,  # Filecount
    ])
    for file in file_list:
        pre_file_offset += sum([
            4,  # String Length as Int32
            file['length_of_path_string'],
            8,  # File offset as Int64
            8,  # File size as Int64
            16,  # MD5 as 16 bytes
        ])

    # Now we add the pre_file_offset to each file's offset
    for file in file_list:
        file['file_offset'] += pre_file_offset

    with open(target_pack_file, 'wb') as fh:
        # Write Magic Number: 0x43504447 (GDPC)
        b = struct.pack('<cccc', b'G', b'D', b'P', b'C')
        fh.write(b)

        # Write Godo Pack Version: 4 x Int32  | Engine version: version, major, minor, revision
        b = struct.pack('<IIII', 1, 3, 4, 2)
        fh.write(b)

        # Write reserved space: 16 x Int32 | Reserved space, 0
        b = struct.pack('<16I', *([0] * 16))
        fh.write(b)

        # Write number of files in archive: Int32
        b = struct.pack('<I', len(file_list))
        fh.write(b)

        for file in file_list:
            fh.write(struct.pack('<I', file['length_of_path_string']))
            fh.write(file['pack_path'].encode('utf-8'))
            fh.write(struct.pack('<Q', file['file_offset']))
            fh.write(struct.pack('<Q', file['file_size']))
            fh.write(file['md5'])

        for file in file_list:
            with open(file['source_path'], 'rb') as sf:
                fh.write(sf.read())


def inspect(pack_file):
    if not os.path.exists(pack_file):
        raise FileNotFoundError(f'Could not find: {pack_file}')
    with open(pack_file, 'rb') as fh:
        data = fh.read()
    index = 0
    magic = struct.unpack_from('<cccc', data, offset=index)
    index += struct.calcsize('<cccc')

    godot_version = struct.unpack_from('<IIII', data, index)
    index += struct.calcsize('<IIII')

    reserved_buffer = struct.unpack_from('<16I', data, index)
    index += struct.calcsize('<16I')

    number_of_files = struct.unpack_from('<I', data, index)[0]
    index += struct.calcsize('<I')

    s = {
        'magic': magic,
        'reserved': reserved_buffer,
        'godot_version': godot_version,
        'number_of_files': number_of_files,
        'file_headers': []
    }
    logger.debug(s)
    for i in range(number_of_files):
        length_of_filepath_string = struct.unpack_from('<I', data, index)[0]
        index += struct.calcsize('<I')

        filepath_string = data[index:(index + length_of_filepath_string)]
        index += length_of_filepath_string

        file_offset = struct.unpack_from('<Q', data, index)[0]
        index += struct.calcsize('<Q')

        file_size = struct.unpack_from('<Q', data, index)
        index += struct.calcsize('<Q')

        md5junk = data[index:(index + 16)]
        index += 16

        s['file_headers'].append({
            'length': length_of_filepath_string,
            'path': str(filepath_string, 'utf8'),
            'file_offset': file_offset,
            'file_size': file_size,
            'md5': md5junk
        })
        logger.debug(s['file_headers'][i])
    return s


def thumbify(pack_id, no_delete, width):
    project_root = utils.get_project_root(CWD)
    asset_root = project_root / 'unpacked-asset-tree'
    thumbs_dir = project_root / 'unpacked-asset-tree' / 'thumbnails'

    if not thumbs_dir.exists():
        logger.debug('Creating new thumbnail directory.')
        thumbs_dir.mkdir()

    simple_tilesets_dir: pathlib.Path = asset_root / 'textures' / 'tilesets' / 'simple'
    smart_tilesets_dir: pathlib.Path = asset_root / 'textures' / 'tilesets' / 'smart'
    smartdouble_tilesets_dir: pathlib.Path = asset_root / 'textures' / 'tilesets' / 'smart_double'
    terrain_dir: pathlib.Path = asset_root / 'textures' / 'terrain'
    materials_dir: pathlib.Path = asset_root / 'textures' / 'materials'

    # Do terrains
    if not terrain_dir.exists():
        logger.debug('No terrain directory')
    else:
        logger.debug('Creating thumbnails for terrains')
    for source_texture in terrain_dir.iterdir():
        if not source_texture.suffix in ASSET_TEXTURE_FILETYPE_SUFFIXES:
            continue
        in_pack_path = f'res://packs/{pack_id}/textures/terrain/{source_texture.stem}.png'
        target_filename = thumbs_dir / f'{md5(in_pack_path.encode("utf8")).hexdigest()}.png'
        if target_filename.exists() and no_delete:
            continue
        create_thumbnail(width, source_texture, target_filename)

    # Do simple tilesets
    if not simple_tilesets_dir.exists():
        logger.debug('No simple tilesets directory')
    else:
        logger.debug('Create thumbnails for simple tilesets')
    for source_texture in simple_tilesets_dir.iterdir():
        if not source_texture.suffix in ASSET_TEXTURE_FILETYPE_SUFFIXES:
            continue
        in_pack_path = f'res://packs/{pack_id}/textures/tilesets/simple/{source_texture.stem}.png'
        target_filename = thumbs_dir / f'{md5(in_pack_path.encode("utf8")).hexdigest()}.png'
        if target_filename.exists() and not no_delete:
            continue
        create_thumbnail(width, source_texture, target_filename)

    # Do smart tilesets
    if not smart_tilesets_dir.exists():
        logger.debug('No smart tileset directory.')
    else:
        logger.debug('Create thumbnails for smart tilesets')
    for source_texture in smart_tilesets_dir.iterdir():
        if source_texture.suffix not in ASSET_TEXTURE_FILETYPE_SUFFIXES:
            continue
        in_pack_path = f'res://packs/{pack_id}/textures/tilesets/smart/{source_texture.stem}.png'
        target_filename = thumbs_dir / f'{md5(in_pack_path.encode("utf8")).hexdigest()}.png'
        if target_filename.exists() and not no_delete:
            continue
        create_thumbnail(width, source_texture, target_filename)

    # Do double smart tilesets
    if not smartdouble_tilesets_dir.exists():
        logger.debug('No smart-double tilesets directory.')
    else:
        logger.debug('Create thumbnails for smart-double tilesets')
    for source_texture in smartdouble_tilesets_dir.iterdir():
        if not source_texture.suffix in ASSET_TEXTURE_FILETYPE_SUFFIXES:
            continue
        in_pack_path = f'res://packs/{pack_id}/textures/tilesets/smart_double/{source_texture.stem}.png'
        target_filename = thumbs_dir / f'{md5(in_pack_path.encode("utf8")).hexdigest()}.png'
        if target_filename.exists() and not no_delete:
            continue
        create_thumbnail(width, source_texture, target_filename)

    # Do materials
    if not materials_dir.exists():
        logger.debug('No materials assets directory.')
    else:
        logger.debug('Create thumbnails for material assets.')
    for source_texture in materials_dir.iterdir():
        if not source_texture.stem.endswith('_tile') or \
                not source_texture.suffix in ASSET_TEXTURE_FILETYPE_SUFFIXES:
            continue
        in_pack_path = f'res://packs/{pack_id}/textures/materials/{source_texture.stem}.png'
        target_filename = thumbs_dir / f'{md5(in_pack_path.encode("utf8")).hexdigest()}.png'
        if target_filename.exists() and not no_delete:
            continue
        create_thumbnail(width, source_texture, target_filename)

def create_thumbnail(width: int, source_texture: pathlib.Path, target_filename: pathlib.Path):
    logging.debug(f'Mapping {source_texture.name} to {target_filename}')
    with Image.open(source_texture) as img:
        crop_size = min(img.width, img.height, 500)
        box = (0, 0, crop_size, crop_size)
        cropped = img.crop(box)
        cropped.thumbnail((width, width))
        cropped.save(target_filename, 'PNG')


def create_set(set_name: str):
    logger.debug(f'Creating set {set_name}')
    try:
        data = _get_tag_json()
    except FileNotFoundError:
        data = _create_default_tag_dict()
    except json.JSONDecodeError as e:
        logger.error(e)
        raise InvalidTagStructure
    if set_name not in data['sets']:
        data['sets'][set_name] = []
    _put_tag_json(data)

def delete_set(set_name:str):
    logger.debug(f'Deleting set {set_name}')
    try:
        data = _get_tag_json()
    except FileNotFoundError:
        data = _create_default_tag_dict()
    except json.JSONDecodeError as e:
        logger.error(e)
        raise InvalidTagStructure
    popped = data['sets'].pop(set_name, None)
    if not popped:
        logger.warning(f'{set_name} not found in sets.')
    else:
        _put_tag_json(data)

def remove_tag_from_set(tag_name, set_name):
    logger.debug(f'Removing {tag_name} from set {set_name}')
    try:
        data = _get_tag_json()
    except FileNotFoundError:
        data = _create_default_tag_dict()
    except json.JSONDecodeError as e:
        logger.error(e)
        raise InvalidTagStructure
    try:
        new_tag_list = [tag for tag in data['sets'][set_name] if tag != tag_name]
        data['sets'][set_name] = new_tag_list
    except KeyError as e:
        logger.warning(e)
    else:
        _put_tag_json(data)

def create_tag(tag_name: str, set_name=None):
    logger.debug(f'Creating tag {tag_name}')
    try:
        data = _get_tag_json()
    except FileNotFoundError:
        data = _create_default_tag_dict()
    except json.JSONDecodeError as e:
        logger.error(e)
        raise InvalidTagStructure
    if tag_name not in data['tags']:
        data['tags'][tag_name] = []
    if set_name is not None:
        if set_name not in data['sets']:
            logger.debug(f'Creating set {set_name} and '
                         f'adding {tag_name} to it.')
            data['sets'][set_name] = [tag_name]
        else:
            if tag_name not in data['sets'][set_name]:
                logger.debug(f'Adding {tag_name} to {set_name}')
                data['sets'][set_name].append(tag_name)
    _put_tag_json(data)


def delete_tag(tag_name: str):
    logger.debug(f'Deleting tag {tag_name}')
    try:
        data = _get_tag_json()
    except FileNotFoundError as e:
        logger.error(e)
        data = _create_default_tag_dict()
    except json.JSONDecodeError as e:
        logger.error(e)
        raise InvalidTagStructure
    popped = data['tags'].pop(tag_name, None)
    if not popped:
        logger.warning('Tag was not found.')
    popped = data['sets'].pop(tag_name, None)
    if popped:
        _put_tag_json(data)

def add_tag_to_set(tag_name: str, set_name: str):
    create_tag(tag_name, set_name)

def tag_objects(tag_name, object_paths: list[pathlib.Path], colorable=False):
    data = _get_tag_json()
    if tag_name not in data['tags']:
        data['tags'][tag_name] = []
    for object_path in object_paths:
        if object_path not in data['tags'][tag_name]:
            data['tags'][tag_name].append(object_path)
        if colorable and object_path not in data['tags']['Colorable']:
            data['tags']['Colorable'].append(object_path)
    _put_tag_json(data)


def untag_objects(tag_name, object_paths: list[pathlib.Path]):
    data = _get_tag_json()
    if tag_name not in data['tags']:
        logger.warning('Nothing to do.')
        return
    new_object_list = [op for op in data['tags'][tag_name] if op not in object_paths]
    data['tags'][tag_name] = new_object_list
    _put_tag_json(data)


def get_tag_json() -> dict:
    return _get_tag_json()

def _get_tag_json() -> dict:
    project_root = utils.get_project_root(CWD)
    tags_filename = project_root / 'unpacked-asset-tree' / 'data' / 'default.dungeondraft_tags'
    try:
        with open(tags_filename, 'r') as fh:
            data = json.load(fh)
    except FileNotFoundError:
        data = _create_default_tag_dict()
        _put_tag_json(data)
    except json.JSONDecodeError as e:
        logger.error(e)
        raise InvalidTagStructure
    return data


def _put_tag_json(data: dict):
    project_root = utils.get_project_root(CWD)
    tags_filename = project_root / 'unpacked-asset-tree' / 'data' / 'default.dungeondraft_tags'
    with open(tags_filename, 'w') as fh:
        json.dump(data, fh, indent=4)


def get_object_assets():
    objects = {}
    project_root = utils.get_project_root(CWD)
    objects_dir = project_root / 'unpacked-asset-tree' / 'textures' / 'objects'
    for file_path in objects_dir.iterdir():
        if not file_path.suffix in ASSET_TEXTURE_FILETYPE_SUFFIXES:
            continue
        pack_relative_pathstr = os.path.join('textures', 'objects', file_path.name)
        objects[file_path.stem] = pack_relative_pathstr
    return objects


def _create_default_tag_dict():
    return {
        'tags': {
            'Colorable': []
        },
        'sets': {

        }
    }
