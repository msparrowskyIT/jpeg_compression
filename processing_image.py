import cv2
import numpy as np
import quality_array as qa

array_128_8x8 = np.ones((8, 8)) * 128;

def split_to_block_8x8(channel):
    height, width = channel.shape
    blocks = []
    y=0
    for i in range(8, height+1, 8):
        x = 0
        for j in range(8, width + 1, 8):
            blocks.append(channel[y:i, x:j] - array_128_8x8)
            x = j
        y = i
    return [np.float32(block) for block in blocks]

def apply_quality_array(dtc_blocks, quality_array_name):
    quality_array = qa.get_quality_array(quality_array_name)
    for dtc_block in dtc_blocks:
        for i in range(8):
            for j in range(8):
                dtc_block[i, j] = np.around(dtc_block[i, j] / quality_array[i, j])

def encode(channel, quality_array_name):
    blocks = split_to_block_8x8(channel)
    dct_blocks =  [cv2.dct(block) for block in blocks]
    apply_quality_array(dct_blocks, quality_array_name)
    return dct_blocks

def decode(dct_blocks):
    return [cv2.idct(dtc_block) for dtc_block in dct_blocks]

def merge_block_8x8(idct_blocks,width):
    row = 0
    rowNcol = []
    for j in range(int(width / 8), len(idct_blocks) + 1, int(width / 8)):
        rowNcol.append(np.hstack((idct_blocks[row:j])))
        row = j
    return normalize(np.vstack((rowNcol)))

def process_image(channel, quality_array_name):
    encoded_channel = encode(channel, quality_array_name)
    decoded_channel = decode(encoded_channel)
    return merge_block_8x8(decoded_channel, len(channel[0]))

def normalize(channel):
    channel = channel - channel.mean()
    channel =  channel / (2*channel.max()) + 0.5
    return channel
