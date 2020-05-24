import xml.etree.cElementTree as ET
import os
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, default='.', help="Location of Jsons to read")
parser.add_argument("-o", "--output", type=str, default='.', help="Location of XMLs to  write")
args = parser.parse_args()

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


if __name__ == "__main__":
    for file in os.listdir(args.input):
        convert_to_xml(args.input, file, args.output)
