#!/usr/bin/python
# Code generated for pattern detection
# Author: Nahid Akhtar
# Email: nahid.saarland@gmail.com
########################################################################################################################
#  Libraries
########################################################################################################################
import collections
import re
import os
########################################################################################################################
# Meta characters of Regular Expressions
meta_characters = ['.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '\\', '|', '(', ')']
########################################################################################################################
# Function Description for character_type(char)
'''       Function to Recognize char and return type 
            d if digital (0-9)
            k if small letter (a-z)
            c if capital letter (A-Z)
            m if meta character
            s if special character
            a if letter but not in range (a-z) or (A-Z)      
'''


def character_type(char):
    if char.isdigit():
        type_char = 'd'    # digit
    elif char.isalpha():
        try:
            if char.encode('ascii').isalpha():    # alphabet in range (A-Za-z)
                if char.isupper():
                    type_char = 'c'  # capital alphabet
                else:
                    type_char = 'k'  # small alphabet
        except UnicodeEncodeError:
            type_char = 'a'    # alphabet but not in range (A-Za-z)
    else:
        if char in meta_characters:
            type_char = 'm'   # meta character
        else:
            type_char = 's'   # special character
    return type_char
########################################################################################################################
# Function Description for regular_expression(char_num,char_type)
# It takes character type and number of characters to make a regular expression


def regular_expression(char_num,char_type):
    if char_type == 'd':
        reg_exp = '\\d{' + char_num + '}'
    elif char_type == 'c':
        reg_exp = '[A-Z]{' + char_num + '}'
    elif char_type == 's':
        reg_exp = '[a-z]{' + char_num + '}'
    return reg_exp
########################################################################################################################
# Function Description for create_type_list(input_list)
# It takes input list and return type list containing types of characters
# For instance it takes input 'AB123' and return 'ccddd'


def create_type_list(input_list):
    type_list= []
    for i in input_list:
        type_entry = ''
        for j in i:
            type = character_type(j)
            type_entry = type_entry + type
        type_list.append(type_entry)
    return type_list
########################################################################################################################
# Function Description for create_indexes(input_list, type_list):
# It takes input_list and type_list and return pattern, similar_index, non_similar_index, similar_items


def create_indexes(input_list, type_list):
    similar_index = []
    non_similar_index = []
    similar_items = []
    dictionary_elements = {}
    for items in type_list:
        dictionary_elements[items] = type_list.count(items)
    # Find Key with Max Value
    max_value = max(dictionary_elements.items(), key=lambda x: x[1])
    pattern = max_value[0]
    for i, k in enumerate(type_list):
        if k == max_value[0]:
            similar_index.append(i)
        else:
            non_similar_index.append(i)
    for i in non_similar_index:
        if pattern in type_list[i] or type_list[i] in pattern:
            similar_index.append(i)
            non_similar_index.remove(i)
    for i in similar_index:
        pattern_last_letter = pattern[-1]
        index = type_list[i].find(pattern)
        if index == 0:
            difference = len(type_list[i]) - len(pattern)
            for k in range(difference):
                if pattern_last_letter != type_list[i][len(type_list[i])-k- 1]:
                    similar_index.remove(i)
                    non_similar_index.append(i)
        else:
            non_similar_index.append(i)
    for i in similar_index:
        similar_items.append(input_list[i])
    return pattern, similar_index, non_similar_index, similar_items
########################################################################################################################
# Function Description for create_common_letters(similar_items)
# It takes similar_items and  return common_letters_format


def create_common_letters(similar_items):
    min_length = min(len(x) for x in similar_items)
    common_letters_format = []
    for i in range(min_length):
        check_count = 0
        for k, v in enumerate(similar_items[1:]):
            if v[i] == similar_items[0][i]:
                check_count = check_count + 1
        if check_count == (len(similar_items)-1):
            common_letters_format.append('*')
        else:
            common_letters_format.append('-')
    return common_letters_format
########################################################################################################################
# Function Description for create_final_pattern(similar_items,common_letters_pattern)
# It takes similar_items,common_letters_pattern and return final_pattern like [*,2,d,2,s5]


def create_final_pattern(similar_items,common_letters_pattern):
    smallest_pattern = min(similar_items, key=len)
    smallest_pattern_array = []
    common_letters_index = []
    common_letters = []
    for i, k in enumerate(common_letters_pattern):
        if k == '*':
            common_letters_index.append(i)
            common_letters.append(smallest_pattern[i])
    for i, k in enumerate(smallest_pattern):
        if i in common_letters_index:
            t = '*'
        else:
            t = character_type(k)
        smallest_pattern_array.append(t)
    count = 1
    final_pattern_array = []
    if len(smallest_pattern_array) > 1:
        for i in range(1, len(smallest_pattern_array)):
            if smallest_pattern_array[i - 1] == smallest_pattern_array[i]:
                count += 1
            else:
                final_pattern_array.append(smallest_pattern_array[i - 1])
                final_pattern_array.append(str(count))
                count = 1
        final_pattern_array.append(smallest_pattern_array[i])
        final_pattern_array.append(str(count))
    else:
        i = 0
        final_pattern_array.append(smallest_pattern_array[i])
        final_pattern_array.append(str(count))
    return final_pattern_array, common_letters
########################################################################################################################
# Function Description for create_final_regular_expression(similar_items, final_pattern_array, common_letters)
# It takes similar_items, final_pattern_array, common_letters and return final regular expression detected


def create_final_regular_expression(similar_items, final_pattern_array, common_letters):
    max_length = max(len(x) for x in similar_items)
    min_length = min(len(x) for x in similar_items)
    reg_exp = '^'
    count = 0
    for i, k in enumerate(final_pattern_array[:-1]):
        if final_pattern_array[i] != "*" and (final_pattern_array[i + 1].isdigit() == True):
            reg_exp = reg_exp + regular_expression(final_pattern_array[i + 1], final_pattern_array[i])
        elif final_pattern_array[i] == "*" and (final_pattern_array[i + 1].isdigit() == True):
            value = int(final_pattern_array[i + 1])
            for i in range(count, count + value):
                reg_exp = reg_exp + common_letters[i]
            count = count + value
    pattern_diff_length = max_length - min_length
    if pattern_diff_length > 0:
        reg_exp = reg_exp[:-1]
        last_number = int(reg_exp[-1])
        last_pattern_num = last_number + pattern_diff_length
        reg_exp = reg_exp + ',' + str(last_pattern_num) + '}$'
    else:
        reg_exp = reg_exp + '$'
    return reg_exp
########################################################################################################################
# Main Function


def main(input_list):
    type_list = create_type_list(input_list)
    pattern, similar_index, non_similar_index, similar_items = create_indexes(input_list, type_list)
    common_letters_pattern = create_common_letters(similar_items)
    final_pattern_array, common_letters = create_final_pattern(similar_items, common_letters_pattern)
    reg_exp = create_final_regular_expression(similar_items, final_pattern_array, common_letters)
    print(similar_items)
    print('Input Elements:')
    print('==========================')
    print(*input_list, sep=", ")
    print('\nDetected Pattern:')
    print('==========================')
    print(reg_exp)
    print('\nItems from which pattern is detected:')
    print('==========================')
    print(*similar_items, sep = ", ")
    for i, k in enumerate(similar_items):
        r = re.findall(reg_exp, k)
        #print(i, r)
########################################################################################################################
# Call for Main Function


if __name__ == "__main__":
    path = 'Input\\'
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.txt' in file:
                file_name = os.path.join(r, file)
                print('\n####################################################################################')
                print('\n   RESULTS OF ' + file)
                print('\n####################################################################################')
                with open(file_name) as f:
                    sample_list = f.read().splitlines()
                    main(sample_list)