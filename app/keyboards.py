from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

menu = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Catalog')],
        [KeyboardButton(text='Contacts')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Chose the one'
)

contacts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Telegram', url='https://t.me/Thenotoriousmma122')]
])

async def clients_name(name):
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=name)]],
                               resize_keyboard=True)

async def clients_phone():
    return ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text='Share ur contact',
                       request_contact=True)
    ]], resize_keyboard=True)

async def client_location():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Share location', request_location=True)]
    ], resize_keyboard=True)



