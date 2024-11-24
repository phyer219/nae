import mutagen
import os

bas_dir = './test_media'
files = os.listdir(bas_dir)

for f in files:
    mfile = mutagen.File(os.path.join(bas_dir, f))
    mfile.info.pprint()
    for k, v in mfile.tags.items():
        print(k, v)
