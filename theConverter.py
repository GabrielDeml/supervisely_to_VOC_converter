import xml.etree.cElementTree as ET
import os
import json
import argparse
import glob
import sys
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, default='.', help="Location of Jsons to read")
parser.add_argument("-s", "--supervisely", type=str, help="Location of Supervisely folder")
parser.add_argument("-o", "--output", type=str, default='.', help="Location of XMLs to  write")
parser.add_argument('-p', "--pretend", default=False, action='store_true', help="Pretend to be VOC2012")
parser.add_argument("-r", "--overwrite", default=False, action='store_true',
                    help="Overwrite the output dir if it exists")
args = parser.parse_args()


##
# Create fake VOC2012 file structure
def create_voc(location):
    # Check if we can overwrite the folder
    if os.path.exists(os.path.join(location, "voc2012_raw")):
        if args.overwrite:
            shutil.rmtree(os.path.join(location, "voc2012_raw"), ignore_errors=True)
        else:
            sys.exit("Folder already exists: {}".format(os.path.join(location, "voc2012_raw")))
    # Create the folders
    os.makedirs(os.path.join(location, "voc2012_raw/VOCdevkit/VOC2012/Annotations"))
    os.makedirs(os.path.join(location, "voc2012_raw/VOCdevkit/VOC2012/JPEGImages"))


##
# Writes an XML given prams
def write_xml(cords, width, height, depth, filename, folder):
    # Make the names right
    if folder[-1] != '/':
        folder_out_name = folder
        folder = folder + '/'
    else:
        folder_out_name = folder[:-1]
    filename = filename[:-5]

    annotation = ET.Element("annotation")

    # folder
    if args.pretend:
        ET.SubElement(annotation, "folder").text = "VOC2012"
    else:
        ET.SubElement(annotation, "folder").text = str(folder_out_name)

    # filename
    ET.SubElement(annotation, "filename").text = str(filename)

    # size block
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(depth)

    # object block
    for point in cords:
        object = ET.SubElement(annotation, "object")
        ET.SubElement(object, "name").text = point[0]
        bndbox = ET.SubElement(object, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(point[1])
        ET.SubElement(bndbox, "ymin").text = str(point[2])
        ET.SubElement(bndbox, "xmax").text = str(point[3])
        ET.SubElement(bndbox, "ymax").text = str(point[4])

    # Write to a file
    print("Writing: {}{}.xml".format(folder, filename[:-4]))
    tree = ET.ElementTree(annotation)
    tree.write(folder + filename[:-4] + ".xml")


# Convert Json to XML
def convert_to_xml(folder_in, file_in, folder_out):
    with open(folder_in + file_in) as f:
        data = json.load(f)
        # find the cords
        if data['objects'] is not None:
            # List of points
            cords = []
            # Go over every object
            for i in range(len(data['objects'])):
                # Example point: ["name", x, y, x1, y1]
                point = [data['objects'][i]["classTitle"]]
                j = 0
                # Make a point
                while j < 2:
                    k = 0
                    while k < 2:
                        point.append(data['objects'][i]['points']['exterior'][j][k])
                        k = k + 1
                    j = j + 1
                cords.append(point)
        else:
            print('There was nothing in objects for: ' + file_in)

        # Get width and height
        width = data['size']['width']
        height = data['size']['height']

        # Write it to XML
        write_xml(cords, width, height, 3, file_in, folder_out)


def convert_files(input, output):
    # Check to see if we can overwrite the file
    if os.path.exists(output):
        if args.overwrite:
            shutil.rmtree(output, ignore_errors=True)
        else:
            sys.exit("Folder already exists: {}".format(output))
    os.makedirs(output)
    # Convert all of the jsons
    for file in os.listdir(input):
        convert_to_xml(input, file, output)


def get_location_of_jsons():
    if args.supervisely is not None:
        return glob.glob(args.supervisely + "/**/ann/")[0]
    else:
        return args.input


def copy_files_from_supervisely(super, dest):
    src = glob.glob(super + "/**/img/")[0]
    for file in os.listdir(src):
        shutil.copyfile(os.path.join(src, file), os.path.join(dest, file))


if __name__ == "__main__":
    if args.pretend:
        create_voc(args.output)
        convert_files(get_location_of_jsons(), os.path.join(args.output, "voc2012_raw/VOCdevkit/VOC2012/Annotations/"))
        copy_files_from_supervisely(args.supervisely,
                                    os.path.join(args.output, "voc2012_raw/VOCdevkit/VOC2012/JPEGImages/"))
    else:
        convert_files(get_location_of_jsons(), args.output)
