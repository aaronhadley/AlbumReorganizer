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

import tkinter as tk
from PIL import Image, ImageTk
import os


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
            basewidth = 400
            wpercent = (basewidth / float(image.size[0]))
            hsize = int((float(image.size[1]) * float(wpercent)))
            # Resize the image to fit in the window
            # image = image.resize((600, 600))
            image = image.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            # Convert the image to a Tkinter-compatible format
            photo = ImageTk.PhotoImage(image)
            # Add the photo to the list
            photos.append({'path': os.path.join(folder_path, file_name), 'photo': photo})
    return photos


def ChooseBest(folder_path, x, y):
    # Window location: Pixels from top left of main monitor
    # 0,0 will be top left, negative goes up and lef, positive goes down and right
    # x = -50
    # y = -1440
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
        endprocess = False
        print(selected_photos)
        for photo in selected_photos:
            os.rename(photo['path'], os.path.join(os.path.dirname(folder_path), os.path.basename(photo['path'])))
        # Rename the folder after reviewed only if there are changed
        if len(selected_photos) > 0:
            os.rename(folder_path, f'{os.path.dirname(folder_path)}\\x{os.path.basename(folder_path)[5:]}')
        # Close the window
        window.destroy()

    def EndProcess():
        global endprocess
        endprocess = True
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

    if len(photos) >= 9:
        ncols = 4
    else:
        ncols = 4

    # Create the photo labels and add them to the list
    for i, photo in enumerate(photos):
        label = tk.Label(image=photo['photo'], background='white')
        label.grid(row=i // ncols, column=i % ncols, padx=5, pady=5)
        label.bind('<Button-1>', lambda event, index=i: toggle_selection(index))
        photo_labels.append(label)

    # Keep nothing button
    trash_button = tk.Button(window, text='Trash all', command=TrashAll)
    trash_button.grid(row=len(photos) // ncols + 1, column=0, pady=10)

    # Create a button to move the selected photos to the main folder
    move_button = tk.Button(window, text='Keep selected', command=move_selected)
    move_button.grid(row=len(photos) // ncols + 1, column=1, pady=10)

    # Exit button
    exit_button = tk.Button(window, text='End', command=EndProcess)
    exit_button.grid(row=len(photos) // ncols + 1, column=2, pady=10)

    # Initialize the selected photos list
    selected_photos = []

    # Make window be in upper window (for my particular setup)
    # w = window.winfo_screenwidth()
    # h = window.winfo_screenheight()
    window.update()
    w = window.winfo_reqwidth()
    h = window.winfo_reqheight()

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
