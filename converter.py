from PIL import Image
import argparse
import os

def load_image(filename, target_width, target_height):
    """
    Loads an image, resized it to the target dimensions and returns it's data.
    """

    image = Image.open(filename, 'r')
    image = image.resize((target_width, target_height), Image.NEAREST)
    image_data = image.load()

    return image.size[0], image.size[1], image_data


def get_pixel_intensity(pixel, invert=False, max_value=255):
    """
    Gets the average intensity of a pixel.
    """
    intensity = 0

    # Pixel is multi channel
    if type(pixel) is list or type(pixel) is tuple:
        for channel_intensity in pixel:
            intensity += channel_intensity
        intensity /= len(pixel)
    # Pixel is single channel
    elif type(pixel) is int or type(pixel) is float:
        intensity = pixel
    # Pixel is magic
    else:
        raise ValueError('Not a clue what format the pixel data is: ' + str(type(pixel)))

    if invert:
        return max_value - intensity
    else:
        return intensity


def get_average_pixel_intensity(width, height, pixel_data, invert):
    """
    Gets the average intensity over all pixels.
    """

    avg_intensity = 0

    for x_idx in range(0, width):
        for y_idx in range(0, height):
            avg_intensity += get_pixel_intensity(pixel_data[x_idx, y_idx], invert)

    avg_intensity = avg_intensity / (width * height)

    return avg_intensity


def output_image_c_array(width, height, pixel_data, crossover, output, invert):
    """
    Outputs the data in a C bitmap array format.
    """

    base = os.path.basename(output)
    output_file = open(output, "w")

    line = 'const uint8_t ' + os.path.splitext(base)[0] + '[] U8G_PROGMEM = {' + '\n'
    output_file.write(line)
    line = hex(width/8) + ', ' + hex(height) + ', ' + '// row_bytes = WIDTH/8, HEIGHT' + '\n'
    output_file.write(line)

    for y_idx in range(0, height):
        next_line = ''
        next_value = 0

        for x_idx in range(0, width):
            if (x_idx % 8 == 0 or x_idx == width - 1) and x_idx > 0:
                next_line += str('0x%0.2X' % next_value).lower() + ","
                next_value = 0

            if get_pixel_intensity(pixel_data[x_idx, y_idx], invert) > crossover:
                next_value += 2 ** (7 - (x_idx % 8))

        line = next_line + '\n'
        output_file.write(line)

    line = '};'
    output_file.write(line)
    output_file.close()


def convert(params):
    """
    Runs an image conversion.
    """

    width, height, image_data = load_image(params.image, params.width, params.height)
    if params.threshold == 0:
        crossover_intensity = get_average_pixel_intensity(width, height, image_data, params.invert)
    else:
        crossover_intensity = params.threshold
    output_image_c_array(width, height, image_data, crossover_intensity, params.output, params.invert)


def run():
    """
    Gets parameters and runs conversion.
    """
    parser = argparse.ArgumentParser(description='Convert a bitmap image to a C array for GLCDs')

    parser.add_argument(
            '-i', '--invert',
            action='store_true',
            help='Invert image intensity')

    parser.add_argument(
            '--threshold',
            default=0,
            type=int,
            help='BW pixel intensity threshold')

    parser.add_argument(
            '--width',
            default=64,
            type=int,
            help='Width of the output image')

    parser.add_argument(
            '--height',
            default=128,
            type=int,
            help='Height of the output image')

    parser.add_argument(
            '-f', '--image',
            type=str,
            help='Image input file to convert')

    parser.add_argument(
            '-o', '--output',
            type=str,
            help='Image output file name')

    params = parser.parse_args()
    convert(params)


if __name__ == '__main__':
    run()
