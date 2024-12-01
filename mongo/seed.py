import random

from faker import Faker

from setup_db import cats_collection


def seed_db():
    cats_collection.delete_many({})

    fake = Faker()

    features_list = [
        "likes to sleep", "chases mice", "friendly", "lazy", "playful",
        "noisy", "quiet", "curious", "adventurous", "likes to climb",
        "afraid of water", "loves fish", "independent", "loves cuddles",
        "scratches furniture", "afraid of strangers", "likes to hide", "smart"
    ]

    num_cats = 10

    for _ in range(num_cats):
        name = fake.first_name().lower()
        age = random.randint(1, 15)
        features = random.sample(features_list, k=random.randint(3, 5))

        cat = {
            'name': name,
            'age': age,
            'features': features
        }

        cats_collection.insert_one(cat)

    print(f"Inserted {num_cats} cats into the database")


if __name__ == '__main__':
    seed_db()
