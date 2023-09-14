import matplotlib.pyplot as plt


def compare_two(original_image, result):
    fig, axes = plt.subplots(1, 2)

    axes[0].set_title("Input Image")
    axes[0].imshow(original_image, cmap=plt.cm.gray)

    axes[1].set_title("Output image")
    axes[1].imshow(result, cmap=plt.cm.gray)

    plt.tight_layout()
    plt.show()


def add_two(first, second, result):
    fig, axes = plt.subplots(1, 3)

    axes[0].set_title("Input 1")
    axes[0].imshow(first, cmap=plt.cm.gray)

    axes[1].set_title("Input 2")
    axes[1].imshow(second, cmap=plt.cm.gray)

    axes[2].set_title("Output image")
    axes[2].imshow(result, cmap=plt.cm.gray)

    plt.tight_layout()
    plt.show()


def img(image, title="Image Title"):
    plt.imshow(image, cmap=plt.cm.gray)
    plt.title(title)
    plt.show()
