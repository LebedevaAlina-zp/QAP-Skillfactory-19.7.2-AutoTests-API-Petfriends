from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

# Copied from dimm23 repository on https://github.com/SkillfactoryCoding/QAP_PetFriensTesting
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_api_key_with_wrong_password(email=valid_email, password=valid_password+"0"):
    """ Проверяем что на запрос api ключа с неверным паролем пользователь не получает ключ"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, _ = pf.get_api_key(email, password)

    # Сверяем статус код
    assert status == 403


def test_get_api_key_with_uppercase_email(email=valid_email.upper(), password=valid_password):
    """ Проверяем пользователь получает ключ авторизации при вводе емэйла большими буквами и верном пароле. """

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_api_key_with_uppercase_password(email=valid_email, password=valid_password.upper()):
    """ Проверяем, что пользователь не получает ключ авторизации при случайном наборе верного пароля большими буквами. """

    status, _ = pf.get_api_key(email, password)

    assert status == 403


# Copied from dimm23 repository on https://github.com/SkillfactoryCoding/QAP_PetFriensTesting
def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_get_pets_list_with_filter_my_pets(filter="my_pets"):
    """ Проверяем что запрос питомцев с фильтром "my_pets" возвращает непустой список питомцев."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert len(result['pets']) > 0


def test_get_all_pets_with_wrong_key(filter=''):
    """ Проверяем, что с неверным ключом авторизации невозможно получить список питомцев"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # В полученном ключе удалим поледний символ
    auth_key['key'] = auth_key['key'][:-1]
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403


# Copied from dimm23 repository on https://github.com/SkillfactoryCoding/QAP_PetFriensTesting
def test_add_new_pet_with_valid_data(name='Carrie', animal_type='siamese cat',
                                     age='8', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными."""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_valid_data_rus(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными, введенными символами русского алфавита"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age


def test_add_new_pet_with_wrong_key(name='Carrie', animal_type='siamese cat',
                                     age='8', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с неверным ключом авторизации"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # В полученном ключе удалим поледний символ
    auth_key['key'] = auth_key['key'][:-1]

    # Пробуем добавить питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


def test_add_new_pet_with_png_image(name='Grusha', animal_type='cockatiel',
                                  age='5', pet_photo='images\Grusha.png'):
    """ Проверяем возможность добавить питомца с фото в формате png (такая возможность указана в swagger документации)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age \
           and result['pet_photo'] != ''


# Copied from dimm23 repository on https://github.com/SkillfactoryCoding/QAP_PetFriensTesting
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# Copied from dimm23 repository on https://github.com/SkillfactoryCoding/QAP_PetFriensTesting
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_delete_someone_elses_pet():
    """ Проверяем невозможность удаления чужого питомца (не из списка "my_pets") """

    # Получаем ключ auth_key и запрашиваем список всех питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, '')

    # Запоминаем id первого питомца из списка
    i = 0
    pet_id = all_pets['pets'][i]['id']

    # Получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если окажется, что в общем списке только наши питомцы, то отправляем соотсетствующее сообщение
    if len(my_pets['pets']) == len(all_pets['pets']):
        raise Exception("There are no pets of other users.")

    # Если список своих питомцев не пуст, то
    if len(my_pets['pets']) != 0:
        # Проверяем, что в списке наших питомцев нет pet_id
        for pet in my_pets['pets']:
            # А если есть, то возьмем следующего питомца из общего списка и дальше в цикле будем проверять его
            # Поскольку животные в обоих списках расположены от новых к старым, то можно продолжить сверку в том же цикле
            if pet['id'] == pet_id:
                i += 1
                pet_id = all_pets['pets'][i]['id']

    # Пытаемся удалить чужого питомца
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Проверяем, чтобы питомец, которого мы попытались удалить, все еще в списке питомцев, а статус ответа не 200
    assert pet_id in all_pets.values()
    assert status != 200


def test_add_new_pet_without_photo_with_valid_data(name="Kitty", animal_type="The Kitten", age="0"):
    """Проверяем успешное добавление питомца без фото с корректными данными."""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Проверяем статус и ожидаемый результат
    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age


def test_upload_photo_to_pets_card_jpg(pet_photo="images\P1040103.jpg"):
     """Проверяем загрузку фото jpg к питомцу без фото."""

     # Получаем ключ auth_key и список своих питомцев
     _, auth_key = pf.get_api_key(valid_email, valid_password)
     _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

     # Перебираем по очереди питомцев в существующем списке
     for i in range(0, len(my_pets["pets"])):
         # Выбираем из них питомца без фото, загружаем этому питомцу фото и выходим из цикла
         if my_pets["pets"][i]["pet_photo"] == "":
             status, result = pf.add_pets_photo(auth_key, my_pets["pets"][i]['id'], pet_photo)
             break
         # Если мы дошли до конца списка питомцев, а питомца без фото не нашлось, добавим его, а затем загрузим фото
         if i == len(my_pets["pets"]) -1:
             _, simple_pet = pf.add_new_pet_without_photo(auth_key, "Kitty", "cat", "2")
             status, result = pf.add_pets_photo(auth_key, simple_pet['id'], pet_photo)

     # Проверяем статус и ожидаемый результат
     assert status == 200
     assert result['pet_photo'] != ""


def test_upload_photo_to_pets_card_png(pet_photo="images\Grusha.png"):
    """ Проверяем загрузку фото png к питомцу без фото."""
    # P.S. Такая возможность написана в swagger документации, но она и там не работает.

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Перебираем по очереди питомцев в существующем списке
    for i in range(0, len(my_pets["pets"])):
        # Выбираем из них питомца без фото, загружаем этому питомцу фото и выходим из цикла
        if my_pets["pets"][i]["pet_photo"] == "":
            status, result = pf.add_pets_photo(auth_key, my_pets["pets"][i]['id'], pet_photo)
            break
        # Если мы дошли до конца списка питомцев, а питомца без фото не нашлось, добавим его, а затем загрузим фото
        if i == len(my_pets["pets"]) - 1:
            _, simple_pet = pf.add_new_pet_without_photo(auth_key, "Kitty", "cat", "2")
            status, result = pf.add_pets_photo(auth_key, simple_pet['id'], pet_photo)

    # Проверяем статус и ожидаемый результат
    assert status == 200
    assert result['pet_photo'] != ""
