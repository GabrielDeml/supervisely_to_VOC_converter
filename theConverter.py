import xml.etree.cElementTree as ET
import os
import json


def file_locations(folder):
    i = 0
    list_of_files = []
    for filename in os.listdir(folder):
        list_of_files.append(folder + filename)
        print(folder + filename)
        i = i + 1
    return list_of_files
    # with open(os.path.join(os.cwd(), filename), 'r') as f:


def print_json_data(file):
    with open(file) as f:
        data = json.load(f)
        if data['objects'] is not None:
            print(range(len(data['objects'])))
            for i in range(len(data['objects'])):
                print('point {} :'.format(i))
                print(data['objects'][i]['points']['exterior'])
        else:
            print('There was nothing in objects in: ' + file)


def write_test_xml(xmin, ymin, xmax, ymax, filename):
    annotation = ET.Element("annotation")
    object = ET.SubElement(annotation, "object")
    ET.SubElement(object, "name").text = filename
    bndbox = ET.SubElement(object, "bndbox")
    ET.SubElement(bndbox, "xmin").text = str(xmin)
    ET.SubElement(bndbox, "ymin").text = str(ymin)
    ET.SubElement(bndbox, "xmax").text = str(xmax)
    ET.SubElement(bndbox, "ymax").text = str(ymax)

    tree = ET.ElementTree(annotation)
    tree.write("filename.xml")


if __name__ == "__main__":
    write_test_xml(1, 2, 3, 4, "filename")
    # list_of_files = file_locations('Filming Day 2 Video/ann/')
    # print(list_of_files)
    # print_json_data('Filming Day 2 Video/ann/frame_00000.png.json')
