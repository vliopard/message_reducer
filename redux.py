import os
import sys
import json
import argparse
import configparser


input_text = None
output_text = None
json_file = None


def load_ini():
    global input_text, output_text, json_file
    
    file_name = 'settings.ini'
    
    if os.path.isfile(file_name):
        config = configparser.ConfigParser()
        config.read(file_name)
        input_text = config.get('Parameters', 'input_text')
        output_text = config.get('Parameters', 'output_text')
        json_file = config.get('Parameters', 'json_file')
    else:
        print('Default file [settings.ini] does not exist.')

def load_arg():
    global input_text, output_text, json_file
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_f', help='Input text')
    parser.add_argument('-o', '--output_f', help='Output text')
    parser.add_argument('-d', '--dict_f', help='Language ictionary')
    args = parser.parse_args()

    if args.input_f:
        input_text = args.input_f

    if args.output_f:
        output_text = args.output_f

    if args.dict_f:
        json_file = args.dict_f

def usage():
    print("Usage: python redux.py input_text output_text json_file")
    sys.exit(1)


def replace_words(input_dict, input_string):
    for key, value in input_dict.items():
        input_string = input_string.replace(key, value)
    return input_string


if __name__ == "__main__":

    load_ini()
    load_arg()
    
    if not (input_text and output_text and json_file):
        usage()

    if not os.path.isfile(json_file):
        print(f'File [{json_file}] does not exist.')
        sys.exit(1)
        
    with open(json_file, 'r', encoding='utf-8') as lang:
        replaced = json.load(lang)

    with open(input_text, 'r', encoding='utf-8') as redux:
        lines = redux.readlines()

        reduxed = []
        for line in lines:
            newline = replace_words(replaced, line)
            reduxed.append(newline)

    with open(output_text, 'w', encoding='utf-8') as reduxing:
        for line in reduxed:
            reduxing.write(line)
