from PIL import Image
import pytesseract
import shutil
import os
import re

def read_dump(path, unreadables_path):

    results = {'disks': []}
    serial_number_pattern = r'(S\/N)\s*([A-Za-z0-9]+)'
    part_number_pattern = r'(P\/N)\s*([A-Za-z0-9]+)'

    # Create the unreadables directory
    try:
        os.mkdir(unreadables_path)
        print(f"Directory '{unreadables_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{unreadables_path}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{unreadables_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Empty the directory
    for file in os.listdir(unreadables_path):
        os.remove(unreadables_path + file)
    matches = 0
    skipped = 0
    # Iterate over every file
    for file in os.listdir(path):
        if file.endswith(".jpg") or file.endswith(".jpeg"):
            print("Reading " + str(file))
            # Prints only text file present in My Folder
            image = Image.open(path + file)
            results_per_algo = {'results': []}

            # Specify Neural net mode and Default mode
            modes = [1,3]
            # Try the 3 different available algorithms to maximize success
            for i in range (0, len(modes)):
                text = pytesseract.image_to_string(image, config='--oem ' + str(modes[i]))
                # Serial is found
                if "S/N" in text:
                    # Find all matches of the pattern in the extracted text
                    serial_number = re.findall(serial_number_pattern, text)
                    part_number = re.findall(part_number_pattern, text)

                    disk = {}
                    disk['image'] = file
                    disk['SN'] = serial_number[0]
                    # Nice to have but not mandatory
                    if len(part_number) > 0:
                        disk['PN'] = part_number[0]
                    # More than one match
                    if len(serial_number) > 1 or len(part_number) > 1:
                        disk['multiple_matches'] = [serial_number, part_number]

                    results_per_algo['results'].append(disk)
            # At least one result was found
            if len(results_per_algo['results']) > 0:
                matches += 1
                results['disks'].append(results_per_algo)
            # Serial is not found
            else:
                skipped += 1
                shutil.copy(path + file, unreadables_path + file)

    print(str(len(os.listdir(path))) + ' Files read')
    print(str(matches) + ' Serials found, ' + str(skipped) + ' files skipped')
    return results