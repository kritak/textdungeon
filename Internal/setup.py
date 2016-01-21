#same folder as the main folder!

from distutils.core import setup
import py2exe

setup(console=['dungeon2d.py'])


DATA=[('dungeons',['C:\\Users/Andreas/Desktop/textdungeon-master/dungeons/zoo.csv',
    'C:\\Users/Andreas/Desktop/textdungeon-master/dungeons/items.csv',
    'C:\\Users/Andreas/Desktop/textdungeon-master/dungeons/meleeweapon.csv',
    'C:\\Users/Andreas/Desktop/textdungeon-master/dungeons/wearables.csv',
    'C:\\Users/Andreas/Desktop/textdungeon-master/dungeons/legend.txt',
    'C:\\Users/Andreas/Desktop/textdungeon-master/dungeons/commands.txt',
    'C:\\Users/Andreas/Desktop/textdungeon-master/dungeons/dungeon001.txt',
    'C:\\Users/Andreas/Desktop/textdungeon-master/dungeons/dungeon002.txt',
    'C:\\Users/Andreas/Desktop/textdungeon-master/dungeons/dungeon003.txt',
    'C:\\Users/Andreas/Desktop/textdungeon-master/dungeons/dungeon004.txt',
    'C:\\Users/Andreas/Desktop/textdungeon-master/dungeons/dungeon005.txt'
    ])]

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    zipfile = None,
    data_files = DATA,
)
