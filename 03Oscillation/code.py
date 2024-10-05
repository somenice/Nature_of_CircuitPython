import board
import displayio
import rgbmatrix
import framebufferio
import vectorio
import math

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

startAngle = 0
deltaAngle = 0.2
angle = startAngle

for i in range(0,127,4):
    unique_name = "circle" + str(i)
    unique_name = displayio.Group()
    circle = vectorio.Circle(pixel_shader=palette, color_index=1, radius=4, x=i+2, y=12)
    unique_name.append(circle)
    group.append(unique_name)

def draw():
    global angle
    for x in group:
        x.y = int(map_range(math.sin(angle), -1, 1, 0, height))-12
        angle += deltaAngle

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
    draw()
    display.refresh(minimum_frames_per_second=0)