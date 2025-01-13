from pgzero.builtins import Actor

def build(filename, tile_size, offset_x=9, offset_y=9):
    with open(filename, "r") as f:
        contents = [list(map(int, row.split(","))) for row in f.read().splitlines()]

    items = []
    for row, line in enumerate(contents):
        for col, tile_num in enumerate(line):
            if tile_num >= 0:
                item = Actor(f"tiles/tile_{tile_num:04d}", (col * tile_size + offset_x, row * tile_size + offset_y))
                items.append(item)

    return items

class SpriteActor(Actor):
    def __init__(self, images, pos=(0, 0), fps=5):
        super().__init__(images[0], pos)
        self.images = images
        self.current_frame = 0
        self.fps = fps
        self.last_update_time = 0

    def animate(self, time_now):
        if time_now - self.last_update_time > 1 / self.fps:
            self.last_update_time = time_now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]