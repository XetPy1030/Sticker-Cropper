from random import random

from components.rect import Rect
import tkinter as tk


class MouseEngine:
    def __init__(self, controller):
        self.controller = controller

    def init_update(self, event):
        pass

    def update(self, event):
        pass

    def end(self, event):
        pass

    def check(self, event) -> bool:
        return False


class ChangeSizeRectEngine(MouseEngine):
    def __init__(self, controller):
        super().__init__(controller)

        controller.canvas.bind('<Motion>', self.move_cursor, add=True)

        self.max_diff_near_border = 6
        self.border = None  # top, bottom, left, right
        self.rect: Rect

    def move_cursor(self, event):
        x, y = event.x, event.y

        if not self.check(event):
            self.controller.canvas.config(cursor='arrow')
            return

        border = self.get_border(x, y)
        if border == 'left' or border == 'right':
            self.controller.canvas.config(cursor='sb_h_double_arrow')
        elif border == 'top' or border == 'bottom':
            self.controller.canvas.config(cursor='sb_v_double_arrow')
        else:
            self.controller.canvas.config(cursor='arrow')

    def check(self, event) -> bool:
        x, y = event.x, event.y

        for croparea in self.controller.crop_rects:
            rs_ca = croparea.rescale_rect(self.controller.scale, self.controller.x0, self.controller.y0)
            if ((rs_ca.left - self.max_diff_near_border < x < rs_ca.left + self.max_diff_near_border or
                 rs_ca.right - self.max_diff_near_border < x < rs_ca.right + self.max_diff_near_border)
                and rs_ca.top < y < rs_ca.bottom
            ) or \
                    ((rs_ca.top - self.max_diff_near_border < y < rs_ca.top + self.max_diff_near_border or
                      rs_ca.bottom - self.max_diff_near_border < y < rs_ca.bottom + self.max_diff_near_border)
                     and rs_ca.left < x < rs_ca.right
                    ):
                return True

        return False

    def get_crop_rect(self, x, y) -> 'Rect':
        for croparea in self.controller.crop_rects:
            rs_ca = croparea.rescale_rect(self.controller.scale, self.controller.x0, self.controller.y0)
            if ((rs_ca.left - self.max_diff_near_border < x < rs_ca.left + self.max_diff_near_border or
                 rs_ca.right - self.max_diff_near_border < x < rs_ca.right + self.max_diff_near_border)
                and rs_ca.top < y < rs_ca.bottom
            ) or \
                    ((rs_ca.top - self.max_diff_near_border < y < rs_ca.top + self.max_diff_near_border or
                      rs_ca.bottom - self.max_diff_near_border < y < rs_ca.bottom + self.max_diff_near_border)
                     and rs_ca.left < x < rs_ca.right
                    ):
                return croparea

    def get_border(self, x, y) -> str:
        for croparea in self.controller.crop_rects:
            rs_ca = croparea.rescale_rect(self.controller.scale, self.controller.x0, self.controller.y0)
            if ((rs_ca.left - self.max_diff_near_border < x < rs_ca.left + self.max_diff_near_border)
                    and rs_ca.top < y < rs_ca.bottom
            ):
                return 'left'
            elif ((rs_ca.right - self.max_diff_near_border < x < rs_ca.right + self.max_diff_near_border)
                  and rs_ca.top < y < rs_ca.bottom
            ):
                return 'right'
            elif ((rs_ca.top - self.max_diff_near_border < y < rs_ca.top + self.max_diff_near_border)
                  and rs_ca.left < x < rs_ca.right
            ):
                return 'top'
            elif ((rs_ca.bottom - self.max_diff_near_border < y < rs_ca.bottom + self.max_diff_near_border)
                  and rs_ca.left < x < rs_ca.right
            ):
                return 'bottom'

    def init_update(self, event):
        self.border = self.get_border(event.x, event.y)
        self.rect = self.get_crop_rect(event.x, event.y)

    def update(self, event):
        x = (event.x - self.max_diff_near_border * 2) * self.controller.scale[0]
        y = (event.y - self.max_diff_near_border * 2) * self.controller.scale[1]

        if self.border == 'left':
            self.rect.left = x
        elif self.border == 'right':
            self.rect.right = x
        elif self.border == 'top':
            self.rect.top = y
        elif self.border == 'bottom':
            self.rect.bottom = y

        if not self.controller.checkButton.get():
            self.controller.redraw()
        else:
            self.controller.redraw_rect()

    def end(self, event):
        self.rect = None
        self.border = None
        self.controller.redraw()


class MoveRectEngine(MouseEngine):
    def __init__(self, controller):
        super().__init__(controller)

        self.move_start = None
        self.move_rect: Rect

    def check(self, event) -> bool:
        x, y = event.x, event.y
        for croparea in self.controller.crop_rects:
            rs_ca = croparea.rescale_rect(self.controller.scale, self.controller.x0, self.controller.y0)
            left, top, right, bottom = rs_ca.left, rs_ca.top, rs_ca.right, rs_ca.bottom

            if left < x < right and top < y < bottom:
                return True
        return False

    def get_crop_rect(self, x, y) -> 'Rect':
        for croparea in self.controller.crop_rects:
            rs_ca = croparea.rescale_rect(self.controller.scale, self.controller.x0, self.controller.y0)
            if rs_ca.left < x < rs_ca.right and rs_ca.top < y < rs_ca.bottom:
                return croparea

    def init_update(self, event):
        self.move_start = (event.x, event.y)
        self.move_rect = self.get_crop_rect(event.x, event.y)

    def update(self, event):
        dx = event.x - self.move_start[0]
        dx = dx * self.controller.scale[0]
        dy = event.y - self.move_start[1]
        dy = dy * self.controller.scale[1]
        self.move_rect.self_move(dx, dy)
        self.move_start = (event.x, event.y)

        if self.controller.checkButton.get():
            self.controller.redraw_rect()
        else:
            self.controller.redraw()

    def end(self, event):
        self.move_rect = None
        self.controller.redraw()


class DrawRectEngine(MouseEngine):
    def __init__(self, controller):
        super().__init__(controller)

    def check(self, event) -> bool:
        return True

    def update(self_, event):
        self = self_.controller
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        x1, y1 = self.croprect_start
        x2 = event.x

        if self.is_shift:
            if event.y > y1:
                diff = x2 - x1
            else:
                diff = x1 - x2

            if event.x < x1:
                diff = -diff

            y2 = y1 + diff
        else:
            y2 = event.y

        bbox = (x1, y1, x2, y2)
        dx = int((x2 - x1) * self.scale[0] * 10 + 0.5) * 0.1
        dy = int((y2 - y1) * self.scale[1] * 10 + 0.5) * 0.1
        dt = str(round(dx)) + " x " + str(round(dy))
        cr = self.canvas.create_rectangle(bbox)
        self.current_rect = cr
        self.sizeLabel.configure(text=dt)

    def end(self_, event):
        self = self_.controller

        if self.is_shift:
            x1, y1 = self.croprect_start
            x2 = event.x
            if event.y > y1:
                diff = x2 - x1
            else:
                diff = x1 - x2

            if event.x < x1:
                diff = -diff

            y2 = y1 + diff
            self.croprect_end = (x2, y2)
        else:
            self.croprect_end = (event.x, event.y)

        self_.set_crop_area()
        self.canvas.delete(self.current_rect)
        self.current_rect = None

    def set_crop_area(self_):
        self = self_.controller

        r = Rect(self.croprect_start, self.croprect_end)

        # adjust dimensions
        r.clip_to(self.image_thumb_rect)

        # ignore rects smaller than this size
        if min(r.h, r.w) < 10:
            return

        ra = r
        ra = ra.scale_rect(self.scale)
        ra = ra.move_rect(self.x0, self.y0)
        ra = ra.valid_rect(self.w, self.h)
        if self.zoommode:
            self.canvas.delete(tk.ALL)
            self.x0 = ra.left
            self.y0 = ra.top
            self.region_rect = ra
            self.displayimage()
            self.zoommode = False
            self.work_action_frame.zoomButton.deselect()
            self.zooming = True
        else:
            self.drawrect(r)
            self.crop_rects.append(ra)
            self.n = self.n + 1
        self.set_button_state()
