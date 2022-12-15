from api import PetFriends
from settings import valid_email, valid_password

my_pf = PetFriends()
key = my_pf.get_api_key(valid_email, valid_password)
print(key)

pets_list = my_pf.get_list_of_pets(key[1], "my_pets")
print(pets_list)

new_pets_name = "Tom"
new_pets_type = "Mr. Cat"
new_pets_age = "1"
new_pets_photo = "tests/images/cat1.jpg"
new_pet = my_pf.add_new_pet(key[1], new_pets_name, new_pets_type, new_pets_age, new_pets_photo)
print(new_pet)
pet_id = new_pet[1]['id']

upd_name = "Sailor"
upd_type = "cat"
upd_age = "4"
upd_pet = my_pf.update_pet_info(key[1], pet_id, upd_name, upd_type, upd_age)
print(upd_pet)

del_pet = my_pf.delete_pet(key[1], pet_id)
print(del_pet)

new_pets_name = "Jack"
new_pets_type = "Mr. Dog"
new_pets_age = "3"
status, new_simple_pet = my_pf.add_new_pet_without_photo(key[1], new_pets_name, new_pets_type, new_pets_age)
print("Status code", status, "\nResponse body:", new_simple_pet)
pet_id = new_simple_pet['id']

pet_photo = "tests/images/cat1.jpg"
pet_with_photo = my_pf.add_pets_photo(key[1], pet_id, pet_photo)
print(pet_with_photo)

del_pet = my_pf.delete_pet(key[1], pet_id)
print(del_pet)
