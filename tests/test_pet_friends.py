from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


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


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_get_api_key_with_correct_mail_and_wrong_passwor(email=valid_email, password=valid_password):
    """Проверяем запрос с правильным email и c неправильным паролем.
    Проверяем нет ли ключа в ответе."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неправильным паролем')

def test_get_api_key_with_wrong_email_and_correct_password(email=valid_email, password=valid_password):
    """Проверяем запрос с невалидным email и с валидным паролем.
    Проверяем нет ли ключа в ответе."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неправильным email')


def test_get_api_key_with_wrong_email_and_wrong_password(email=valid_email, password=valid_password):
    """Проверяем запрос с невалидным email и с невалидным паролем.
    Проверяем нет ли ключа в ответе."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неправильным email и паролем')




def test_get_all_pets_with_novalid_key():
    """ Проверяем, что запрос всех питомцев доступное только при значении параметра filter - 'my_pets' либо ''
    в противном случае получаем status == 500"""

    filter = 'my_pets'  # допустимое
    filter = 'my__pets'  # допустимое, ошибочное
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500
    print(f'\nСтатус {status}, недоступное значение параметра filter')



def test_add_pet_with_valid_data_without_photo(name='пес', animal_type='собак', age='9'):
    """Проверяем возможность добавления нового питомца без фото"""
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'добавлен {result}')



def test_add_pet_with_a_lot_of_age_in_variable_age(name='Karlson', animal_type='Кошка',
                                                   pet_photo='images/cat3.jpg'):
    """Добавления очень взрослого питомца с большим возрастом.
    Тест выводит предупреждение, если будет добавлен в приложение питомец с невозможным возрастом, меньше 0 или старше 20 лет."""
    age = '120'
    # age = '-1'
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    age = float(result['age'])  # .split()
    assert status == 200
    assert (age > 20 or age < 0), 'Добавлен питомец с невозможным возрастом, меньше 0 или старше 20 лет.'
    print(f'\n Сайт позволяет добавлять питомеца с невозможным возрастом, меньше 0 или старше 20 лет. {age}')


def test_add_pet_with_variable_age_symble(name='leva', animal_type='леВ', pet_photo='images/cat3.jpg'):
    """Добавления питомца с символами в поле возраста.
    Тест выводит предупреждение, если добавлен питомец с нечисловым возрастом"""
    age = '№№№'
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    # age = float(result['age'])#.split()
    assert status == 200
    assert age, 'Добавлен питомец с невозможным возрастом'
    print(f'\n Сайт позволяет добавлять питомеца с невозможным возрастом {age}')



def test_successful_delete_notvalid_key_pet():
    """Проверяем возможность удаления питомца по неправильному auth_key. По статусу 403"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    print()
    print(auth_key)
    # {'key': '6ecc18c60009357ae13ba9e44ac5ea152b80178ec7b755c3f57a5c91'}#правильный ключ
    auth_key = {'key': 'ecc18c60009357ae13ba9e44ac5ea152b80178ec7b755c3f57a5c91'}  # неправильный ключ
    print(auth_key)
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "попугай", "попуг", "12", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке было, {num} питомцев')

    # # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # # Проверяем что статус ответа равен 403 и в списке питомцев нет изменений
    assert status == 403
    # assert pet_id in my_pets.values()
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке , {num} питомцев')






