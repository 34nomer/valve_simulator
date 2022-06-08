from os import system
def input_uint(comment="", min=False, max=False):
    assert min > 0 if min != False else True
    assert max > 0 if max != False else True
    assert max > min,  "Максимальное значение диапазона должно быть больше минимального  "
    while True:
        user_text = input(comment)
        if not user_text.isdigit():
            print("this is not 'int' digit")
        else:
            user_int = int(user_text)
            if min and min > user_int:
                print("below bottom range" + " min=" + str(min))
                continue
            if max and max < user_int:
                print("above upper range" + " max=" + str(max))
                continue
            break

    return user_int


def choice_function_from_dict(dictionary, prefix=""):
    """"""
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






