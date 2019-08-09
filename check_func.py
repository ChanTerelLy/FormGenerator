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
        if re.search(r'с.*й о.*т', type_answer) or re.search(r'простой текст', type_answer):
            type_answer = 0
        elif re.search(r'з.*[ея] из.*с.*а', type_answer):
            type_answer = 2
    else:
        type_answer = 0
    return type_answer


def check_multi_choise(multi_choise):
    if multi_choise:
        multi_choise.lower()
        if re.search(r'да', multi_choise) or re.search(r'/+', multi_choise):
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
        answers = answers.encode('utf-8')
        answers = str(answers).replace('_x000D_', '')
        answers = answers.split('\n')
        if len(answers) > 1:
            return answers
        else:
            if isinstance(answers[0], str):
                answers = re.split(r'\s{2,}', answers[0])
                if len(answers) > 1:
                    return answers
                else:
                    answers = re.split(r',', answers[0])
    elif answers == None:
            answers = ['']
    return answers


def check_type_element_data(type_element_data):
    type_element_data = str(type_element_data)
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