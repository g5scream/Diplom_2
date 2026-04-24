from faker import Faker


fake = Faker('en_US')

def generate_user(is_random=False, password_length=6):
    email_fmt = f"{fake.user_name()}.{fake.random_number(digits=7)}@yandex.ru"

    password = fake.password(
        length=password_length,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True
    )
    
    return {
        "email": email_fmt,
        "password": password,
        "name": fake.first_name()
    }