# AlbumReorganizer: A Python tool for organizing digital photo collections efficiently.
# Copyright (C) 2023 Aaron Hadley

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
from photo_processing import processPhoto
from datetime import datetime

def processFolder(folderPath, destinationPath, countOnly, totalFiles, processedPhotos, notPhotos):
    for file in os.listdir(folderPath):
        print(file)
        # read all files and folder
        fileNameIn = os.path.normpath(os.path.join(folderPath, file))
        # print(fileNameIn)
        # if this is a folder, read all files inside
        if os.path.isdir(fileNameIn):
            totalFiles, processedPhotos, notPhotos =processFolder(fileNameIn, destinationPath, countOnly, totalFiles, processedPhotos, notPhotos)
        # if it's file, process it as a photo
        else:
            if countOnly:
                totalFiles +=1
            else:
                processedPhotos, notPhotos = processPhoto(fileNameIn, destinationPath, processedPhotos, notPhotos)
    return totalFiles, processedPhotos, notPhotos

def temporalGrouping(path, threshold = 5):
      # Set the threshold for the time between photos in seconds
    # threshold = 4

    # Create a dictionary to store the photos
    photos = {}

    # Loop through all the files in the folder
    for file in os.listdir(path):
        # Check if the file is a JPEG image
        if file.endswith(".JPG") or file.endswith(".JPEG") or file.endswith(".PNG"):
            # Get the time from the filename
            time_str = os.path.splitext(file)[0]
            time = datetime.strptime(time_str, "%Y%m%d %H%M%S")
            # Add the file to the dictionary with the time as the key
            photos[time] = file

    # Sort the dictionary by the creation time
    sorted_photos = sorted(photos.items())

    # Loop through the sorted photos and find groups of photos taken within the threshold
    groups = []
    group = []
    previous_time = None
    for time, file in sorted_photos:
        if previous_time is not None and (time - previous_time).total_seconds() < threshold:
            group.append((time, file))
        else:
            if group:
                groups.append(group)
            group = [(time, file)]
        previous_time = time

    # Move all the photos within each group to a new folder
    for group in groups:
        if len(group)>1:
            # Create a new folder for the group
            group_folder = os.path.join(path, "group-" + group[0][0].strftime("%Y%m%d-%H%M%S"))
            os.mkdir(group_folder)
            # Move all the photos to the group folder
            for time, file in group:
              os.rename(os.path.join(path, file), os.path.join(group_folder, file))

