import board
import displayio
import rgbmatrix
import framebufferio
import vectorio

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

circle = vectorio.Circle(pixel_shader=palette, color_index=1, radius=3, x=70, y=10)
group.append(circle)

position = [10,15]
velocity = [1,1]

def add_matrix(a,b):
    return [a[0] + b[0], a[1] + b[1]]

def draw():
    global position
    newpos = add_matrix(position, velocity)
    # print(newpos)
    if ((newpos[0]+circle.radius) > width) or ((newpos[0]-circle.radius) < 0):
        velocity[0] = velocity[0] * -1
    if ((newpos[1]+circle.radius) > height) or ((newpos[1]-circle.radius) < 0):
        velocity[1] = velocity[1] * -1
    circle.x = newpos[0]
    circle.y = newpos[1]
    position = newpos

# a + b = (a1 + b1, a2 + b2, a3 + b3) 
while True:
    draw()
    display.refresh(minimum_frames_per_second=0)