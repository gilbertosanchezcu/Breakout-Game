import tkinter
import time
from bricks import Brick

# Width of drawing canvas in pixels CANVAS_HEIGHT = 600
CANVAS_WIDTH = 625

# Height of drawing canvas in pixels
CANVAS_HEIGHT = 650

#PADDLE_Y = CANVAS_HEIGHT - 40
PADDLE_Y = CANVAS_HEIGHT - 70
#PADDLE_WIDTH = 100

PADDLE_WIDTH = 100

N_ROWS = 10
N_COLS = 8
SIZE = CANVAS_HEIGHT / N_ROWS - 1

# BALL_SIZE = 30
BALL_SIZE = 280


class Game:

    def __init__(self):
        self.canvas = self.make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Breakout')
        self.ball = self.canvas.create_oval(250, 250, BALL_SIZE, BALL_SIZE, fill='red', outline='red')
        self.paddle = self.canvas.create_rectangle(0, PADDLE_Y, PADDLE_WIDTH, CANVAS_HEIGHT - 50, fill="blue")

        self.bricks_list = self.create_bricks(self.canvas)
        self.display_bricks(self.bricks_list)
        self.score = 0
        self.score_count(self.canvas, self.score)

        self.dx = 10
        self.dy = 6

    def main(self):
        while True:
            # get the mouse location and react to it
            mouse_x = self.canvas.winfo_pointerx()
            self.canvas.moveto(self.paddle, mouse_x, PADDLE_Y)

            self.canvas.move(self.ball, self.dx, self.dy)
            if self.hit_left_wall(self.canvas, self.ball) or self.hit_right_wall(self.canvas, self.ball):
                self.dx *= -1
            if self.hit_top_wall(self.canvas, self.ball):
                self.dy *= -1

            # check if the ball hits the paddle
            if self.hit_paddle(self.canvas, self.ball, self.paddle):
                self.dy *= -1

            x = self.hit_brick(self.bricks_list, self.canvas)
            if x is not False:
                if x.hits == 0:
                    x.is_hit()
                elif x.hits == 1:
                    remove_obj = self.bricks_list[x.gridID[0]][x.gridID[1]]
                    self.canvas.delete(remove_obj)
                    x.is_hit()
                    self.bricks_list[x.gridID[0]][x.gridID[1]] = None
                    self.score += 1

                self.canvas.delete('counter')
                self.score_count(self.canvas, self.score)

                self.dy *= -1

            # redraw canvas
            self.canvas.update()
            # pause
            time.sleep(1 / 50.)
        return

    def score_count(self, canvas, score):
        counter = canvas.create_text(550, 640, text='Score Count: ' + str(score), tag='counter')
        return counter

    def create_bricks(self, canvas):
        bricks_grid = []
        for rows in range(5):
            row = []
            for cols in range(7):
                row.append(Brick(canvas, rows, cols))
            bricks_grid.append(row)

        return bricks_grid

    def display_bricks(self, brick_list):
        # brick_list 2D array
        grid_pos = [[[0, 0, 85, 24], [90, 0, 175, 24], [180, 0, 265, 24], [270, 0, 355, 24], [360, 0, 445, 24],[450, 0, 535, 24], [540, 0, 625, 24]],
                    [[0, 29, 85, 53], [90, 29, 175, 53], [180, 29, 265, 53], [270, 29, 355, 53], [360, 29, 445, 53], [450, 29, 535, 53], [540, 29, 625, 53]],
                    [[0, 58, 85, 82], [90, 58, 175, 82], [180, 58, 265, 82], [270, 58, 355, 82], [360, 58, 445, 82], [450, 58, 535, 82], [540, 58, 625, 82]],
                    [[0, 87, 85, 111], [90, 87, 175, 111], [180, 87, 265, 111], [270, 87, 355, 111], [360, 87, 445, 111], [450, 87, 535, 111], [540, 87, 625, 111]],
                    [[0, 116, 85, 140], [90, 116, 175, 140], [180, 116, 265, 140], [270, 116, 355, 140], [360, 116, 445, 140], [450, 116, 535, 140], [540, 116, 625, 140]]
                    ]

        for row in range(len(brick_list)):
            for col in range(len(brick_list[row])):
                pos = grid_pos[row][col]
                brick_list[row][col].create_brick(pos[0], pos[1], pos[2], pos[3])
        return

    def hit_brick(self, brick_list, canvas):
        # ball_coords = canvas.coords(ball)
        for row in brick_list:
            for obj in row:
                if obj is not None:
                    brick_coords = obj.get_coords()
                    x1 = brick_coords[0]
                    y1 = brick_coords[1]
                    x2 = brick_coords[2]
                    y2 = brick_coords[3]
                    results = canvas.find_overlapping(x1, y1, x2, y2)
                    if len(results) > 1:
                        return obj

        return False

    def hit_paddle(self, canvas, ball, paddle):
        # paddle_coords is of type list.
        paddle_coords = canvas.coords(paddle)
        x1 = paddle_coords[0]
        y1 = paddle_coords[1]
        x2 = paddle_coords[2]
        y2 = paddle_coords[3]
        results = canvas.find_overlapping(x1, y1, x2, y2)
        return len(results) > 1

    def hit_left_wall(self, canvas, object):
        return self.get_left_x(canvas, object) <= 0

    def hit_top_wall(self, canvas, object):
        return self.get_top_y(canvas, object) <= 0

    def hit_right_wall(self, canvas, object):
        return self.get_right_x(canvas, object) >= CANVAS_WIDTH

    def hit_bottom_wall(self, canvas, object):
        return self.get_bottom_y() >= CANVAS_HEIGHT

    def get_left_x(self, canvas, object):
        return canvas.coords(object)[0]

    def get_top_y(self, canvas, object):
        return canvas.coords(object)[1]

    def get_right_x(self, canvas, object):
        return canvas.coords(object)[2]

    def get_bottom_y(self, canvas, object):
        return canvas.coords(object)[3]

    def make_canvas(self, width, height, title):
        top = tkinter.Tk()
        top.minsize(width=width, height=height)
        top.title(title)
        canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
        canvas.pack()
        return canvas


if __name__ == '__main__':
    game = Game()
    game.main()
