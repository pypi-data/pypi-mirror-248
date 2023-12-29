import os
from typing import Any
from uuid import UUID
import aiohttp
from petstoremodels.pet import Pet as PetModel
from petstoremodels.user import User as UserModel
from petstoremodels.device import Device as DeviceModel
from .generate import generate_device, generate_pet, generate_user

_ENV = {
    "PETSTORE_HOST": os.environ["PETSTORE_HOST"],
    "PETSTORE_PORT": os.environ["PETSTORE_PORT"],
}


class Pet:
    def __init__(self, client: Any) -> None:
        self.client = client

    async def get(self, pet_uuid: UUID) -> PetModel:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.client.base_url}/pet/{pet_uuid}"
            ) as response:
                json = await response.json()
                return PetModel.model_validate(json)

    async def create(
        self,
        device_uuid: UUID,
        user_uuid: UUID,
        pet: PetModel | None = None,
    ) -> PetModel:
        if pet is None:
            pet = generate_pet(device_uuid=device_uuid, user_uuid=user_uuid)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.client.base_url}/pet", json=pet.model_dump(mode="json")
            ) as response:
                json = await response.json()
                return PetModel.model_validate(json)

    async def delete(self, pet_uuid: UUID) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{self.client.base_url}/pet/{pet_uuid}"):
                return None

    async def update_icon(self, pet_uuid: UUID, icon_id: str) -> PetModel:
        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{self.client.base_url}/pet/{pet_uuid}/icon/{icon_id}"
            ) as response:
                json = await response.json()
                return PetModel.model_validate(json)


class User:
    def __init__(self, client: Any) -> None:
        self.client = client

    async def get(self, user_uuid: UUID) -> UserModel:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.client.base_url}/user/{user_uuid}"
            ) as response:
                json = await response.json()
                return UserModel.model_validate(json)

    async def create(self, user: UserModel | None = None) -> UserModel:
        if user is None:
            user = generate_user()
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.client.base_url}/user", json=user.model_dump(mode="json")
            ) as response:
                json = await response.json()
                return UserModel.model_validate(json)

    async def delete(self, user_uuid: UUID) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{self.client.base_url}/user/{user_uuid}"):
                return None

    async def update_avatar(self, user_uuid: UUID, avatar_id: str) -> UserModel:
        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{self.client.base_url}/user/{user_uuid}/avatar/{avatar_id}"
            ) as response:
                json = await response.json()
                return UserModel.model_validate(json)


class Device:
    def __init__(self, client: Any) -> None:
        self.client = client

    async def get(self, device_uuid: UUID) -> DeviceModel:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.client.base_url}/device/{device_uuid}"
            ) as response:
                json = await response.json()
                return DeviceModel.model_validate(json)

    async def create(
        self, device: DeviceModel | None = None, num_functions: int = 5
    ) -> DeviceModel:
        if device is None:
            device = generate_device(num_functions=num_functions)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.client.base_url}/device", json=device.model_dump(mode="json")
            ) as response:
                if response.status != 200:
                    raise Exception(await response.text())
                json = await response.json()
                return DeviceModel.model_validate(json)

    async def delete(self, device_uuid: UUID) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{self.client.base_url}/device/{device_uuid}"):
                return None


class PetStore:
    pet: Pet
    user: User
    device: Device

    def __init__(self) -> None:
        self.base_url = f"http://{_ENV['PETSTORE_HOST']}:{_ENV['PETSTORE_PORT']}"
        self.pet = Pet(self)
        self.user = User(self)
        self.device = Device(self)
