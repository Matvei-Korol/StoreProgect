from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def if_user_keyb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton('Catalog'), KeyboardButton('Contacts')]
    ])
    
    return kb


def if_admin_keyb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton('Catalog'),],
        [ KeyboardButton('Contacts'), KeyboardButton('Admin-panel')]
    ])
    
    return kb


def admin_panel() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton('Add product'), KeyboardButton('Delete product')],
        [KeyboardButton('Menu🏠'), KeyboardButton('Make newsletter')]
    ])
    
    return kb


def catalog() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton('T-shirts👕', callback_data='shirts'), InlineKeyboardButton('Shorts🩳', callback_data='shorts')], 
         [InlineKeyboardButton('Sneakers👟', callback_data='sneakers')]
    ])
    
    return ikb


def cancel() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton('Back🔙'), KeyboardButton("Cancel🚫")]
    ])

    return kb


def select_m_or_w()-> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton('men'), KeyboardButton('women')],
        [KeyboardButton('Back🔙'), KeyboardButton("Cancel🚫")]
    ])

    return kb


def add_item() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton('Add✅', callback_data='add'), InlineKeyboardButton('Cancel🛑', callback_data='cancel')]
    ])
    
    return ikb

def gender_cloth() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton('Men 🙋‍♂', callback_data='men_cloth'), InlineKeyboardButton('Women 🙋‍♀', callback_data='women_cloth')],
        [InlineKeyboardButton('Back🔙', callback_data='back')]
    ])
    
    return ikb


def goods_tape(tape, count) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
        [InlineKeyboardButton(f'{tape + 1}|{count}', callback_data='count')],
        [InlineKeyboardButton('◀', callback_data='prev_prod'), InlineKeyboardButton('Buy🛒', callback_data='buy'),InlineKeyboardButton('▶', callback_data='next_prod')]
    ])
    
    return ikb

def cancel_payment() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton('Cancel🚫')]
    ])
    
    return kb

def menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton('Menu🏠')]
    ])
    
    return kb

def contacts() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton('BOT', callback_data='bot_support')],
        [InlineKeyboardButton('Back🔙', callback_data='back')]
    ])
    
    return ikb