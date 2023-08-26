#!/usr/bin/env python
from typing import List, Optional

import customtkinter

from components.action_frame import ActionFrame
from components.image_action import ImageActionFrame
from components.image_core import ImageCore
from components.mouse_engines import MoveRectEngine, DrawRectEngine, MouseEngine, ChangeSizeRectEngine
from components.rect import Rect
from components.work_action_frame import WorkActionFrame
from config import thumbsize

PROGNAME = 'Cropper-Tk'
VERSION = '0.20210423'

import argparse
import tkinter as tk


class Application(customtkinter.CTk, ImageCore):
    def __init__(self, master=None, filename=None):
        super().__init__(master)
        self.create_widgets()
        self.croprect_start = None
        self.croprect_end = None
        self.canvas_rects = []
        self.crop_rects: List[Rect] = []
        self.region_rect = []
        self.current_rect = None
        self.zoommode = False
        self.countour = False
        self.zooming = False
        self.w = 1
        self.h = 1
        self.x0 = 0
        self.y0 = 0
        self.scale = None
        self.n = 0

        self.folder_cropped_stickers = 'cropped_stickers'
        self.is_shift = False

        self.engines_mouse = [
            ChangeSizeRectEngine(self),
            MoveRectEngine(self),
            DrawRectEngine(self),
        ]
        self.current_engine_mouse: Optional[MouseEngine] = None

        # if not (filename):
        #     filenames = tkfd.askopenfilenames(master=self,
        #                                       defaultextension='.jpg',
        #                                       multiple=1, parent=self,
        #                                       filetypes=(
        #                                           (('Image Files'),
        #                                            '.jpg .JPG .jpeg .JPEG .png .PNG .tif .TIF .tiff .TIFF'),
        #                                           (('JPEG Image Files'),
        #                                            '.jpg .JPG .jpeg .JPEG'),
        #                                           (('PNG Image Files'),
        #                                            '.png .PNG'),
        #                                           (('TIFF Image Files'),
        #                                            '.tif .TIF .tiff .TIFF'),
        #                                           (('All files'), '*'),
        #                                       ),
        #                                       title=('Select images to crop'))
        #     if filenames:
        #         filename = filenames[0]
        #
        # if filename:
        #     self.filename = filename
        #     self.loadimage()
        #     self.focus()
        # else:
        #     self.quit()

        self.image_action_frame.init_image()

    def shift_down(self, event):
        # self.is_shift = True
        pass

    def shift_up(self, event):
        self.is_shift = not self.is_shift

    def create_widgets(self):
        self.canvas = tk.Canvas(
            self, height=1, width=1, relief=tk.SUNKEN)

        self.canvas.bind_all('<KeyPress-Shift_L>', self.shift_down, add=True)
        self.canvas.bind_all('<KeyRelease-Shift_L>', self.shift_up, add=True)

        self.canvas.bind_all('<Control-z>', self.undo_event)

        self.canvas.bind('<Button-1>', self.canvas_mouse1_callback)
        self.canvas.bind('<ButtonRelease-1>', self.canvas_mouseup1_callback)
        self.canvas.bind('<B1-Motion>', self.canvas_mouseb1move_callback)

        self.sizeLabel = customtkinter.CTkLabel(self, text="0x0")


        self.bottom_panel_frame = customtkinter.CTkFrame(self)
        self.bottom_panel_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.countourButton = customtkinter.CTkCheckBox(self.bottom_panel_frame, text='Контур',
                                                        command=self.countour_mode)
        self.countourButton.grid(row=1, column=0)

        self.checkButton = customtkinter.CTkCheckBox(self.bottom_panel_frame, text='Скорость')
        self.checkButton.grid(row=1, column=3)

        self.work_action_frame = WorkActionFrame(self.bottom_panel_frame, self)
        self.action_frame = ActionFrame(self.bottom_panel_frame, self)

        self.image_action_frame = ImageActionFrame(self, self)

        self.canvas.grid(row=0, columnspan=3)
        self.sizeLabel.grid(row=3, column=0, columnspan=3)

    def undo_event(self, event):
        self.undo_last()

    def undo_last(self):
        if self.n > 0:
            if self.canvas_rects:
                r = self.canvas_rects.pop()
                self.canvas.delete(r)
            if self.crop_rects:
                self.crop_rects.pop()
            self.n -= 1
        self.set_button_state()
        self.redraw()

    def set_button_state(self):
        pass
        # if self.n > 0:
        #     self.plusButton.config(state='normal')
        # self.undoButton.config(state='normal')
        # self.goButton.config(state='normal')
        # else:
        #     self.plusButton.config(state='disabled')
        # self.undoButton.config(state='disabled')
        # self.goButton.config(state='disabled')
        # if self.zooming:
        # self.unzoomButton.config(state='normal')
        # else:
        # self.unzoomButton.config(state='disabled')

    def canvas_mouse1_callback(self, event):
        self.croprect_start = (event.x, event.y)

        for engine in self.engines_mouse:
            if engine.check(event):
                self.current_engine_mouse = engine
                self.current_engine_mouse.init_update(event)
                break

    def canvas_mouseb1move_callback(self, event):
        if self.current_engine_mouse:
            self.current_engine_mouse.update(event)
            return

    def canvas_mouseup1_callback(self, event):
        if self.current_engine_mouse:
            self.current_engine_mouse.end(event)
            self.current_engine_mouse = None
            return

    def redraw(self):
        self.canvas.delete(tk.ALL)
        self.displayimage()
        self.redraw_rect()

    def countour_mode(self):
        if self.countour:
            self.countour = False
        else:
            self.countour = True
        self.displayimage()

    def redraw_rect(self):
        for croparea in self.crop_rects:
            self.drawrect(croparea.rescale_rect(self.scale, self.x0, self.y0))

    def drawrect(self, rect):
        bbox = (rect.left, rect.top, rect.right, rect.bottom)
        cr = self.canvas.create_rectangle(
            bbox, activefill='', fill='red', stipple='gray25')
        self.canvas_rects.append(cr)


def main(filename):
    app = Application(filename=filename)
    app.attributes('-fullscreen', True)
    app.title(PROGNAME)
    app.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Cropper Image')
    parser.add_argument('filename', nargs='?', default=None,
                        help='image file name')
    args = parser.parse_args()
    main(args.filename)
