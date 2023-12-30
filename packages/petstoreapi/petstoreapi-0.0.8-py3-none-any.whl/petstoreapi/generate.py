from uuid import UUID
from petstoremodels.user import User
from petstoremodels.pet import Pet, Character, Traits
from petstoremodels.device import Function, Device, Skeleton, Display, Prompt
from random_username.generate import generate_username
from faker import Faker
from gptfunction.GPTFunction import GPTFunction

fake = Faker()


def generate_user() -> User:
    first, last, *_ = fake.name().split(" ")
    return User(
        username=generate_username(1)[0],
        first_name=first,
        last_name=last,
        email=f"{first}.{last}@fakemail.com",
    )


def generate_pet(user_uuid: UUID, device_uuid: UUID) -> Pet:
    pet_name = generate_username(1)[0]
    return Pet(
        model="gpt-3.5-turbo-1106",
        user=user_uuid,
        device=device_uuid,
        character=Character(
            name=pet_name,
            personality=f"Your name is {pet_name}. You are a {fake.job()}.",
            traits=Traits(
                extraversion=fake.pyint(0, 10),
                agreeableness=fake.pyint(0, 10),
                openness=fake.pyint(0, 10),
                conscientiousness=fake.pyint(0, 10),
                neuroticism=fake.pyint(0, 10),
            ),
            voice=Display(name="gpt_whisper", args={"voice": "fable"}),
        ),
    )


def generate_device(num_functions: int = 5) -> Device:
    return Device(
        model_name=fake.word(),
        skeleton=Skeleton(
            displays=[
                Display(name="text"),
            ],
            functions=[_generate_function() for _ in range(num_functions)],
        ),
    )


def _generate_function() -> Function:
    func = lambda: None  # noqa: E731
    func.__name__ = fake.word()
    func.__doc__ = fake.sentence()
    gpt_func = GPTFunction(func)

    return Function.model_validate(gpt_func.schema()["function"])
