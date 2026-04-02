from aiogram.filters import CommandStart, StateFilter, Command
from aiogram import Router, F
from aiogram.types import Message
import ssl
import certifi
from geopy.geocoders import Nominatim

from app.database.models import async_session, User, Photo
from app.database.request import check_user, get_user, check_admin, get_photos, get_all_users
import app.keyboards as kb
from aiogram.fsm.context import FSMContext

client = Router()

ctx = ssl.create_default_context(cafile=certifi.where())
geolocator = Nominatim(user_agent='TelegramBotForShop', ssl_context=ctx)

@client.message(CommandStart())
async def start(message: Message):
    is_registered = await check_user(message.from_user.id)
    if not is_registered:
        await message.answer('You need to registration! use command /reg or click on -> /reg \nYou can use /help command')
    else:
        await message.answer("Hello again, use this commands \n\n\n "
                             '/start - Start the bot\n'
                         '/reg - Register your account\n'
                         '/share - Share any photo\n'
                         '/weather - Show the weather\n'
                         '/currency - Show currency rates\n'
                         '/fact - Get a random useless fact')




@client.message(F.location, StateFilter('waiting for address'))
async def getting_location(message: Message, state: FSMContext):
    data = await state.get_data()
    address = geolocator.reverse(f'{message.location.latitude}, {message.location.longitude}',
                                 exactly_one=True, language='ru')
    user = await get_user(message.from_user.id)
    card_id = data.get('card_id')

    full_info = (
        f'New order\n\n'
        f'User: {user.name}, @{message.from_user.username}, ID-{user.tg_id}\n'
        f'number: {user.phone_number}\n'
        f'address: {address}\n'
        f'Thing ID {card_id}'

    )

    await message.bot.send_message(-4809427347, full_info)
    await message.answer('Perfect, waiting for admins', reply_markup=kb.menu)
    await state.clear()


@client.message(StateFilter('waiting for address'))
async def getting_location(message: Message, state: FSMContext):
    data = await state.get_data()
    address = message.text
    user = await get_user(message.from_user.id)
    card_id = data.get('card_id')

    full_info = (
        f'New order\n\n'
        f'User: {user.name}, @{message.from_user.username}, ID-{user.tg_id}\n'
        f'number: {user.phone_number}\n'
        f'address: {address}\n'
        f'Thing ID {card_id}'

    )

    await message.bot.send_message(-4809427347, full_info)
    await message.answer('Perfect, waiting for admins', reply_markup=kb.menu)
    await state.clear()


@client.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('/start - Start the bot\n'
                         '/reg - Register your account\n'
                         '/share - Share any photo\n'
                         '/weather - Show the weather\n'
                         '/currency - Show currency rates\n'
                         '/fact - Get a random useless fact')


@client.message(Command('share'))
async def share(message:Message, state:FSMContext):
    is_register = await check_user(message.from_user.id)
    if is_register:
        await message.answer('Share your picture')
        await state.set_state('waiting_photo')
    else:
        await message.answer('You need to register first! Click on -> /reg')


@client.message(F.photo, StateFilter('waiting_photo'))
async def getting_photo(message:Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    name = message.from_user.first_name
    tg_id = message.from_user.id
    print(file_id)

    async with async_session() as session:
        photo = Photo(image=file_id, name=name, tg_id=tg_id)
        session.add(photo)
        await session.commit()

    await message.answer('Photo saved ✅')
    await state.clear()

@client.message(F.text=='Photo')
async def get_all_photo(message: Message):
    is_admin = await check_admin(message.from_user.id)
    if is_admin:
        photos = await get_photos()
        print(photos)
        for photo in photos:
            await message.answer_photo(photo=photo.image, caption=f'name_of_user: {photo.name} \ntelegramID_of_user {photo.tg_id}')
    else :
        await message.answer('You are not admin')

@client.message(Command('broadcast'))
async def start_broadcast(message: Message, state: FSMContext):
    is_admin = await check_admin(message.from_user.id)
    if not is_admin:
        await message.answer('You are not admin')
        return
    await message.answer('Write your text for all users')
    await state.set_state('waiting_text')

@client.message(StateFilter('waiting_text'))
async def do_broadcast(message: Message, state: FSMContext):
    text = message.text
    users = await get_all_users()
    success = 0

    for user_id in users:
        try:
            await message.bot.send_message(chat_id=user_id, text=text)
            success += 1
        except Exception as e:
            print(f'Error : {e}')

    await message.answer(f'success = {success}')
    await state.clear()


@client.message(F.text)
async def text(message: Message):
    await message.reply('Unknown command to see all commands click on -> /help')

@client.message(F.photo)
async def get_photo(message:Message):
    file_id = message.photo[-1].file_id
    await message.answer(file_id)


