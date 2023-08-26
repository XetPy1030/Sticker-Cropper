import os
import tkinter as tk

import customtkinter

from utils import collect_files


class ImageActionFrame:
    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent

        self.folder_stickers = 'stickers'
        self.folder_cropped_stickers = 'cropped_stickers'
        self.folder_dones_stickers = 'dones_stickers'

        self.create_widgets()

    def init_image(self):
        self.images_list = collect_files(self.folder_stickers, ['png', 'jpg', 'jpeg'])
        self.images_list.sort()

        self.set_page_max(len(self.images_list))

        self.set_page(1)

    def create_widgets(self):
        self.imageFrame = customtkinter.CTkFrame(self.controller)
        self.imageFrame.grid(row=2)

        self.prevButton = customtkinter.CTkButton(self.imageFrame, text='Prev',
                                                  command=self.prev_image)
        self.nextButton = customtkinter.CTkButton(self.imageFrame, text='Next',
                                                  command=self.next_image)
        self.doneButton = customtkinter.CTkButton(self.imageFrame, text='Done',
                                                  command=self.done_image)
        self.controller.bind('<Left>', lambda event: self.prev_image())
        self.controller.bind('<Right>', lambda event: self.next_image())
        self.controller.bind('<Return>', lambda event: self.done_image())
        self.pageLabel = customtkinter.CTkLabel(self.imageFrame, text='Page')
        self.pageEntry = customtkinter.CTkEntry(self.imageFrame, width=5)
        self.maxPageLabel = customtkinter.CTkLabel(self.imageFrame, text='of 0')

        self.pageEntry.insert(0, '1')
        self.pageEntry.bind('<Return>', self.page_entry_callback)

        self.prevButton.grid(row=0, column=0)
        self.nextButton.grid(row=0, column=1)
        self.doneButton.grid(row=0, column=2)
        self.pageLabel.grid(row=0, column=3)
        self.pageEntry.grid(row=0, column=4)
        self.maxPageLabel.grid(row=0, column=5)

    def prev_image(self):
        if self.get_page() > 1:
            self.set_page(self.get_page() - 1)

    def next_image(self):
        if self.get_page() < len(self.images_list):
            self.set_page(self.get_page() + 1)

    def done_image(self, *args, **kwargs):
        self.controller.start_cropping()

        folder, filename = os.path.split(self.controller.filename)
        new_folder = self.folder_dones_stickers
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        new_filename = os.path.join(new_folder, filename)
        os.rename(self.controller.filename, new_filename)

        self.init_image()


    def page_entry_callback(self, event):
        ...

    def set_page(self, page):
        self.pageEntry.delete(0, tk.END)
        self.pageEntry.insert(0, str(page))

        self.controller.filename = self.images_list[page - 1]
        self.controller.loadimage()

    def get_page(self):
        return int(self.pageEntry.get())

    def set_page_max(self, page_max):
        self.maxPageLabel.configure(text='of ' + str(page_max))

    def set_button_state(self):
        if self.controller.n > 0:
            self.prevButton['state'] = tk.NORMAL
        else:
            self.prevButton['state'] = tk.DISABLED
        if self.controller.n < len(self.controller.crop_rects):
            self.nextButton['state'] = tk.NORMAL
        else:
            self.nextButton['state'] = tk.DISABLED
        if self.controller.n > 0 and self.controller.n == len(self.controller.crop_rects):
            self.doneButton['state'] = tk.NORMAL
        else:
            self.doneButton['state'] = tk.DISABLED



