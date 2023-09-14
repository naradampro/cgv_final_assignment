import matplotlib.pyplot as plt
import numpy as np


def display_image(image_path, title):
    # load the image
    image = plt.imread(image_path)

    # display the image
    plt.imshow(image)
    plt.title(title)
    plt.show()


def display_and_compare_images(image_paths, titles):
    num_images = len(image_paths)

    for i in range(num_images):
        image = plt.imread(image_paths[i])
        plt.subplot(1,2,i+1),plt.imshow(image)
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])

    plt.show()


display_image('sign_sheets/1.jpeg', 'Single Image')

image_paths = ['sign_sheets/1.jpeg', 'sign_sheets/2.jpeg']
titles = ['Title 1', 'Title 2']
display_and_compare_images(image_paths, titles)