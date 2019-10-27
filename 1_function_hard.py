def phrase_search(object_list: list, search_string: str) -> int:
    phrase_combos = []  # 1. Пустой список, в который в будущем будут помещены комбинации.
    string_check = False  # В будуещм будет использоваться для проверки условия.

    for dic in object_list:

        dic_phrase = dic['phrase']  # 2. Получить значение ключа phrase.
        dic_id = dic['id']  # 3. Получить значение ключа id.

        # 4. Проверка, являются ли объекты внутри спика slots строкой.
        if dic['slots']:
            for string in dic['slots']:
                if isinstance(string, str):
                    string_check = True

        # 5. Проверка на наличие фигурных скобок в значении ключа phrase и строки в списке slots.
        if ('{' and '}' in dic_phrase) and string_check:
            dic_phrase_modfifed = dic_phrase.replace('{', '')
            dic_phrase_modfifed1 = dic_phrase_modfifed.replace('}', '')
            phrase_combos.append(dic_phrase_modfifed1)  # добавить в массив комбинаций вариант строки из фигурных скобок
            slots_index = 0  # создать переменную, которая в будущем используется как индекс списка.
            phrase_content = dic_phrase[:dic_phrase.find('{')]  # сохранить содержимое строки до {

            for i in dic['slots']:
                # вместо {} подставить слово из списка slots и содержимое строки до {}.
                dic_phrase = phrase_content + dic['slots'][slots_index]
                phrase_combos.append(dic_phrase)  # добавить комбинацию в список из п.1.
                slots_index += 1  # переход к следующему индексу списка.

            # анализ каждой комбинации в полученном списке
            for search in phrase_combos:
                word = (search_string.upper()).split()  # разбить искомую строку на слова
                search_1 = (search.upper()).split()  # разбить фразу из списка с комбинациями на слова
                if set(word).issubset(search_1):
                    return dic_id
        else:
            if search_string.upper() == dic_phrase.upper():
                return dic_id

    # если искомой строки нет ни в массиве с комбинациями и если она не равна другим фразам в списке
    for cut in object_list:
        if (search_string not in phrase_combos) and (search_string != cut['phrase']):
            return 0


if __name__ == "__main__":
    object_list = [
        {"id": 1, "phrase": "Hello world!", "slots": []},
        {"id": 2, "phrase": "I wanna {coke} and {pasta}", "slots": ["pizza", "BBQ", "sushi"]},
        {"id": 3, "phrase": "Give me your power", "slots": ["money", "gun"]},
    ]

    assert phrase_search(object_list, 'i wanna pasta') == 2
    assert phrase_search(object_list, 'give me your power') == 3
    assert phrase_search(object_list, 'Hello world!') == 1
    assert phrase_search(object_list, 'I wanna nothing') == 0
    assert phrase_search(object_list, 'Hello again world!') == 0
    assert phrase_search(object_list, 'I need your clothes, your boots & your motorcycle') == 0
