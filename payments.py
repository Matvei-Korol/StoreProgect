from aiogram.types import ShippingOption, ShippingQuery, LabeledPrice, PreCheckoutQuery
from aiogram.types.message import ContentType
from aiogram import types
import sqlite3 as sq
from dotenv import load_dotenv
import os
from keyboards import cancel_payment
from main import bot

load_dotenv()

db = sq.connect('tg.db')

cur = db.cursor()


SUPERSPEED_SHIPPING_OPTION = ShippingOption(
    id = 'superspeed',
    title = 'Superspeed!)'
).add(LabeledPrice(label='Personally in hands', amount=300))


async def buy_process(call: types.CallbackQuery, tape, cloth_type, gender):
    
    items = cur.execute(f"""SELECT * FROM items WHERE gender == '{gender}' and type == '{cloth_type}'""").fetchall()
    prod = items[tape]
    
    PRICES = [
    LabeledPrice(label=f'{prod[5]}', amount=prod[3])
]

        
    await bot.send_invoice(call.message.chat.id, 
                           title=f'{prod[1]}', 
                           description=f'{prod[2]}', 
                           provider_token=os.getenv('PAY_TOKEN'), 
                           currency='usd',  
                           need_email=True, 
                           need_phone_number=True, 
                           is_flexible=True, 
                           prices=PRICES, 
                           start_parameter='example', 
                           payload='some_invoice')
    
    await call.message.answer('Cancel payment?',
                              reply_markup=cancel_payment())






# POST_SHIPPING_OPTION =  ShippingOption(
#     id = 'post',
#     title = 'Post Russia'
# ).add(LabeledPrice('Cardboard box', 300))


# PICKUP_SHIPPING_OPTION = ShippingOption(
#     id = 'pickup', 
#     title = 'Pickup'
# ).add(LabeledPrice('Pickup in Moscow', 300))