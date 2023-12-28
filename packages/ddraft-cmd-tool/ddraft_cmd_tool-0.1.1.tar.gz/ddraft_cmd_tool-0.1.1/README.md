
# Development Guidelines
- [Semantic Versioning](https://semver.org/#semantic-versioning-200)
- [Changelog](https://keepachangelog.com/en/1.0.0/)
- [Python Style Guide](https://peps.python.org/pep-0008/)

# Creating a Project
Installing this package adds a command-line tool that can be called from the terminal,
called `draft`. You should be able to use `draft --help` to get a list of commands 
available. The general workflow is as follows:

Create a new project directory and navigate to that directory in your terminal.
Use the `draft init` command to initialize a new DungeonDraft project. 
If you follow all the default options, like so:

```
$ draft init
Please enter information for your config file. These can be changed later.
Author: Jacob Lee
Pack Name: Example-DungeonDraft-Pack
Do you want to generate a new pack id now? Y/n: y
Your pack id is: YqtFEhSN
Where do you want to put packed assets? Leave empty to use the default: /home/jacoblee/Projects/Dungeondraft-Asset-Packs/resources/asset-tool/test/example-project/packed-assets
Would you like to create a workspace in /home/jacoblee/Projects/Dungeondraft-Asset-Packs/resources/asset-tool/test/example-project/workspace for asset development? This is optional, but may be useful. Y/n: y
New project initialized

```

it will create a folder structure like the following:

```
.
├── .draft
│   └── config.ini
├── packed-assets
├── unpacked-asset-tree
│   ├── data
│   │   ├── tilesets
│   │   └── walls
│   └── textures
│       ├── caves
│       ├── lights
│       ├── materials
│       ├── objects
│       ├── paths
│       ├── roofs
│       ├── terrain
│       ├── tilesets
│       │   ├── simple
│       │   ├── smart
│       │   └── smart_double
│       └── walls
└── workspace
    ├── drafts
    │   ├── caves
    │   ├── lights
    │   ├── materials
    │   ├── objects
    │   ├── paths
    │   ├── portals
    │   ├── roofs
    │   ├── terrains
    │   ├── tilesets
    │   │   ├── simple
    │   │   ├── smart
    │   │   └── smart_double
    │   └── walls
    ├── notes
    └── resources

```

So what are these?

## .draft directory
This is the directory where configuration and logs are written. The init command created a 
file called `config.ini`. In this example, that file would look like:

```
[PROJECT]
name = Example-DungeonDraft-Pack
id = YqtFEhSN
author = Jacob Lee
workspace = /home/jacoblee/Projects/Dungeondraft-Asset-Packs/resources/asset-tool/test/example-project/workspace
packed_assets_dir = /home/jacoblee/Projects/Dungeondraft-Asset-Packs/resources/asset-tool/test/example-project/packed-assets
```

which includes the name of your asset project, the asset pack ID, and 
author information. It also gives the full paths to two special directories, which we'll discuss next.
Although the file can be manually edited, it is intended that the tool be used to manage this and other files.

## Packed Assets Directory
This is the directory where .dungeondraft_pack files are written when you use the `draft pack` command.
I don't recommend you change this (and I haven't tested it anywhere else). Copy files from here to 
anywhere you need them, or point DungeonDraft's asset directory here.

## Unpacked Asset Tree Directory
This directory is where the unpacked asset goes. While you can edit, add, and remove these files
directly, this tool is intended to make the management of an asset easier. There is no guarantee
that things will work correctly if ad-hoc custom changes are made outside of use of the tool.

## Workspace Directory
This directory is intended as the place for you to do all the messy creative stuff you do, keeping the 
unpacked asset tree clean. You don't have to use it, but it is intended to be a reasonable, if 
opinionated, way of organizing your workspace. The tool *does not* assume that this directory exists.

# Managing a Project

## Adding an asset
To add an asset to the project, you use the `draft add` command. It requires three arguments, the asset type,
the asset-key-name you'd like to use, and the path to the asset. e.g.

```
draft add wall dank-stone workspace/drafts/walls/dank-stone-wall-version-3.0.1.png
```

Assuming (of course), that there is a matching `dank-stone-wall-version-3.0.1_end.png`
file, this will add the following to the `unpacked-asset-tree/textures/walls` directory:

```
dank-stone.png
dank-stone_end.png
```

and create an appropriate corresponding 
data file `unpacked_asset-tree/data/walls/dank-stone.dungeondraft_wall`.

## Removing an asset
To remove an asset, call `draft remove` command. This takes two arguments. The `asset-type`
and the `asset-key-name`. To remove the dank-stone-wall asset, you'd use the command:

```
draft remove wall dank-stone
```

## Listing your assets
Use the `draft list` command to see what assets are in the unpacked asset tree.

## Creating thumbnails
When you are ready to pack, if you want to, you can use this tool to create thumbnails,
currently implemented only for terrain and for tilesets. This will create larger, close-up, 
thumbnails that can be embedded in the packed asset. Note: the thumbnail filenames
use the pack id. If you change the pack id, you will need to regenerate the thumbnails (because the
filenames will change).

To create thumbnails, use the command:

```
draft thumbify
```

This will create a directory in the unpacked asset tree called `thumbnails`

## Packing your asset
Packing your assets is easy. Simply use the command:

```
draft pack [version]
```

The rest of the information (name, author, etc.) are in the draft tool's config file.

e.g.

```
draft pack 1.0.1
```

will create a new pack file in the `packed-assets` directory.
