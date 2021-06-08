import faker

fake = faker.Faker()


class User:

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class Builder:

    @staticmethod
    def create_user(username=None, email=None, password=None):
        if username is None:
            username = fake.lexify('????????')
        if email is None:
            email = fake.email()
        if password is None:
            password = fake.bothify('##??#????#?#?')
        user = User(username, email, password)
        return user
