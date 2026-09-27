from PIL import Image
import math
import os

# Generate exactly 256 UNIQUE colors.
# Each byte has exactly one corresponding RGB color.
RGBI = []

for byte in range(256):
    # 8 bits → 3/3/2 RGB
    r = (byte >> 5) & 0b111
    g = (byte >> 2) & 0b111
    b = byte & 0b11

    RGBI.append((
        r * 255 // 7,
        g * 255 // 7,
        b * 255 // 3
    ))


# Reverse lookup: RGB → original byte
RGBI_REVERSE = {
    rgb: byte
    for byte, rgb in enumerate(RGBI)
}


def encode(data:bytes, width=None, filename="output"):

    if width is None:
        width = math.ceil(math.sqrt(len(data)))

    height = math.ceil(len(data) / width)

    img = Image.new("RGB", (width, height), RGBI[0])
    pixels = img.load()
    x=0
    for i, byte in enumerate(data):
        x = i % width
        y = i // width

        pixels[x, y] = RGBI[byte] # type: ignore
        if not i % (1000000): print(f"Byte {i}/{len(data)}")

    img.save(filename+'.png')

    print(f"\nEncoded {len(data)} bytes\nImage size: {width}x{height}")


def decode(filename="output.png"):
    img = Image.open(filename).convert("RGB")

    data = bytearray()

    for y in range(img.height):
        for x in range(img.width):
            rgb = img.getpixel((x, y))

            data.append(RGBI_REVERSE[rgb])
    return data

with open('vmlinuz', 'rb') as f:
    encode(f.read(), filename=os.path.basename(f.name))
    f.close()