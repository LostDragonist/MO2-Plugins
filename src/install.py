'''
Copies the files to an MO2 install
'''
from release import files_to_pack
import shutil
import os

install_directory = os.path.join("C:/", "git", "modorganizer-umbrella", "install", "bin")

for file_, path in files_to_pack:
    shutil.copy2(
        file_,
        os.path.join(install_directory, path)
        )