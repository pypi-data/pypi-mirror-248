from petstoreapi.api import PetStore
from models.user import User
from models.pet import Pet
from models.device import Device
import pytest


@pytest.fixture
def petstore() -> PetStore:
    yield PetStore()


@pytest.mark.asyncio
async def test_user_create(petstore: PetStore) -> None:
    user = await petstore.user.create()
    assert isinstance(user, User)


@pytest.mark.asyncio
async def test_user_get(petstore: PetStore) -> None:
    user = await petstore.user.create()
    user2 = await petstore.user.get(user.uuid)
    assert user == user2


@pytest.mark.asyncio
async def test_user_delete(petstore: PetStore) -> None:
    user = await petstore.user.create()
    await petstore.user.delete(user.uuid)
    with pytest.raises(Exception):
        await petstore.user.get(user.uuid)


@pytest.mark.asyncio
async def test_device_create(petstore: PetStore) -> None:
    device = await petstore.device.create()
    assert isinstance(device, Device)


@pytest.mark.asyncio
async def test_device_get(petstore: PetStore) -> None:
    device = await petstore.device.create()
    device2 = await petstore.device.get(device.uuid)
    assert device == device2


@pytest.mark.asyncio
async def test_device_delete(petstore: PetStore) -> None:
    device = await petstore.device.create()
    await petstore.device.delete(device.uuid)
    with pytest.raises(Exception):
        await petstore.device.get(device.uuid)


@pytest.mark.asyncio
async def test_pet_create(petstore: PetStore) -> None:
    user = await petstore.user.create()
    device = await petstore.device.create()
    pet = await petstore.pet.create(user_uuid=user.uuid, device_uuid=device.uuid)
    assert isinstance(pet, Pet)


@pytest.mark.asyncio
async def test_pet_get(petstore: PetStore) -> None:
    user = await petstore.user.create()
    device = await petstore.device.create()
    pet = await petstore.pet.create(user_uuid=user.uuid, device_uuid=device.uuid)
    pet2 = await petstore.pet.get(pet.uuid)
    assert pet == pet2


@pytest.mark.asyncio
async def test_pet_delete(petstore: PetStore) -> None:
    user = await petstore.user.create()
    device = await petstore.device.create()
    pet = await petstore.pet.create(user_uuid=user.uuid, device_uuid=device.uuid)
    await petstore.pet.delete(pet.uuid)
    with pytest.raises(Exception):
        await petstore.pet.get(pet.uuid)
