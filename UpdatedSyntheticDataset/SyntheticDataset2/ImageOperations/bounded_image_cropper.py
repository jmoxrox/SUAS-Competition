from PIL import Image

class BoundedImageCropper(object):
    """
    Crop an image, so that only a rectangle with the pixels of the intended color remain
    """
    @staticmethod
    def crop_bounded_image(image, pixel_data, color):
        """
        :param image: an image to be cropped
        :param pixel_data: the pixel data of the image, obtained by calling image.load()
        :param color: the color to serve as the criterion of cropping
        :type image: png, jpg, or other image files
        :type pixel_data: PIL.PyAccess
        :type color: (R, G, B, A) (:type R, G, B, and A: int from 0 to 255)
        """
        dimension = image.size
        list_of_x = []
        list_of_y = []

        for x in range(0, dimension[0]):
            for y in range(0, dimension[1]):
                if  pixel_data[x,y] == color:
                    list_of_x.append(x)
                    list_of_y.append(y)

        left_x = min(list_of_x)
        right_x = max(list_of_x)
        up_y = min(list_of_y)
        low_y = max(list_of_y)
        return image.crop((left_x, up_y, right_x, low_y))

    @staticmethod
    def crop_bounded_image_inverse(image, pixel_data, color):
        """
        :param image: an image to be cropped
        :param pixel_data: the pixel data of the image, obtained by calling image.load()
        :param color: the color to serve as the criterion of cropping
        :type image: png, jpg, or other image files
        :type pixel_data: PIL.PyAccess
        :type color: (R, G, B, A) (:type R, G, B, and A: int from 0 to 255)
        """
        dimension = image.size
        list_of_x = []
        list_of_y = []

        for x in range(0, dimension[0]):
            for y in range(0, dimension[1]):
                if  pixel_data[x,y] != color:
                    list_of_x.append(x)
                    list_of_y.append(y)

        left_x = min(list_of_x)
        right_x = max(list_of_x)
        up_y = min(list_of_y)
        low_y = max(list_of_y)
        return image.crop((left_x, up_y, right_x, low_y))
