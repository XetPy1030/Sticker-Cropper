import customtkinter
import tkinter as tk

from components.rect import Rect


class WorkActionFrame:
    def __init__(self, parent, controller):
        self.controller = controller

        self.workFrame = customtkinter.CTkFrame(parent)

        self.zoomFrame = customtkinter.CTkLabel(self.workFrame, text='Zooming')

        self.zoomButton = customtkinter.CTkCheckBox(self.zoomFrame, text='Zoom',
                                                    command=self.zoom_mode)

        self.unzoomButton = customtkinter.CTkButton(self.zoomFrame, text='<-|->',
                                                    command=self.unzoom_image)

        self.zoomButton.grid(row=0, column=0)
        self.unzoomButton.grid(row=1, column=0)

        self.plusButton = customtkinter.CTkButton(self.workFrame, text='+',
                                                  command=self.plus_box)

        self.zoomFrame.grid(row=0, column=0, padx=5)
        self.plusButton.grid(row=0, column=2, padx=5)

        self.workFrame.grid(row=1, column=1)


    def zoom_mode(self_):
        self = self_.controller
        if self.zoommode:
            self.zoommode = False
        else:
            self.zoommode = True

    def unzoom_image(self_):
        self = self_.controller
        self.canvas.delete(tk.ALL)
        self.zoommode = False
        self_.zoomButton.deselect()
        self.x0 = 0
        self.y0 = 0
        self.region_rect = Rect((0, 0), (self.w, self.h))
        self.zooming = False
        self.displayimage()

    def plus_box(self_):
        self = self_.controller
        if self.n > 1:
            self.canvas.delete(tk.ALL)
            if self.crop_rects:
                ra = self.crop_rects[self.n - 1]
                self.crop_rects.pop()
                self.n -= 1
                ra0 = self.crop_rects[self.n - 1]
                ra0 = ra0.plus_rect(ra)
                self.crop_rects[self.n - 1] = ra0
                self.displayimage()
                self.zoommode = False
                self.zoomButton.deselect()

