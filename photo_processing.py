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
from PIL import Image
from datetime import datetime
import shutil
from PIL.ExifTags import TAGS



def processPhoto(photoPath, destinationPath , processedPhotos, notPhotos):
    _TAGS_r = dict(((v, k) for k, v in TAGS.items()))
    try:
        processme=False
        with Image.open(photoPath) as im:
            exif_data_PIL = im._getexif()
            # print(_TAGS_r["DateTimeOriginal"])
            if exif_data_PIL is not None:
                if exif_data_PIL[_TAGS_r["DateTimeOriginal"]] is not None:
                    fileDate = exif_data_PIL[_TAGS_r["DateTimeOriginal"]]
                    if fileDate != '' and len(fileDate) > 10:
                        fileDate = fileDate.replace(":", "")
                        # my destination folders are named as YYYY
                        # destinationFolder = fileDate[:6] ### Edit here if you want Year/Month
                        destinationFolder = fileDate[:4]  ### Year only in file name
                        # if destination folder does not exist, create one
                        if not os.path.isdir(os.path.abspath(os.path.join(destinationPath, destinationFolder))):
                            os.mkdir(os.path.abspath(os.path.join(destinationPath, destinationFolder)))
                        # new name of the photo
                        newPhotoName = os.path.abspath(os.path.join(destinationPath, destinationFolder, fileDate + '.' + im.format))
                        if im.format =='MPO':
                            trueextension=os.path.splitext(photoPath)[-1]
                            newPhotoName = os.path.abspath(
                                os.path.join(destinationPath, destinationFolder, fileDate + trueextension))

                        newPhotoName=newPhotoName.replace('/','\\')
                        processme=True

                        processedPhotos += 1
                        # print("\r%d photos processed, %d not processed A" % (processedPhotos, notPhotos))
            else:
                notPhotos += 1
                if photoPath[-3:]=='jpg' or photoPath[-3:]=='JPG' or photoPath[-3:]=='bmp' or photoPath[-3:]=='BMP' \
                        or photoPath[-3:]=='png' or photoPath[-3:]=='PNG' or photoPath[-4:]=='jpeg' or photoPath[-4:]=='JPEG':
                    processedPhotos, notPhotos = getModifiedtime(photoPath, destinationPath,im, processedPhotos, notPhotos)
                    notPhotos -= 1
                    processedPhotos += 1

                    # print("\r%d photos processed, %d not processed A" %
                #
                    print("\r%d photos processed, %d not processed" % (processedPhotos, notPhotos))
                # im.close()
        if processme:
            shutil.move(photoPath, newPhotoName)
        print("\r%d photos processed, %d not processed" % (processedPhotos, notPhotos))

    except IOError as err:
        notPhotos += 1
        getVideos(photoPath,destinationPath, processedPhotos, notPhotos)
        getBMPS(photoPath,destinationPath, processedPhotos, notPhotos)
        print("\r%d photos processed, %d not processed" % (processedPhotos, notPhotos))
        pass
    except KeyError:
        print("key error")
        processedPhotos, notPhotos = getModifiedtime(photoPath,destinationPath,im, processedPhotos, notPhotos)
        notPhotos += 1
        pass
    except AttributeError:
        print("attribute error")
        processedPhotos, notPhotos = getModifiedtime(photoPath, destinationPath,im, processedPhotos, notPhotos)
        notPhotos += 1
        pass
    return processedPhotos, notPhotos

def getModifiedtime(photoPath,destinationPath,im, processedPhotos, notPhotos):
    try:
        timestamp=os.path.getmtime(photoPath)
        fileDate = datetime.fromtimestamp(timestamp).strftime('%Y%m%d %H%M%S')
        destinationFolder = fileDate[:4]
        # if destination folder does not exist, create one
        if not os.path.isdir(os.path.abspath(os.path.join(destinationPath, destinationFolder))):
            os.mkdir(os.path.abspath(os.path.join(destinationPath, destinationFolder)))
        # new name of the photo
        newPhotoName = os.path.abspath(os.path.join(destinationPath, destinationFolder, fileDate + '.' + im.format))
        if im.format == 'MPO':
            trueextension = os.path.splitext(photoPath)[-1]
            newPhotoName = os.path.abspath(
                os.path.join(destinationPath, destinationFolder, fileDate + trueextension))

        newPhotoName = newPhotoName.replace('/', '\\')
        # processme = True
        im.close()
        shutil.move(photoPath, newPhotoName)

        processedPhotos += 1
        print("\r%d photos processed, %d not processed" % (processedPhotos, notPhotos))
    except: print('error again')
    return processedPhotos, notPhotos

def getVideos(photoPath, destinationPath, processedPhotos, notPhotos,):
    try:
        timestamp=os.path.getmtime(photoPath)
        fileDate = datetime.fromtimestamp(timestamp).strftime('%Y%m%d %H%M%S')
        # destinationFolder = fileDate[:6] ### Year/Month
        destinationFolder = fileDate[:4] ### Year
        vidfolder='Videos'
        # if destination folder does not exist, create one
        if not os.path.isdir(os.path.abspath(os.path.join(destinationPath, destinationFolder,vidfolder))):
            os.mkdir(os.path.abspath(os.path.join(destinationPath, destinationFolder,vidfolder)))
        # new name of the photo
        trueextension = os.path.splitext(photoPath)[-1]
        newPhotoName = os.path.abspath(os.path.join(destinationPath, destinationFolder,vidfolder, fileDate + trueextension))
        processme = True

        shutil.move(photoPath, newPhotoName)
        # im.close()
        processedPhotos += 1
        print("\r%d photos processed, %d not processed A" % (processedPhotos, notPhotos))
    except: print('error again')
    return processedPhotos, notPhotos

def getBMPS(photoPath, destinationPath, processedPhotos, notPhotos):
    try:
        timestamp=os.path.getmtime(photoPath)
        fileDate = datetime.fromtimestamp(timestamp).strftime('%Y%m%d %H%M%S')
        # destinationFolder = fileDate[:6] ### Year/Month
        destinationFolder = fileDate[:4]  ### Year
        vidfolder='BMPS'
        # if destination folder does not exist, create one
        if not os.path.isdir(os.path.abspath(os.path.join(destinationPath, destinationFolder,vidfolder))):
            os.mkdir(os.path.abspath(os.path.join(destinationPath, destinationFolder,vidfolder)))
        # new name of the photo
        trueextension = os.path.splitext(photoPath)[-1]
        newPhotoName = os.path.abspath(os.path.join(destinationPath, destinationFolder,vidfolder, fileDate + trueextension))
        processme = True

        shutil.move(photoPath, newPhotoName)
        # im.close()
        processedPhotos += 1
        print("\r%d photos processed, %d not processed A" % (processedPhotos, notPhotos))
    except: print('bmp error again')
    return processedPhotos, notPhotos

