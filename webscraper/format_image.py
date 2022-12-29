# loop through the images directory and print the size of each image
import os
import matplotlib.image as mpim
import cv2


# for file in os.listdir('images'):
#     if file.endswith('.jpg'):
#         img = mpim.imread('images/'+file)
#         print(img.shape)
#     else:
#         continue


def resize(path):
    desired_size = (224, 224)
    for file in os.listdir(path):
        if file.endswith('.jpg') or file.endswith('.png'):
            try:
                img = mpim.imread(path+file)
                resized_image = cv2.resize(img, desired_size)
                # create a new direcory in path called resized
                os.makedirs(path+'resized', exist_ok=True)

                mpim.imsave(path+'resized/'+file, resized_image)
            except Exception as e:
                print(e)
                continue


def main(image_site):
    path = "../images/"+image_site + "/"
    resize(path)


if __name__ == '__main__':
    image_site = input("Enter the site name: ")
    main(image_site)
