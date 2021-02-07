'''
Copies the files to an MO2 install
'''
from release import files_to_pack
import shutil
import os

#install_directory = os.path.join("C:/", "git", "modorganizer-umbrella", "install", "bin")
install_directory = os.path.join("C:/", "Modding", "Tools", "Mod Organizer 2.4.0 RC1")

for key in files_to_pack:
    for file_, path in files_to_pack[key]:
        shutil.copy2(
            file_,
            os.path.join(install_directory, path)
            )