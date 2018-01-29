from PIL import Image
from PIL import ImageFilter
from collections import Counter
from .color_operations import ColorOperations
from .target_analyzer import TargetAnalyzer
from .background_color_nullifier import BackgroundColorNullifier
from .connected_component_labeler import ConnectedComponentLabeler

class SingleTargetsCapturer(object):

    @staticmethod
    def capture_single_targets(target_map_image_path, positive_list):
        """
        Crop the single targets with information given by target_location.

        :param target_map_image_path: the path to the target map image
        :param positive_list: the list holding information of the locations of
                              targets, which are four-tuples of the target's top
                              left x, top left y, width, and height

        :type target_map_image_path: an image file such as JPG and PNG
        :type positive_list: list
        :type target_location: (x, y, width, height)
        :type x: int
        :type y: int
        :type length: int
        :type width: int

        Concept:
        Stage 1
        Find the average color of the target_map.

        Stage 2
        For every detected target on the target map:
        1. Crop it out with 30-pixel margins on each side.
        2. Find the average_corner_color of the image.
        3. Find the rim_average_color of the image.

        if the average_corner_color is not within 15 percent difference from the
        rim_average_color, the target is determined as a false positive and is
        added to list_to_eliminate.
        Otherwise, proceed to to Stage 3.

        Stage 3
        Apply BackgroundColorNullifier.nullify_color_and_recrop_target to the
        image. For more detail see .background_color_nullifier.
        """
        target_map_image = Image.open(target_map_image_path)
        target_map_image_average_color = TargetAnalyzer.find_target_average_color(target_map_image, (0, 0, target_map_image.width, target_map_image.height))

        resultant_image_list = []
        list_to_eliminate = []
        for index in range(len(positive_list)):

            target_location = positive_list[index]

            target_x = target_location[0]
            target_y = target_location[1]
            target_width = target_location[2]
            target_height = target_location[3]

            crop_x1 = target_x - 30
            crop_y1 = target_y - 30
            crop_x2 = target_x + target_width + 30
            crop_y2 = target_y + target_height + 30

            if (crop_x1 < 0):
                crop_x1 = 0

            if (crop_x2 >= target_map_image.width):
                crop_x2 = target_map_image.width - 1

            if (crop_y1 < 0):
                crop_y1 = 0

            if (crop_y2 >= target_map_image.height):
                crop_y2 = target_map_image.height - 1

            captured_image = target_map_image.crop((crop_x1, crop_y1, crop_x2, crop_y2))

            captured_image_average_corner_color = TargetAnalyzer.find_average_corner_color(captured_image)
            captured_image_rim_average_color = TargetAnalyzer.find_rim_average_color(captured_image)
            percentage_difference = ColorOperations.find_percentage_difference(captured_image_average_corner_color, captured_image_rim_average_color)

            if (percentage_difference > 15):
                list_to_eliminate.append(index)
                continue

            else:
                color_nullifying_result = BackgroundColorNullifier.nullify_color_and_recrop_target(captured_image, 15)
                if (color_nullifying_result == 0):
                    list_to_eliminate.append(index)
                else:
                    resultant_image = color_nullifying_result
                    resultant_image_list.append(resultant_image)

        return [resultant_image_list, list_to_eliminate]


        #The code commented out are applications of color quantization and
        #connected components labeling, which are currently not in use.
        '''
            labeled_image = captured_image.crop(ConnectedComponentLabeler.label_connected_components(captured_image))
            labeled_image.show()

            quantized_image = ColorOperations.apply_color_quantization(captured_image, 4)
            quantized_image_average_color = TargetAnalyzer.find_target_average_color(quantized_image, (0, 0, quantized_image.width, quantized_image.height))
            quantized_image_average_corner_color = TargetAnalyzer.find_average_corner_color(quantized_image)

            percentage_difference_1 = ColorOperations.find_percentage_difference(quantized_image_average_color, quantized_image_average_corner_color)
            percentage_difference_2 = ColorOperations.find_percentage_difference(target_map_image_average_color, quantized_image_average_corner_color)

            if (percentage_difference_1 < 5):
                list_to_eliminate.append(index)
                continue

            #if the following four lines are uncommented, more targets and false positives would be captured.
            if (percentage_difference_2 >= 10):
                list_to_eliminate.append(index)
                continue

            color_nullifying_result = ColorOperations.nullify_color_and_crop_to_target(captured_image, 15)
            if (color_nullifying_result == 0):
                list_to_eliminate.append(index)
            else:
                resultant_image = color_nullifying_result
                resultant_image_list.append(resultant_image)

        return [resultant_image_list, list_to_eliminate]
        '''