from pymongo.errors import PyMongoError

from setup_db import cats_collection

from seed import seed_db


def display_all_cats():
    try:
        if cats_collection.count_documents({}) == 0:
            print("No cats found")
            return
        cats = cats_collection.find()
        for cat in cats:
            print(f"Name: {cat['name']}, Age: {cat['age']}, Features: {', '.join(cat['features'])}")
    except PyMongoError as e:
        print(f"An error occurred: {e}")


def find_cat_by_name(name):
    try:
        cat = cats_collection.find_one({'name': name})
        if cat:
            print(f"Name: {cat['name']}, Age: {cat['age']}, Features: {', '.join(cat['features'])}")
        else:
            print(f"Cat '{name}' not found.")
    except PyMongoError as e:
        print(f"An error occurred: {e}")


def update_cat_age(name, new_age):
    try:
        result = cats_collection.update_one({'name': name}, {'$set': {'age': new_age}})
        if result.matched_count > 0:
            print(f"Cat '{name}' age updated to {new_age}.")
        else:
            print(f"Cat '{name}' not found.")
    except PyMongoError as e:
        print(f"An error occurred: {e}")


def add_feature_to_cat(name, new_feature):
    try:
        result = cats_collection.update_one({'name': name}, {'$push': {'features': new_feature}})
        if result.matched_count > 0:
            print(f"Feature '{new_feature}' added to cat '{name}'.")
        else:
            print(f"Cat '{name}' not found.")
    except PyMongoError as e:
        print(f"An error occurred: {e}")


def delete_cat_by_name(name):
    try:
        result = cats_collection.delete_one({'name': name})
        if result.deleted_count > 0:
            print(f"Cat '{name}' deleted.")
        else:
            print(f"Cat '{name}' not found.")
    except PyMongoError as e:
        print(f"An error occurred: {e}")


def delete_all_cats():
    try:
        result = cats_collection.delete_many({})
        print(f"All cats deleted. Total deleted: {result.deleted_count}")
    except PyMongoError as e:
        print(f"An error occurred: {e}")


def main():
    seed_db()
    print()

    print("Display all cats")
    display_all_cats()
    print()

    print("Get the name of the first cat for testing")
    first_cat = cats_collection.find_one()
    if first_cat:
        test_name = first_cat['name']
        print(f"Name: {test_name}, Age: {first_cat['age']}")
    else:
        print("No cats in the database.")
        return
    print()

    print("Find a cat by name")
    find_cat_by_name(test_name)
    print()

    print("Update a cat's age")
    new_age = first_cat['age'] + 1
    update_cat_age(test_name, new_age)
    print()

    print("Add a feature to a cat")
    new_feature = 'loves catnip'
    add_feature_to_cat(test_name, new_feature)
    print()

    print("Display the updated cat")
    find_cat_by_name(test_name)
    print()

    print("Delete a cat by name")
    delete_cat_by_name(test_name)
    print()

    print("Try to find the deleted cat")
    find_cat_by_name(test_name)
    print()

    print("Delete all cats")
    delete_all_cats()
    print()

    print("Display all cats to confirm deletion")
    display_all_cats()
    print()


if __name__ == '__main__':
    main()
