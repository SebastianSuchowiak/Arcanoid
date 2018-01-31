

class Animation:

    def __init__(self, images_list, rect):
        self.images_list = images_list
        self.start_len = len(images_list)
        self.rect = rect
        self.current_animation = images_list
        self.animation_speed = 10
        self.status = self.animation_speed - 1

    def get_current(self):
        if len(self.images_list) > 0 and self.status // self.animation_speed != self.start_len:
            self.status += 1
            if self.status % self.animation_speed == 0 and len(self.images_list) > 0:
                self.current_animation = self.images_list.pop()
            return self.current_animation
        return ""
