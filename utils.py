import csv
import datetime
import os


def write_text_file(content, path="replies_traces/", filename=None, date=True, different=True):
    if date:
        filename = generate_numbers() + (" " + filename if filename else "")

    if not os.path.exists(path):
        os.makedirs(path) #recursively build a directory

    counter = 0
    tempfilename = path + filename + " " + str(counter) + ".txt"
    while os.path.isfile(tempfilename) and different:
        counter += 1
        tempfilename = path + filename + " " + str(counter) + ".txt"
    filename = tempfilename

    try:
        with open(filename, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"An error occurred while writing the file: {str(e)}")


def generate_numbers():
    now = datetime.datetime.now()
    number_string = now.strftime('%y%m%d%H%M%S')
    return number_string


def load_csv_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data


def get_files_in_folder(folder_path):
    try:
        files = [folder_path+"/"+f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return files
    except Exception as e:
        print(f"An error occurred while getting files in the folder: {str(e)}")
        return []


def read_file(filename):
    with open(filename, 'r') as file:
        contents = file.read()
    return contents


def read_file_contents(filename):
    try:
        with open(filename, 'r') as file:
            contents = file.readlines()
            contents = [line.rstrip('\n') for line in contents]
        return contents
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return []