from __future__ import division

from PIL import Image

def avghash(image_path, hash_size=8):
    """ Compute the average hash of the given image. """
    with open(image_path, 'rb') as f:
        # Open the image, resize it and convert it to black & white.
        image = Image.open(f).resize((hash_size, hash_size), Image.ANTIALIAS).convert('L')
        pixels = list(image.getdata())
        print(pixels)
    avg = sum(pixels) / len(pixels)

    # Compute the hash based on each pixels value compared to the average.
    bits = "".join(map(lambda pixel: '1' if pixel > avg else '0', pixels))
    #print(avg,bits)
    hashformat = "0{hashlength}x".format(hashlength=hash_size ** 2 // 4)
    #print(hashformat)
    return int(bits, 2).__format__(hashformat)


import photohash
hash1=avghash("../WaveReconize/figure/fq156223.9.jpg")
hash2=avghash("../WaveReconize/figure/fq156223.9.jpg")
distance = photohash.hash_distance(hash1, hash2)
print(hash1,hash2,distance)