'''
Packs all the plugins up into a zip file to upload elsewhere.
Zip file is packed such that it can be extracted to the MO2 directory to install everything.
'''

from zipfile import ZipFile, ZIP_DEFLATED

files_to_pack = {
    # Archive
    "../LostDragonist-MO2-Plugins.zip" : (
        # File to pack                          Path to extract to
        ("FixGameRegKey/FixGameRegKey.py",      "plugins/FixGameRegKey.py"),
        ("GameRedirector/GameRedirector.py",    "plugins/GameRedirector.py"),
        ("ConflictDeleter/ConflictDeleter.py",  "plugins/ConflictDeleter.py"),
    ),

    # Archive
    "../LootPreventifier.zip" : (
        # File to pack                           Path to extract to
        ("LootPreventifier/LootPreventifier.py", "plugins/LootPreventifier.py"),
    ),
}

for key in files_to_pack:
    with ZipFile(key, 'w', ZIP_DEFLATED) as zip:
        for file_, path in files_to_pack[key]:
            zip.write(file_, path)