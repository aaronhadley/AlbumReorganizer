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
from PIL.ExifTags import TAGS
import shutil
import time
from datetime import datetime, timedelta
import tkinter as tk
from PIL import Image, ImageTk


# This is your original photo folder
localPath = os.path.normpath('E:/Old Pictures')
destinationPath = 'E:/New Pictures'
_TAGS_r = dict(((v, k) for k, v in TAGS.items()))
totalFiles = 0
processedPhotos = 0
notPhotos = 0
# path= 'E:\\Test\\202204'
# folder_path='E:\\Test\\202204\\group-20220420-155136'

def processPhoto(photoPath):
    global processedPhotos, notPhotos
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
                        # my destination folders are named as YYYYMM
                        # destinationFolder = fileDate[:6] ### Year/Month
                        destinationFolder = fileDate[:4]  ### Year
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

                        # shutil.copy2(photoPath, newPhotoName)
                        # im.close()
                        processedPhotos += 1
                        # print("\r%d photos processed, %d not processed A" % (processedPhotos, notPhotos))
            else:
                notPhotos += 1
                if photoPath[-3:]=='jpg' or photoPath[-3:]=='JPG' or photoPath[-3:]=='bmp' or photoPath[-3:]=='BMP' \
                        or photoPath[-3:]=='png' or photoPath[-3:]=='PNG' or photoPath[-4:]=='jpeg' or photoPath[-4:]=='JPEG':
                    getModifiedtime(photoPath, im)
                    notPhotos -= 1
                    processedPhotos += 1

                    # print("\r%d photos processed, %d not processed A" %
                #
                    print("\r%d photos processed, %d not processed B" % (processedPhotos, notPhotos))
                # im.close()
        if processme:
            shutil.move(photoPath, newPhotoName)
        print("\r%d photos processed, %d not processed C" % (processedPhotos, notPhotos))

    except IOError as err:
        notPhotos += 1
        getVideos(photoPath)
        getBMPS(photoPath)
        print("\r%d photos processed, %d not processed D" % (processedPhotos, notPhotos))
        pass
    except KeyError:
        print("key error")
        getModifiedtime(photoPath,im)
        notPhotos += 1
        pass
    except AttributeError:
        print("attribute error")
        getModifiedtime(photoPath, im)
        notPhotos += 1
        pass

def getModifiedtime(photoPath,im):
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
        print("\r%d photos processed, %d not processed A" % (processedPhotos, notPhotos))
    except: print('error again')

def getVideos(photoPath):
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

def getBMPS(photoPath):
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

def processFolder(folderPath, countOnly):
    global totalFiles
    for file in os.listdir(folderPath):
        print(file)
        # read all files and folder
        fileNameIn = os.path.normpath(os.path.join(folderPath, file))
        # print(fileNameIn)
        # if this is a folder, read all files inside
        if os.path.isdir(fileNameIn):
            processFolder(fileNameIn, countOnly)
        # if it's file, process it as a photo
        else:
            if countOnly:
                totalFiles +=1
            else:
                processPhoto(fileNameIn)

def temporalGrouping(path):
      # Set the threshold for the time between photos in seconds
    threshold = 4

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

def load_photos(folder_path):
    # Create a list to store the photos
    photos = []
    # root = tk.Tk()
    # Loop through all the files in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file is a JPEG image
        print(file_name)
        if file_name.endswith('.JPG') or file_name.endswith('.JPEG') or file_name.endswith('.PNG'):
            # Load the image
            image = Image.open(os.path.join(folder_path, file_name))
            basewidth=400
            wpercent=(basewidth/float(image.size[0]))
            hsize = int((float(image.size[1])*float(wpercent)))
            # Resize the image to fit in the window
            # image = image.resize((600, 600))
            image = image.resize((basewidth,hsize), Image.Resampling.LANCZOS)
            # Convert the image to a Tkinter-compatible format
            photo = ImageTk.PhotoImage(image)
            # Add the photo to the list
            photos.append({'path': os.path.join(folder_path, file_name), 'photo': photo})
    return photos

def ChooseBest(folder_path):

    global endprocess
    # Create the main window
    window = tk.Tk()

    # Load the photos from the folder
    photos = load_photos(folder_path)

    # Create a list to store the photo labels
    photo_labels = []

    # Define a function to toggle the selection of a photo
    def toggle_selection(index):
        # nonlocal selected_photos
        photo = photos[index]
        if photo in selected_photos:
            selected_photos.remove(photo)
        else:
            selected_photos.append(photo)
        # Update the background color of the photo label
        if photo_labels[index].config('background')[-1] == 'white':
            photo_labels[index].config(background='yellow')
        else:
            photo_labels[index].config(background='white')

    # Define a function to move the selected photos to the main folder
    def move_selected():
        global endprocess
        endprocess=False
        print(selected_photos)
        for photo in selected_photos:
            os.rename(photo['path'], os.path.join(os.path.dirname(folder_path), os.path.basename(photo['path'])))
        # Rename the folder after reviewed only if there are changed
        if len(selected_photos)>0:
            os.rename(folder_path,f'{os.path.dirname(folder_path)}\\x{os.path.basename(folder_path)[5:]}')
        # Close the window
        window.destroy()

    def EndProcess():
        global endprocess
        endprocess=True
        window.destroy()

    def TrashAll():
        global endprocess
        endprocess = False
        # print(selected_photos)
        # for photo in selected_photos:
        #     os.rename(photo['path'], os.path.join(os.path.dirname(folder_path), os.path.basename(photo['path'])))
        # Rename the folder after reviewed only if there are changed
        os.rename(folder_path, f'{os.path.dirname(folder_path)}\\x{os.path.basename(folder_path)[5:]}')
        # Close the window
        window.destroy()

    if len(photos)>=9:
        ncols=4
    else:
        ncols=4

    # Create the photo labels and add them to the list
    for i, photo in enumerate(photos):
        label = tk.Label(image=photo['photo'], background='white')
        label.grid(row=i // ncols, column=i % ncols, padx=5, pady=5)
        label.bind('<Button-1>', lambda event, index=i: toggle_selection(index))
        photo_labels.append(label)

    # Keep nothing button
    trash_button = tk.Button(window, text='Trash all', command = TrashAll)
    trash_button.grid(row=len(photos) // ncols + 1, column=0, pady=10)

    # Create a button to move the selected photos to the main folder
    move_button = tk.Button(window, text='Keep selected', command=move_selected)
    move_button.grid(row=len(photos) // ncols + 1, column=1, pady=10)

    # Exit button
    exit_button = tk.Button(window, text='End', command = EndProcess)
    exit_button.grid(row=len(photos) // ncols + 1, column=2, pady=10)

    # Initialize the selected photos list
    selected_photos = []

    # Make window be in upper window (for my particular setup)
    # w = window.winfo_screenwidth()
    # h = window.winfo_screenheight()
    window.update()
    w = window.winfo_reqwidth()
    h = window.winfo_reqheight()
    x=-50
    y=-1440
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # display_width = window.winfo_screenwidth()
    # display_height = window.winfo_screenheight()
    #
    # # Set the minimum size of the window to display its widgets
    # window.update()
    # window_width = window.winfo_reqwidth()
    # window_height = window.winfo_reqheight()
    #
    # # Set the position of the window to the top left of the second screen
    # window.geometry(f"{window_width}x{window_height}+{display_width - window_width}+0")

    # Start the GUI
    window.mainloop()
    return endprocess

def main(step):

    if step=='prepare':
        tic = time.perf_counter()
        processFolder(localPath, True)
        print("There are total %d files" % totalFiles)
        processFolder(localPath, False)
        print("\nThere are %d photos processed, %d not processed" % (processedPhotos, notPhotos))
        toc = time.perf_counter()
        print(f"Time used: {toc - tic:0.4f} seconds")

    if step=='group':
        tic = time.perf_counter()
        subpath= [p for p in os.listdir(destinationPath)]
        print(subpath)
        for spath in subpath:
            print(spath)
            print(spath[-4:-2])
            if (spath[-4:-2] == '19' or spath[-4:-2] == '20'):
                print('run')
                temporalGrouping(os.path.join(destinationPath,spath))
        toc = time.perf_counter()
        print(f"Time used: {toc - tic:0.4f} seconds")

    if step=='review':
        tic = time.perf_counter()
        subpath = [p for p in os.listdir(destinationPath)]
        endprocess=False
        for spath in subpath:
            print(spath)
            subpathx=os.path.join(destinationPath,spath)
            grouping = [p for p in os.listdir(subpathx)
                        if os.path.isdir(os.path.join(subpathx,p))]
            if endprocess:
                break
            for group in grouping:
                if group[0:5] =='group':
                    endprocess=ChooseBest(os.path.join(destinationPath, spath,group))
                    if endprocess:
                        break

        toc = time.perf_counter()
        print(f"Time used: {toc - tic:0.4f} seconds")

    if step=='undogrouping':
        import shutil

        # Define the path to your main folder
        main_folder_path = 'E:/Organized/2020'

        # Function to check if a file is a picture
        def is_picture(file_name):
            picture_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
            return any(file_name.lower().endswith(ext) for ext in picture_extensions)

        # Iterate over the items in the main folder
        for item in os.listdir(main_folder_path):
            item_path = os.path.join(main_folder_path, item)

            # Check if the item is a directory and starts with 'group'
            if os.path.isdir(item_path) and item.startswith('group'):
                for file in os.listdir(item_path):
                    file_path = os.path.join(item_path, file)

                    # Check if the item is a picture
                    if os.path.isfile(file_path) and is_picture(file):
                        # Move the picture to the main folder
                        shutil.move(file_path, main_folder_path)

        print("Pictures have been moved.")

if __name__ == "__main__":

    step='prepare'
    # step='group'
    # step='review'
    # step='undogrouping'

    main(step=step)