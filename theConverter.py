import xml.etree.cElementTree as ET
import os
import json


def file_locations(folder):
    i = 0
    list_of_files = []
    for filename in os.listdir(folder):
        list_of_files.append(filename)
        # print(folder + filename)
        i = i + 1
    return list_of_files
    # with open(os.path.join(os.cwd(), filename), 'r') as f:


def print_json_data(file):
    with open(file) as f:
        data = json.load(f)
        # if data['objects'] is not None:
        #     print(range(len(data['objects'])))
        #     for i in range(len(data['objects'])):
        #         print('point {} :'.format(i))
        #         print(data['objects'][i]['points']['exterior'])
        # else:
        #     print('There was nothing in objects in: ' + file)


def write_xml(cords, width, height, depth, filename, folder):
    annotation = ET.Element("annotation")

    # folder
    ET.SubElement(annotation, "folder").text = str(folder)
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
    tree = ET.ElementTree(annotation)
    tree.write(folder + filename + ".xml")


def convert_to_xml(folder_in, file_in, folder_out):
    with open(folder_in + file_in) as f:
        data = json.load(f)
        # find the cords
        if data['objects'] is not None:
            cords = []
            print(range(len(data['objects'])))
            for i in range(len(data['objects'])):
                point = []
                point.append(data['objects'][i]["classTitle"])
                j = 0
                while j < 2:
                    k = 0
                    while k < 2:
                        point.append(data['objects'][i]['points']['exterior'][j][k])
                        k = k + 1
                    j = j +    1
                cords.append(point)
            print(cords)
        else:
            print('There was nothing in objects in: ' + file_in)
        width = data['size']['width']
        height = data['size']['height']
        print(str(width) + " " + str(height))
        write_xml(cords, width, height, 3, file_in, folder_out)
        # write_xml(cords,)


if __name__ == "__main__":
    # write_xml([["name", 1, 2, 3, 4], ["name2", 5, 6, 7, 8]], 1080, 1920, 3, "filename", "folder")
    list_of_files = file_locations('Filming Day 2 Video/ann/')
    # print(list_of_files)
    # print_json_data('Filming Day 2 Video/ann/frame_00000.png.json')
    for file in list_of_files:
        print(file)
        convert_to_xml('Filming Day 2 Video/ann/', file, "test/")
