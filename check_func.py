import re


def check_element(element, answers):
    if element:
        element = element.lower()
        if re.search(r'з.*к', element) and answers == None:

            element = 0
        elif re.search(r'в.*с', element):
            element = 1
        else:
            element = 1
    else:
        element = 1
    return element


def check_type_answer(type_answer):
    if type_answer:
        type_answer = type_answer.lower()
        # check if will need by the way
        # if re.search(r'с.*й о.*т', type_answer) or re.search(r'простой текст', type_answer):
        #     type_answer = 0
        if re.search(r'з.*[ея] из.*с.*а', type_answer):
            type_answer = 2
        else:
            type_answer = 0
    else:
        type_answer = 0
    return type_answer


def check_multi_choise(multi_choise):
    if multi_choise:
        multi_choise = multi_choise.lower()
        if re.search(r'да', multi_choise) or re.search(r'\+', multi_choise):
            multi_choise = 1
        elif re.search(r'н.т', multi_choise) or re.search(r'-', multi_choise):
            multi_choise = 0
        else:
            multi_choise = 0
    else:
        multi_choise = 0
    return multi_choise


def check_answers(answers):
    if answers:
        answers = remove_null_answers(is_tab(is_enter(check_x000D_chars(char_decoder(answers)))))
        if len(answers) > 1:
            return answers
        else:
            if isinstance(answers[0], str):
                    return remove_null_answers(re.split(r',', answers[0]))
    else:
            return ['']


def check_x000D_chars(answers):
    return str(answers).replace('_x000D_', '')


def remove_null_answers(answers):
    return list(filter(lambda x: x if x != '' else False, answers))


def is_enter(answers):
    new_answer = []
    new_answer.extend(answers.split('\n')) if isinstance(answers, str) else [new_answer.extend(answer.split('\n')) for
                                                                             answer in answers]
    return new_answer


def is_tab(answers):
    new_answer = []
    new_answer.extend(answers.split(r'\s{3,}')) if isinstance(answers, str) else [new_answer.extend(re.split(r'\s{3,}', answer)) for
                                                                             answer in answers]
    return new_answer


def check_type_element_data(type_element_data):
    if re.search('дата', type_element_data.lower()):
        type_element_data = 1
    elif re.search('время', type_element_data.lower()):
        type_element_data = 2
    elif re.search('дата и время', type_element_data.lower()):
        type_element_data = 3
    elif re.search('логический', type_element_data.lower()):
        type_element_data = 4
    else:
        type_element_data = 0
    return type_element_data

def check_choise_is_not_null(protocol_row):
    if isinstance(protocol_row, list):
        protocol_row[2] = 0 if protocol_row[2] == 2 and protocol_row[4] == [''] else protocol_row[2]
    return protocol_row

def is_conclusion(protocol_row):
    if isinstance(protocol_row, list):
        protocol_row[0] = 1 if protocol_row[0] == 0 and (re.search('анамнез', protocol_row[1].lower())
                                 or re.search('заключение', protocol_row[1].lower()) or
                                 re.search('жалоб', protocol_row[1].lower())) else protocol_row[0]
    return protocol_row

def char_decoder(string):
    if string:
        string = string.replace('α', 'a')
        string = string.replace('β', 'b')
        string = string.replace('³', '3')
        return string
    else:
        return string