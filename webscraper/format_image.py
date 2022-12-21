# loop through the images directory and print the size of each image
import os
import matplotlib.image as mpim
import cv2


for file in os.listdir('images'):
    if file.endswith('.jpg'):
        img = mpim.imread('images/'+file)
        print(img.shape)
    else:
        continue


def resize(path):
    desired_size = (224, 224)
    for file in os.listdir(path):
        if file.endswith('.jpg'):
            img = mpim.imread('images/'+file)
            resized_image = cv2.resize(img, desired_size)
            # create a new direcory in path called resized
            os.makedirs('images/resized', exist_ok=True)

            mpim.imsave('images/resized/'+file, resized_image)


def main():
    path = "images"
    resize(path)


if __name__ == '__main__':
    main()
