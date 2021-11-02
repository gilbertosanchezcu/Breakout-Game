import tkinter


class Brick:
    def __init__(self, canvas, row, col):
        self.canvas = canvas
        #self.hit = False
        self.hits = 0
        self.colors = ['black', 'red']
        self.gridID = [row, col]

    def is_hit(self):
        #self.canvas.itemconfig(self.brick1, fill=self.colors[1])
        if self.hits == 0:
            self.hits += 1
            self.canvas.itemconfig(self.brick1, fill=self.colors[1])
            return

        if self.hits == 1:
            self.remove_brick(self.brick1)
            return

    def create_brick(self, x1, y1, x2, y2):
        # paddle = canvas.create_rectangle(0, PADDLE_Y, PADDLE_WIDTH, CANVAS_HEIGHT - 20, fill="blue")
        self.brick1 = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.colors[0])

    def get_coords(self):
        return self.canvas.coords(self.brick1)

    def remove_brick(self, item):
        return self.canvas.delete(item)
