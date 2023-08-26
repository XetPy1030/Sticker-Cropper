import os

import customtkinter
import tkinter as tk

from components.rect import Rect


class ActionFrame:
    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent

        self.action_frame = customtkinter.CTkFrame(parent)
        self.action_frame.grid(row=1, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.action_label = customtkinter.CTkLabel(self.action_frame, text='Action')
        self.action_label.grid(row=0, column=2, columnspan=1, padx=10, pady=(0, 10), sticky="")

        self.resetButton = customtkinter.CTkButton(self.action_label, text='Reset',
                                                   command=self.reset)

        self.undoButton = customtkinter.CTkButton(self.action_label, text='Undo',
                                                  command=self.controller.undo_last)

        self.goButton = customtkinter.CTkButton(self.action_label, text='Save Crops',
                                                command=self.controller.start_cropping)

        # self.quitButton = customtkinter.CTkButton(self.action_label, text='Quit',
        #                                           command=parent.quit)
        self.redrawButton = customtkinter.CTkButton(self.action_label, text='Redraw',
                                                    command=self.redraw)

        self.resetButton.grid(row=1, column=0)
        self.undoButton.grid(row=2, column=0)
        self.goButton.grid(row=1, column=1)
        # self.quitButton.grid(row=2, column=1)
        self.redrawButton.grid(row=2, column=1)

    def redraw(self):
        self.controller.redraw()

    def reset(self):
        self.controller.canvas.delete(tk.ALL)
        self.controller.zoommode = False
        self.controller.work_action_frame.zoomButton.deselect()
        self.controller.zooming = False
        self.controller.countour = False
        self.controller.countourButton.deselect()
        self.controller.canvas_rects = []
        self.controller.crop_rects = []
        self.controller.region_rect = Rect((0, 0), (self.controller.w, self.controller.h))
        self.controller.n = 0
        self.controller.x0 = 0
        self.controller.y0 = 0

        self.controller.displayimage()


