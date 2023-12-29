import json
import subprocess
import os


from . import constants


def find_indentation(lines):
    min_leading_spaces = None
    for line in lines.split("\n"):
        if line.strip() == "":
            continue
        num_leading_spaces = len(line) - len(line.lstrip(" "))
        if min_leading_spaces == None:
            min_leading_spaces = num_leading_spaces
        elif num_leading_spaces < min_leading_spaces:
            min_leading_spaces = num_leading_spaces
    return min_leading_spaces


def write_lines(target_path, lines, args={}):
    indent = find_indentation(lines)
    with open(target_path, "w") as f:
        for line in lines.split("\n"):
            if args:
                f.write(line[indent:].format(**args) + "\n")
            else:
                f.write(line[indent:] + "\n")


def write_json(target_path, data):
    with open(target_path, "w+") as f:
        f.write(json.dumps(data, sort_keys=True, indent=4))


def load_json(file_path):
    data = None
    with open(file_path) as f:
        data = json.loads(f.read())
    return data


def load_config():
    return load_json(constants.SOROBAN_DEV_FILE_NAME)


def save_config(data):
    write_json(constants.SOROBAN_DEV_FILE_NAME, data)


def call(cmd):
    process = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, error = process.communicate()
    if output:
        output = output.decode()
    if error:
        error = error.decode()
    return output, error


def is_in_sorodev_project():
    return constants.SOROBAN_DEV_FILE_NAME in os.listdir()


def check_in_sorodev_project():
    if not is_in_sorodev_project():
        exit_error("Not in a sorodev project")


def log_action(msg):
    print(f"###### {msg}")


def exit_error(error_msg):
    print("========== Failed ==========")
    print(error_msg)
    exit()
