from PIL import Image
import datetime
import commands
import os

ALLOWED_IMAGE_DIFFERENCE_PERCENT = 3.0
DEFAULT_IMAGE_DIFFERENCE_FILE = os.path.dirname(os.path.realpath(__file__)) + "/difference_file.png"


def compare_images_to_file(file1, file2, difference_file):
    """Compares images in file1 and file2.

    Difference is saved in difference_file.

    :Args:
        - file1 (str): Full path to file 1
        - file2 (str): Full path to file 2
        - difference_file (str): Full path to file where difference will be saved.

    :Usage:
        compare_images_to_file('/Users/Andrii/development/Image1.png', '/Users/Andrii/development/Image1.png')
    """
    command2 = "compare " + file1 + " -metric AE " + file2 + " -compose src " + difference_file
    res = commands.getoutput(command2)


def compare_by_pixels(file_path_1, file_path_2, allowed_difference=ALLOWED_IMAGE_DIFFERENCE_PERCENT,
                      diff_file=DEFAULT_IMAGE_DIFFERENCE_FILE):
    """Compares images in file1 and file2 pixel by pixel.

    Creates differences file. Checks if the difference is not bigger than allowed.

    :Args:
        - file_path_1 (str): Full path to file 1
        - file_path_2 (str): Full path to file 2
        - allowed_difference (float): Allowed difference percentage. Default 3.0
        - diff_file (str): Full path to file where difference will be saved. Default '<script_path>/difference_file.png'.

    :Returns:
        True if images are equal in allowed range, false otherwise.

    :Usage:
        With all arguments:
            python ImageComparison.py /Users/Andrii/development/ImageComparisonTool/images/chapter_5_clean.png
            /Users/Andrii/development/ImageComparisonTool/images/chapter_5_clean.png
            3.0
            /Users/Andrii/development/ImageComparisonTool/defference_file_1.png
        With default value for differences file:
            python ImageComparison.py /Users/Andrii/development/ImageComparisonTool/images/chapter_5_clean.png
            /Users/Andrii/development/ImageComparisonTool/images/chapter_5_clean.png
            3
        With default values for differences file and allowed difference range:
            python ImageComparison.py /Users/Andrii/development/ImageComparisonTool/images/chapter_5_clean.png
            /Users/Andrii/development/ImageComparisonTool/images/chapter_5_clean.png

    :Examples:
        python ImageComparison.py /Users/Andrii/development/ImageComparisonTool/images/chapter_5_clean.png
        /Users/Andrii/development/ImageComparisonTool/images/chapter_5_clean.png
        3.0
        /Users/Andrii/development/ImageComparisonTool/defference_file_1.png
        Output:
            Comparing images.
            File1 = /Users/Andrii/development/ImageComparisonTool/images/chapter_5_clean.png
            File2 = /Users/Andrii/development/ImageComparisonTool/images/chapter_5_clean.png
            Allowed image difference = 3.0
            Number of unequal pixels = 01 of total 23040002
            Percentage of unequal pixels = 0.0
            Time taken to compare images= 0:00:01.340925
            Comparison passed! Images are equal!
    """

    print "Comparing images\nFile1 = %s\nFile2 = %s\nAllowed image difference = %s" % (file_path_1, file_path_2,
                                                                                          allowed_difference)

    # save the time when search for element started
    time = datetime.datetime.now()

    # create difference file; not used to calculate percentage, for visualisation needs only
    compare_images_to_file(file1=file_path_1, file2=file_path_2, difference_file=diff_file)

    file1 = Image.open(file_path_1)
    file2 = Image.open(file_path_2)

    w1 = file1.size[0]
    h1 = file1.size[1]

    w2 = file2.size[0]
    h2 = file2.size[1]

    if w1 != w2 or h1 != h2:
        print "Images have different dimensions!"
        return False

    width = w1
    height = h1

    im1 = file1.load()
    im2 = file2.load()

    failed_pixels = 0

    i = 0
    while i < height:
        j = 0
        while j < width:
            if im1[j, i] != im2[j, i]:
                failed_pixels += 1
            j += 1
        i += 1

    print "Number of unequal pixels = %s1 of total %s2" % (failed_pixels, (height * width))

    diff = float(failed_pixels) * 100 /(height * width)
    print "Percentage of unequal pixels = %s" % diff

    # print the time taken to find element
    print("Time taken to compare images= %s" % str(datetime.datetime.now() - time))

    if diff < allowed_difference:
        print "Comparison passed! Images are equal!"
        return True
    else:
        print "Comparison failed! Images differ!"
        return False

if __name__ == "__main__":
    import sys
    args_count = len(sys.argv)
    if args_count == 5:
        compare_by_pixels(file_path_1=str(sys.argv[1]), file_path_2=str(sys.argv[2]),
                          allowed_difference=float(sys.argv[3]), diff_file=str(sys.argv[4]))
    elif args_count == 4:
        compare_by_pixels(file_path_1=str(sys.argv[1]), file_path_2=str(sys.argv[2]),
                          allowed_difference=float(sys.argv[3]))
    elif args_count == 3:
        compare_by_pixels(file_path_1=str(sys.argv[1]), file_path_2=str(sys.argv[2]))
    else:
        print('Invalid arguments count!')






