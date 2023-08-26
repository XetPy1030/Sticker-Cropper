import os

from PIL import ImageFilter, ImageTk, Image

from components.rect import Rect
from config import thumboffset, thumbsize
import tkinter as tk


class ImageCore:
    filename: str

    def displayimage(self):
        rr = (
            self.region_rect.left, self.region_rect.top,
            self.region_rect.right,
            self.region_rect.bottom)
        self.image_thumb = self.image.crop(rr)
        self.image_thumb.thumbnail(thumbsize, Image.LANCZOS)
        if self.countour:
            self.image_thumb = self.image_thumb.filter(ImageFilter.CONTOUR)

        self.image_thumb_rect = Rect(self.image_thumb.size)

        self.photoimage = ImageTk.PhotoImage(self.image_thumb)
        w, h = self.image_thumb.size
        self.canvas.configure(
            width=(w + 2 * thumboffset),
            height=(h + 2 * thumboffset))

        self.canvas.create_image(
            thumboffset,
            thumboffset,
            anchor=tk.NW,
            image=self.photoimage)

        x_scale = float(self.region_rect.w) / self.image_thumb_rect.w
        y_scale = float(self.region_rect.h) / self.image_thumb_rect.h
        self.scale = (x_scale, y_scale)
        self.redraw_rect()
        self.set_button_state()

    def loadimage(self):
        self.image = Image.open(self.filename)
        self.image_rect = Rect(self.image.size)
        self.w = self.image_rect.w
        self.h = self.image_rect.h
        self.region_rect = Rect((0, 0), (self.w, self.h))

        self.displayimage()

    def newfilename(self, filenum):
        folder, filename = os.path.split(self.filename)
        name, ext = os.path.splitext(filename)
        return os.path.join(self.folder_cropped_stickers, name + '_' + str(filenum) + ext)

    def start_cropping(self):
        cropcount = 0
        for croparea in self.crop_rects:
            cropcount += 1
            f = self.newfilename(cropcount)
            print(f, croparea)
            self.crop(croparea, f)

        self.crop_rects = []
        self.redraw()

    def crop(self, croparea, filename):
        ca = (croparea.left, croparea.top, croparea.right, croparea.bottom)
        newimg = self.image.crop(ca)
        newimg.save(filename)
