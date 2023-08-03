import cv2 as cv

SIGN_SHEETS_PATH = "sign_sheets/"


def sign_sheet_image(name):
    return "{}{}.{}".format(SIGN_SHEETS_PATH, name, "jpeg")


img = cv.imread(sign_sheet_image(1))
print(img.shape)
