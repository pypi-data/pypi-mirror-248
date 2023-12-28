import argparse
import configparser
import json
import logging
import os
import pathlib
import sys

from draft import constants
from draft import drafttool
from draft import utils
from draft import version
from draft.exceptions import NoProjectRootException, AssetNotFoundException, \
    UnknownAssetType, AssetCreationException, InvalidTagStructure


def process():
    invoked_as = os.path.basename(sys.argv[0])
    if invoked_as == 'draft':
        run_draft()


def yesno_query(query):
    yes = {'y', 'ye', 'yes', ''}
    response = input(f'{query} Y/n: ').lower()
    return response in yes


def stdout(x):
    print(x, file=sys.stdout)


def stderr(x):
    print(x, file=sys.stderr)


def create_parser():
    # First define user interface functions to call tool methods

    def _init_pack_project(args):
        if utils.is_asset_project(pathlib.Path(constants.CWD)):
            stderr('This directory is already part of an asset pack project.')
            sys.exit(1)
        else:
            stdout('Please enter information for your config file. '
                   'These can be changed later.')
            author = input('Author: ')
            pack_name = input('Pack Name: ')
            if yesno_query('Do you want to generate a new pack id now?'):
                pack_id = drafttool.gen_pack_id().decode('utf8')
                stdout(f'Your pack id is: {pack_id}')
            else:
                pack_id = ''
                stdout(f'A pack id can be generated any time, or when packing project.')
            packed_assets_dir = input(f'Where do you want to put packed assets? '
                                      f'Leave empty to use the default:')
            if not packed_assets_dir:
                packed_assets_dir = os.path.join(constants.CWD, 'packed-assets')

            create_workspace = yesno_query(f'Would you like to create a workspace in {constants.CWD}/workspace '
                                           f'for asset development? This is optional, but may be useful.')
            drafttool.init(constants.CWD, pack_name, author, pack_id, packed_assets_dir, create_workspace)
            stdout('New project initialized')

    def _thumbify(args):
        if not utils.is_asset_project(pathlib.Path(constants.CWD)):
            stderr('This directory is not part of an asset pack project. '
                   'Use the init command to start one.')
            sys.exit(1)
        project_root = utils.get_project_root(constants.CWD)
        config_file = project_root / '.draft' / 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_file)
        pack_id = config['PROJECT']['id']
        if not pack_id:
            stderr('The pack ID is not set in the config file. Use `genid` \n'
                   'to create a new one, or use the `setconfig` command to set \n'
                   'the pack ID to one of your choice.')
            sys.exit(1)
        drafttool.thumbify(pack_id, args.no_delete, args.width)

    def _gen_packid(args):
        if not utils.is_asset_project(pathlib.Path(constants.CWD)):
            stderr('This directory is not part of an asset '
                   'pack project. Use the init command to start one.')
            sys.exit(1)
        project_root = utils.get_project_root(constants.CWD)
        config_file = project_root / '.draft' / 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_file)
        old_pack_id = config['PROJECT']['id']
        stdout(f'Old pack id = {old_pack_id}')
        new_pack_id = drafttool.gen_pack_id().decode('utf8')
        config['PROJECT']['id'] = new_pack_id
        with open(config_file, 'w') as fh:
            config.write(fh)
        stdout(f'New pack id = {new_pack_id}')

    def _pack(args):
        if not utils.is_asset_project(pathlib.Path(constants.CWD)):
            stderr('This directory is not part of an asset pack project. '
                   'Use the init command to start one.')
            sys.exit(1)
        project_root = utils.get_project_root(constants.CWD)
        config_file = project_root / '.draft' / 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_file)

        try:
            packed_assets_dir = args.packed_assets_dir if args.packed_assets_dir \
                else config['PROJECT']['packed_assets_dir']
            name = args.name if args.name else config['PROJECT']['name']
            pack_id = args.pack_id if args.pack_id else config['PROJECT']['id']
            author = args.author if args.author else config['PROJECT']['author']
            version_str = args.version_str
        except KeyError as e:
            stderr('There seems to be a problem with your config file.')
            stderr(e)
            sys.exit(1)

        if not pack_id:
            pack_id = drafttool.gen_pack_id()
            stdout('No pack ID was specified. New pack ID generated: {pack_id}')
        if not packed_assets_dir or not os.path.exists(packed_assets_dir):
            stderr('`packed_assets_dir` not set in the config file.')
            sys.exit(1)
        if not name:
            stderr('Pack name was not specified in config file or in command arguments.')
            sys.exit(1)
        if not author:
            stderr('Pack author was not specified in config file or in command arguments.')
            sys.exit(1)

        drafttool.call_pack(packed_assets_dir, name, pack_id, author, version_str)

    def _remove_asset(args):
        # Perhaps get confirmation here
        yes = {'y', 'ye', 'yes', ''}
        choice = input(f'Remove asset {args.asset_key_name}? Y/n: ').lower()
        if choice not in yes:
            stderr('Aborting operation.')
            sys.exit(1)
        try:
            drafttool.remove_asset(args.type, args.asset_key_name)
        except NoProjectRootException as e:
            stderr('This directory is not part of an asset pack project. '
                   'Use the init command to start one.')
            sys.exit(1)
        except AssetNotFoundException as e:
            stderr('The asset could not be found. Is the path correct?')
            sys.exit(1)
        except UnknownAssetType as e:
            asset_types = ', '.join(constants.TYPES)
            stderr(f'The asset type you entered was not recognized. '
                   f'Acceptable asset types include: {asset_types}')
            sys.exit(1)
        else:
            stdout('Asset removed.')

    def _add_asset(args):
        try:
            drafttool.add_asset(args.type, args.asset_key_name, args.path_to_asset,
                                color=args.color, custom_color=args.custom_color)
        except NoProjectRootException as e:
            stderr('This directory is not part of an asset pack project. '
                   'Use the init command to start one.')
            sys.exit(1)
        except AssetNotFoundException as e:
            stderr('The asset could not be found. Is the path correct?')
            sys.exit(1)
        except UnknownAssetType as e:
            asset_types = ', '.join(constants.TYPES)
            stderr(f'The asset type you entered was not recognized. '
                   f'Acceptable asset types include: {asset_types}')
            sys.exit(1)
        except AssetCreationException as e:
            stderr('An unexpected error occurred.')
            sys.exit(1)
        else:
            stdout('Asset added.')

    def _replace_asset(args):
        try:
            drafttool.replace_asset(args.type, args.asset_key_name, args.path_to_asset)
        except NoProjectRootException as e:
            stderr('This directory is not part of an asset pack project. '
                   'Use the init command to start one.')
            sys.exit(1)
        except AssetNotFoundException as e:
            stderr('The asset could not be found. Is the path correct?')
            sys.exit(1)
        except UnknownAssetType as e:
            asset_types = ', '.join(constants.TYPES)
            stderr(f'The asset type you entered was not recognized. '
                   f'Acceptable asset types include: {asset_types}')
            sys.exit(1)
        except AssetCreationException as e:
            stderr('An unexpected error occurred.')
            sys.exit(1)
        else:
            stdout('Asset added.')

    def _list_assets(args):
        assets = drafttool.list_assets()
        for asset in assets:
            stdout(f'{asset["asset_type"]}:{asset["asset_name"]}')

    def _tag_object(args):
        objects = drafttool.get_object_assets()
        if not args.object_key_names:
            stderr('Nothing to do.')
            sys.exit(1)
        target = {}
        offtarget = []
        for key_name in args.object_key_names:
            if key_name in objects:
                target[key_name] = objects[key_name]
            else:
                offtarget.append(key_name)
        if offtarget:
            s = '\n'.join(offtarget)
            stderr(f'The following object key names were not found! \n{s}')
            sys.exit(1)
        if not target:
            stderr('None of the provided object keys were found! Aborting.')
            sys.exit(1)
        s = '\n'.join(target.keys())
        if not args.quiet:
            response = yesno_query(f'Tag these objects as "{args.tag_name}"?\n{s}\n')
            if not response:
                stdout('Command aborted.')
                return
        objects_to = [target[k] for k in target]
        drafttool.tag_objects(args.tag_name, objects_to, args.make_colorable)

    def _untag_object(args):
        objects = drafttool.get_object_assets()
        if not args.object_key_names:
            stderr('Nothing to do.')
            sys.exit(1)
        target = {}
        offtarget = []
        for key_name in args.object_key_names:
            if key_name in objects:
                target[key_name] = objects[key_name]
            else:
                offtarget.append(key_name)
        if offtarget:
            s = '\n'.join(offtarget)
            stderr(f'The following object key names were not found! \n{s}')
            sys.exit(1)
        if not target:
            stderr('None of the provided object keys were found! Aborting.')
            sys.exit(1)
        s = '\n'.join(target.keys())
        if not args.quiet:
            response = yesno_query(f'Remove "{args.tag_name} from these objects?\n{s}\n')
            if not response:
                stdout('Command aborted.')
                return
        objects_to = [target[k] for k in target]
        drafttool.untag_objects(args.tag_name, objects_to)

    def _create_tag(args):
        try:
            drafttool.create_tag(args.tag_name, args.add_to_set)
        except InvalidTagStructure:
            stderr('Could not create tag.')
            sys.exit(1)
        else:
            s = f'Creating tag {args.tag_name}'
            t = f' and adding to set {args.add_to_set}.' if args.add_to_set else '.'
            stdout(f'{s}{t}')

    def _delete_tag(args):
        try:
            drafttool.delete_tag(args.tag_name)
        except InvalidTagStructure:
            stderr('Could not delete tag.')
            sys.exit(1)
        else:
            s = f'Deleting tag {args.tag_name} and removing from all sets.'
            stdout(s)

    def _tag_set_add(args):
        try:
            drafttool.add_tag_to_set(args.tag_name, args.set_name)
        except InvalidTagStructure:
            stderr('Could not add tag to set.')
            sys.exit(1)
        else:
            s = f'Added tag {args.tag_name} to set {args.set_name}'
            stdout(s)

    def _tag_set_remove(args):
        try:
            drafttool.remove_tag_from_set(args.tag_name, args.set_name)
        except InvalidTagStructure:
            stderr('Could not delete set.')
            sys.exit(1)
        else:
            s = f'Removed {args.tag_name} from {args.set_name}'
            stdout(s)

    def _tag_set_delete(args):
        try:
            drafttool.delete_set(args.set_name)
        except InvalidTagStructure:
            stderr('Could not delete set.')
            sys.exit(1)
        else:
            s = f'Deleted set {args.set_name}'
            stdout(s)

    def _tag_print(args):
        from pprint import pformat
        data = drafttool.get_tag_json()
        stdout(pformat(data))

    def _inspect(args):
        from pprint import pformat
        s = drafttool.inspect(args.pack_file)
        stdout(pformat(s))

    parser = argparse.ArgumentParser(
        prog='draft',
        description=("A python-based command line tool to create, "
                     "modify and pack DungeonDraft custom assets."),
        epilog="I'd rather have a bottle in front of me, than a frontal lobotomy."
    )
    parser.add_argument('--version', action="version", version=version.version_number)
    action_subparser = parser.add_subparsers(
        help='What action would you like to perform?',
        required=True
    )

    # ACTION: init
    init_action_parser = action_subparser.add_parser(
        'init',
        help="Init project. Creates .draft file in current directory."
    )
    init_action_parser.set_defaults(func=_init_pack_project)

    # ACTION: pack assets
    pack_action_parser = action_subparser.add_parser('pack', help="Pack current DungeonDraft pack.")
    pack_action_parser.add_argument('version_str', help="The asset pack version, e.g. 3, or 1.0.2")
    pack_action_parser.add_argument('--author',
                                    help=("If you want to change the author to something different "
                                          "than what is in your config file."))
    pack_action_parser.add_argument('--name', help="If you want to name the pack something different "
                                                   "than what is named in the config file.")

    pack_action_parser.add_argument('--packed_assets_dir',
                                    help="If you want to save the file somewhere else "
                                         "that the location specified in the config file.")
    pack_action_parser.add_argument('--pack_id',
                                    help="If you want to use a custom pack id different "
                                         "than in config. Not recommended.")
    pack_action_parser.set_defaults(func=_pack)

    # ACTION: remove asset
    remove_action_parser = action_subparser.add_parser('remove', help="Remove an asset.")
    remove_action_parser.add_argument('type', choices=constants.TYPES,
                                      help="The type of asset being removed.")
    remove_action_parser.add_argument('asset_key_name', metavar='asset-key-name',
                                      help="Name of asset to remove.")
    remove_action_parser.set_defaults(func=_remove_asset)

    # ACTION: add asset
    add_action_parser = action_subparser.add_parser('add', help="Add an asset. Will replace or update existing"
                                                                "asset of the same name. If the --color "
                                                                "or --custom-color options were used "
                                                                "before, they must be re-specified here.")
    add_action_parser.add_argument('type', choices=constants.TYPES,
                                   help="The type of asset being added.")
    add_action_parser.add_argument('asset_key_name', metavar='asset-key-name',
                                   help="Identifier for the asset, "
                                        "but not the complete name of the asset.")
    add_action_parser.add_argument('path_to_asset', metavar="path-to-asset",
                                   help="Path to the asset to add.")
    add_action_parser.add_argument('--color', default="ffffff",
                                   help='Specify the hexadecimal formatted '
                                        'color for walls and tilesets. Defaults to'
                                        '"ffffff".')
    add_action_parser.add_argument('--custom-color', action='store_true',
                                   help=('Use this option if you want the meta-file "type" attribute'
                                         'to be set to "custom_color" instead of "normal"'))
    add_action_parser.set_defaults(func=_add_asset)

    # ACTION: rename aseet
    # TODO: implement rename asset functionality

    # ACTION: list assets
    list_action_parser = action_subparser.add_parser('list', help="List all assets")
    list_action_parser.set_defaults(func=_list_assets)

    # ACTION: make thumbnails
    thumbify_action_parser = action_subparser.add_parser(
        'thumbify', help="Generate thumbnails for embedding into pack. "
                         "Only thumbnails for tilesets, terrain "
                         "and materials will be generated. "
                         "Thumbnail file names are a MD5 hash of their file "
                         "path inside the dungeondraft pack; this path includes "
                         "the pack id. If the pack ID changes, then you will "
                         "have to regenerate the thumbnails. By default, we will "
                         "look at the .draft/config file in the project to "
                         "determine the pack id; but if it is not yet "
                         "specified, one will be randomly generated, "
                         "and added to the config file.")
    thumbify_action_parser.add_argument('--no_delete', '-f', action="store_true",
                                        help="Do not overwrite existing thumbnails")
    thumbify_action_parser.add_argument('--width', type=int, default=160,
                                        help="Pixel width of desired output.")
    thumbify_action_parser.set_defaults(func=_thumbify)

    # ACTION: generate new pack id, and write to config file
    packid_action_parser = action_subparser.add_parser(
        'genid', help="Generate a new pack id, and write it to project config. "
                      "Will not change existing pack.json file. That will be "
                      "rewritten when packing."
    )
    packid_action_parser.set_defaults(func=_gen_packid)

    # ACTION: inspect asset pack
    inspect_action_parser = action_subparser.add_parser(
        'inspect', help='Inspect contents of a dungeondraft asset pack.'
    )
    inspect_action_parser.add_argument('pack_file', metavar='pack-file')
    inspect_action_parser.set_defaults(func=_inspect)

    # ACTION: tag
    tag_action_parser = action_subparser.add_parser('tag', help=('Create, delete, and and remove asset tags.'))
    tag_action_subparser = tag_action_parser.add_subparsers(help="What tag action would you like to perform?")

    ## SUB-ACTION: add
    tag_add_parser = tag_action_subparser.add_parser('add', help="Add tag to existing `object` asset.")
    tag_add_parser.add_argument('--make-colorable', action='store_true',
                                help='Tag the object as "Colorable" as well.')
    tag_add_parser.add_argument('--quiet', '-q',
                                action='store_true',
                                help='Do not ask for confirmation before performing action.')
    tag_add_parser.add_argument('tag_name', help="The name of the tag to be applied."
                                                 "Will create the tag if it does not exist.")
    tag_add_parser.add_argument('object_key_names', nargs='+',
                                help='List of key names of objects to tag.')
    tag_add_parser.set_defaults(func=_tag_object)

    ## SUB-ACTION: remove
    tag_remove_parser = tag_action_subparser.add_parser('remove', help="Remove tag from existing`object` asset.")
    tag_remove_parser.add_argument('--remove-colorable', action='store_true',
                                   help='Optionally remove object from the special "Colorable" tag.')
    tag_remove_parser.add_argument('--quiet', '-q',
                                   action='store_true',
                                   help='Do not ask for confirmation before performing action.')
    tag_remove_parser.add_argument('tag_name', help="The name of the tag to be removed. "
                                                    "The tag itself is not deleted.")
    tag_remove_parser.add_argument('object_key_names', nargs='+',
                                   help='List of key names of objects to untag')
    tag_remove_parser.set_defaults(func=_untag_object)

    ## SUB-ACTION: create
    tag_create_parser = tag_action_subparser.add_parser('create', help="Create a new tag.")
    tag_create_parser.add_argument('--add_to_set', default=None,
                                   help="Optionally also add new tag to the named set."
                                        "Will create the set if it does not exist.")
    tag_create_parser.add_argument('tag_name', help="The name of the tag to create")
    tag_create_parser.set_defaults(func=_create_tag)

    ## SUB-ACTION: delete
    tag_delete_parser = tag_action_subparser.add_parser('delete', help="Delete an existing tag.")
    tag_delete_parser.add_argument('tag_name', help="The name of the tag to delete")
    tag_delete_parser.set_defaults(func=_delete_tag)

    ## SUB-ACTION: add-to-set
    tag_set_add_parser = tag_action_subparser.add_parser('add-to-set', help='Add a tag to a set.')
    tag_set_add_parser.add_argument('tag_name', help="The name of the tag to add to a set.")
    tag_set_add_parser.add_argument('set_name', help='The name of the set to add the tag to. '
                                                     'Will create the set if it does not exist.')
    tag_set_add_parser.set_defaults(func=_tag_set_add)

    ## SUB-ACTION: remove-from-set
    tag_set_remove_parser = tag_action_subparser.add_parser('remove-from-set',
                                                            help="Remove tag from set.")
    tag_set_remove_parser.add_argument('tag_name', help='The name of the tag to remove.')
    tag_set_remove_parser.add_argument('set_name', help='The set to remove tag from.')
    tag_set_remove_parser.set_defaults(func=_tag_set_remove)

    ## SUB-ACTION: delete-set
    tag_set_delete_parser = tag_action_subparser.add_parser('delete-set', help='Delete set')
    tag_set_delete_parser.add_argument('set_name', help='Name of set to delete.')
    tag_set_delete_parser.set_defaults(func=_tag_set_delete)

    ## SUB-ACTION: print
    tag_print_parser = tag_action_subparser.add_parser('print', help='Print the tag json file.')
    tag_print_parser.set_defaults(func=_tag_print)

    # TODO: Create a "hexify" command to generate name of thumbnail without actually creating one, in case they want to create customs
    return parser


def run_draft():
    parser = create_parser()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)
    args = parser.parse_args()
    args.func(args)
