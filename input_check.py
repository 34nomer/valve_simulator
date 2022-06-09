from os import system


def choice_function_from_dict(dictionary, prefix=""):
    """Select and run a command from the dictionary"""
    user_input = ""
    while user_input.lower() != "q":
        system('cls')
        print(prefix)
        print("q - для выхода ")
        for element in dictionary:
            print(f"{element} — {dictionary[element].__doc__}")
        user_input = input()
        for element in dictionary:
            if user_input.lower() == element:
                dictionary[element]()
        if user_input.lower() == "q":
            return "q"
        else:
            print("Неизвестная команда")


def choice_object_from_list(list, prefix=""):  #TODO называется плохо, переделать
    """Choice and return from list"""
    user_input_str = ""
    list_len = len(list)
    while user_input_str.lower() != "q":
        system('cls')
        for i in range(list_len):
            print(f"{i}: <{list[i]}>")
        print(prefix)
        print("q - для выхода")
        user_input_str = input("введите номер нужного объекта")
        if user_input_str.lower() == "q":
            continue
        if user_input_str.isdigit():
            user_input_int = int(user_input_str)
            if 0 <= user_input_int < list_len:
                return user_input_int
        else:
            continue
    return None
