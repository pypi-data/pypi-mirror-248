import logging
import os
import shutil

from examples import build_dir
from pixel_font_builder import FontBuilder, StyleName, SerifMode, WidthMode, Glyph, opentype

logging.basicConfig(level=logging.DEBUG)


def main():
    outputs_dir = os.path.join(build_dir, 'create')
    if os.path.exists(outputs_dir):
        shutil.rmtree(outputs_dir)
    os.makedirs(outputs_dir)

    builder = FontBuilder(12)

    builder.meta_infos.version = '1.0.0'
    builder.meta_infos.family_name = 'My Pixel'
    builder.meta_infos.style_name = StyleName.REGULAR
    builder.meta_infos.serif_mode = SerifMode.SANS_SERIF
    builder.meta_infos.width_mode = WidthMode.MONOSPACED
    builder.meta_infos.manufacturer = 'Pixel Font Studio'
    builder.meta_infos.designer = 'TakWolf'
    builder.meta_infos.description = 'A demo pixel font.'
    builder.meta_infos.copyright_info = 'Copyright (c) TakWolf'
    builder.meta_infos.license_info = 'This Font Software is licensed under the SIL Open Font License, Version 1.1.'
    builder.meta_infos.vendor_url = 'https://github.com/TakWolf/pixel-font-builder'
    builder.meta_infos.designer_url = 'https://takwolf.com'
    builder.meta_infos.license_url = 'https://scripts.sil.org/OFL'
    builder.meta_infos.sample_text = 'Hello World!'

    builder.horizontal_header.ascent = 10
    builder.horizontal_header.descent = -2

    builder.vertical_header.ascent = 10
    builder.vertical_header.descent = -2

    builder.properties.x_height = 5
    builder.properties.cap_height = 7

    builder.character_mapping.update({
        ord('A'): 'CAP_LETTER_A',
    })

    builder.glyphs.append(Glyph(
        name='.notdef',
        advance_width=8,
        advance_height=12,
        horizontal_origin=(0, -2),
        vertical_origin_y=0,
        data=[
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ],
    ))
    builder.glyphs.append(Glyph(
        name='CAP_LETTER_A',
        advance_width=8,
        advance_height=12,
        horizontal_origin=(0, -2),
        vertical_origin_y=0,
        data=[
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
    ))

    builder.save_otf(os.path.join(outputs_dir, 'my-pixel.otf'))
    builder.save_otf(os.path.join(outputs_dir, 'my-pixel.woff2'), flavor=opentype.Flavor.WOFF2)
    builder.save_ttf(os.path.join(outputs_dir, 'my-font.ttf'))
    builder.save_bdf(os.path.join(outputs_dir, 'my-font.bdf'))


if __name__ == '__main__':
    main()
