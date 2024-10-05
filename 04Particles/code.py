import board
import random
import displayio
import rgbmatrix
import framebufferio

bit_depth = 4
base_width = 64
base_height = 32
chain_across = 2
tile_down = 1
serpentine = True

width = base_width * chain_across
height = base_height * tile_down

addr_pins = [board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC, board.MTX_ADDRD]

rgb_pins = [
    board.MTX_R1,
    board.MTX_G1,
    board.MTX_B1,
    board.MTX_R2,
    board.MTX_G2,
    board.MTX_B2,
]
clock_pin = board.MTX_CLK
latch_pin = board.MTX_LAT
oe_pin = board.MTX_OE

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
                width=width,
                height=height,
                bit_depth=bit_depth,
                rgb_pins=rgb_pins,
                addr_pins=addr_pins,
                clock_pin=clock_pin,
                latch_pin=latch_pin,
                output_enable_pin=oe_pin,
                tile=tile_down, serpentine=serpentine,
            )
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

# matrix = rgbmatrix.RGBMatrix(     # M4 pinouts
#     width=64, height=32, bit_depth=1,
#     rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
#     addr_pins=[board.A5, board.A4, board.A3, board.A2],
#     clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

# Create a bitmap with two colors
bitmap = displayio.Bitmap(display.width, display.height, 2)

# Create a two color palette
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0x002000

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create a Group
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.root_group = group

def add_matrix(a,b):
    return [a[0] + b[0], a[1] + b[1]]

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.position = [x, y]
        self.velocity = [random.randint(-1, 1), random.randint(-2, 0)]
        self.acceleration = [0, 0]
        self.lifespan = 60
    def run(self):
        gravity = [0, 0.005]
        self.applyForce(gravity)
        self.update()
        self.show()
    
    def update(self):
        self.velocity = add_matrix(self.velocity, self.acceleration)
        self.position = add_matrix(self.position, self.velocity)
        self.x = int(self.position[0])
        self.y = int(self.position[1])
        self.lifespan -= 1
        # self.acceleration.mult(0)

    def show(self):
        # bitmap.fill(0)
        if self.y < (height-1) and self.y >= 0 and self.x < (width-1) and self.x >= 0:
            bitmap[self.x, self.y] = 1

    def applyForce(self, force):
        self.acceleration = add_matrix(self.acceleration, force)

    def isDead(self):
        return (self.lifespan < 0)

particles = []

while True:
    bitmap.fill(0)
    particles.append(Particle(random.randint(0, 127), random.randint(0, 15)))
    # print(particles)
    for i in range(len(particles)-1,0,-1):
        particle = particles[i]
        particle.run()
        if particle.isDead():
            particles.remove(particle)
    print(len(particles))
    display.refresh(minimum_frames_per_second=0)