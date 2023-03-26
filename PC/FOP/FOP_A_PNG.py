from PIL import Image

#descomprimir el archivo FNT2626.FOP con decompressbip y luego usarlo con este script.

def get_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

input_filename = input("Nombre del archivo de la fuente (BIP descomprimido) FOP/FNT: ")
in_fil = f'{input_filename}'
out_fil = f'fnt/{input_filename.split(".")[0]}.PNG'


in_fil, out_fil = f'{input_filename}', f'fnt/{input_filename.split(".")[0]}.PNG'
dat = get_file(in_fil)
data_len = len(dat)
GLYPH_BYTE_WIDTH = 12
GLYPH_PIXEL_WIDTH = 4 * GLYPH_BYTE_WIDTH
GLYPH_BYTE_HEIGHT = 48
GLYPH_PIXEL_HEIGHT = GLYPH_BYTE_HEIGHT
GLYPH_BYTES = GLYPH_BYTE_WIDTH * GLYPH_BYTE_HEIGHT
FONT_HEADER_BYTES = int.from_bytes(dat[0x10:0x14], byteorder='little')
N_GLYPHS = (data_len - FONT_HEADER_BYTES) // GLYPH_BYTES
SIZE_DATA_STARTS = int.from_bytes(dat[0x08:0x0c], byteorder='little')
SIZE_DATA_SIZE = int.from_bytes(dat[0x0c:0x10], byteorder='little')
if N_GLYPHS * 2 != SIZE_DATA_SIZE:
    print(f"Warning: Glyph count mismatch {N_GLYPHS} vs {SIZE_DATA_SIZE / 2}")
size_data = list(dat[SIZE_DATA_STARTS:SIZE_DATA_STARTS + SIZE_DATA_SIZE])
MAX_IMAGE_WIDTH = 1270
GLYPHS_PER_ROW = int(MAX_IMAGE_WIDTH / GLYPH_PIXEL_WIDTH)
GLYPHS_PER_ROW = 188
GLYPHS_PER_ROW = 26
IMAGE_ROWS = (N_GLYPHS - 1) // GLYPHS_PER_ROW + 1
print(f"Planning to print {N_GLYPHS} glyphs in {IMAGE_ROWS} rows of {GLYPHS_PER_ROW}")
print(f"Total of {FONT_HEADER_BYTES} bytes in header.")
print(f"Excess is {data_len - FONT_HEADER_BYTES - N_GLYPHS * GLYPH_BYTES}.")
print(f"Excess glyphs are {IMAGE_ROWS * GLYPHS_PER_ROW - N_GLYPHS}.")
X_SIZE = GLYPH_PIXEL_WIDTH * GLYPHS_PER_ROW
Y_SIZE = GLYPH_PIXEL_HEIGHT * IMAGE_ROWS
image = Image.new('RGB', (X_SIZE, Y_SIZE), (255, 255, 255))
pixels = image.load()
for i in range(N_GLYPHS):
    row = i // GLYPHS_PER_ROW
    col = i % GLYPHS_PER_ROW
    glyph_start = FONT_HEADER_BYTES + i * GLYPH_BYTES
    glyph_bytes = dat[glyph_start:glyph_start + GLYPH_BYTES]
    size_byte_offset = (i * 2) % SIZE_DATA_SIZE
    dx = size_data[size_byte_offset]
    dy = size_data[size_byte_offset + 1]
    for y in range(GLYPH_PIXEL_HEIGHT):
        byte_pos = y * GLYPH_BYTE_WIDTH
        for x in range(GLYPH_PIXEL_WIDTH):
            bit_pos = 6 - 2 * (x % 4)
            byte_val = glyph_bytes[byte_pos + x // 4]
            bit_val = (byte_val >> bit_pos) & 0x03
            pixel_val = 255 - 85 * bit_val
            pixels[col * GLYPH_PIXEL_WIDTH + x, row * GLYPH_PIXEL_HEIGHT + y] = (pixel_val, pixel_val, pixel_val)
image.save(out_fil)
print(f"Output written to {out_fil}")
