# AlbumReorganizer: A Python tool for organizing digital photo collections efficiently.
# Copyright (C) 2023 Aaron Hadley, aaronjhadley@gmail.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import time
from folder_processing import processFolder, temporalGrouping
from PIL.ExifTags import TAGS
from gui import ChooseBest

localPath = os.path.normpath('E:/OldPictures')
destinationPath = 'E:/NewPictures'
undoPath = 'E:/NewPictures/2009'


# _TAGS_r = dict(((v, k) for k, v in TAGS.items()))
# totalFiles = 0
# processedPhotos = 0
# notPhotos = 0
def main(step, threshold):
    totalFiles = 0
    processedPhotos = 0
    notPhotos = 0
    if step == 'prepare':
        tic = time.perf_counter()
        totalFiles, processedPhotos, notPhotos = processFolder(localPath, destinationPath, True, totalFiles,
                                                               processedPhotos, notPhotos)
        print("There are total %d files" % totalFiles)
        totalFiles, processedPhotos, notPhotos = processFolder(localPath, destinationPath, False, totalFiles, processedPhotos, notPhotos)
        print("\nThere are %d photos processed, %d not processed" % (processedPhotos, notPhotos))
        toc = time.perf_counter()
        print(f"Time used: {toc - tic:0.4f} seconds")

    if step == 'group':
        tic = time.perf_counter()
        subpath = [p for p in os.listdir(destinationPath)]
        print(subpath)
        for spath in subpath:
            print(spath)
            print(spath[-4:-2])
            if (spath[-4:-2] == '19' or spath[-4:-2] == '20'):
                print('run')
                temporalGrouping(os.path.join(destinationPath, spath), threshold)
        toc = time.perf_counter()
        print(f"Time used: {toc - tic:0.4f} seconds")

    if step == 'review':
        tic = time.perf_counter()
        subpath = [p for p in os.listdir(destinationPath)]
        endprocess = False
        for spath in subpath:
            print(spath)
            subpathx = os.path.join(destinationPath, spath)
            grouping = [p for p in os.listdir(subpathx)
                        if os.path.isdir(os.path.join(subpathx, p))]
            if endprocess:
                break
            for group in grouping:
                if group[0:5] == 'group':
                    # 0,0 will be top left, negative goes up and lef, positive goes down and right
                    x = 0
                    y = 0
                    endprocess = ChooseBest(os.path.join(destinationPath, spath, group), x, y)
                    if endprocess:
                        break

        toc = time.perf_counter()
        print(f"Time used: {toc - tic:0.4f} seconds")

    if step == 'undogrouping':
        import shutil

        # Function to check if a file is a picture
        def is_picture(file_name):
            picture_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
            return any(file_name.lower().endswith(ext) for ext in picture_extensions)

        # Iterate over the items in the main folder
        for item in os.listdir(undoPath):
            item_path = os.path.join(undoPath, item)

            # Check if the item is a directory and starts with 'group'
            if os.path.isdir(item_path) and item.startswith('group'):
                for file in os.listdir(item_path):
                    file_path = os.path.join(item_path, file)

                    # Check if the item is a picture
                    if os.path.isfile(file_path) and is_picture(file):
                        # Move the picture to the main folder
                        shutil.move(file_path, undoPath)

        print("Pictures have been moved.")


if __name__ == "__main__":
    step='prepare'
    step='group'
    step='review'
    # step='undogrouping'
    # step = ('Warning: This program will rename all your files and move them around without saving the original state.'
    #         'Do not run it unless you know what you are doing. If possible, make a copy first.'
    #         'When ready, uncomment and run for each step incrementally, checking your progress as you go')
    threshold = 5
    main(step=step, threshold=threshold)
