import numpy as np

import matplotlib.pyplot as plt

def createimage(inputString, width, height):
    rawData = np.array(list(inputString)).astype(np.uint8)
    image = rawData.reshape((25, 6, len(rawData)//(width*height)), order='F')
    return image

if __name__ == '__main__':
    with open('./input.txt') as f:
        inputString = f.read()
    image = createimage(inputString, 25, 6)
    nZeros = np.array([np.sum(image[:, :, i] == 0, (0, 1)) for i in range(image.shape[2])])
    minZeros = np.argmin(nZeros)
    minZeroLayer = image[:, :, minZeros]
    print(np.sum(minZeroLayer == 1, (0, 1))*np.sum(minZeroLayer == 2, (0, 1)))

    newImage = np.ones((25, 6))*2
    for i in range(image.shape[2]):
        for j in range(25):
            for k in range(6):
                if newImage[j, k] == 2:
                    newImage[j, k] = image[j, k, i]
    plt.pcolormesh(newImage)
    plt.show()



