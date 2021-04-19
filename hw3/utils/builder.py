import faker

fake = faker.Faker()


class Builder:

    @staticmethod
    def create_title(title=None) -> str:
        if title is None:
            title = fake.lexify(text='???? ??? ??????')
        return title
