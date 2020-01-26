'''
Packs all the plugins up into a zip file to upload elsewhere.
Zip file is packed such that it can be extracted to the MO2 directory to install everything.
'''

from zipfile import ZipFile, ZIP_LZMA

files_to_pack = (
    # File to pack                          Path to extract to
    ("FixGameRegKey/FixGameRegKey.py",      "plugins/FixGameRegKey.py"),
    ("GameRedirector/GameRedirector.py",    "plugins/GameRedirector.py"),
)

with ZipFile('../LostDragonist-MO2-Plugins.zip', 'w', ZIP_LZMA) as zip:
    for file_, path in files_to_pack:
        zip.write(file_, path)