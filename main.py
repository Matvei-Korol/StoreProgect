from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from dotenv import load_dotenv
import os
from keyboards import if_user_keyb, if_admin_keyb, admin_panel, catalog, cancel, \
    gender_cloth, select_m_or_w, menu, contacts
from aiogram.dispatcher.filters import Text
import database as db
import payments as pay
from messages import MESSAGES



storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)

async def on_startup(_):
    await db.db_start()
    print('SYSTEM: bot started...')

tape = 0
gender = ''

class NewOrder(StatesGroup):
    type = State()
    gender = State()
    name = State()
    desc = State()
    price = State()
    photo = State()
    
    
class DeleteProduct(StatesGroup):
    name_del = State()


class Payment(StatesGroup):
    buy = State()
    
    
@dp.message_handler(commands=['id'])
async def start_cmd(message: types.Message):
    
    await message.answer(f'{message.from_user.id}')

# ___________________________________START -->

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    global id_us
    await db.cmd_start_db(message.from_user.id)
    
    id_us = message.from_user.id
    
    if id_us == int(os.getenv('ADMIN_ID')):
        await message.answer('You are logged in as an admin:', 
                             reply_markup=if_admin_keyb())
    
    elif id_us != int(os.getenv('ADMIN_ID')):
        name = message.from_user.first_name
        await message.answer(f"Hello <b>{name}</b>\nWelcome in telegram store!)", 
                            reply_markup=if_user_keyb(), 
                            parse_mode='html')
    
# ___________________________________START -->
@dp.message_handler(Text(equals='Menu🏠'))
async def menu_cmd(message: types.Message):
    id_us = message.from_user.id       
    
    if id_us == int(os.getenv('ADMIN_ID')):
        await message.answer('Make a choice:', 
                             reply_markup=if_admin_keyb())
    
    elif id_us != int(os.getenv('ADMIN_ID')):
        await message.answer(f"Make a choice:", 
                            reply_markup=if_user_keyb())
# __________________________________CATALOG -->
@dp.message_handler(Text(equals=['Catalog']))
async def catalog_cmd(message: types.Message):
    await message.answer('Okey', 
                         reply_markup=ReplyKeyboardRemove())
    await message.answer('What clothes do you need?', 
                         reply_markup=gender_cloth())
    


@dp.callback_query_handler()
async def clothes(call: types.CallbackQuery):
    global tape, gender, cloth_type, id_us
    if call.data == 'men_cloth':
        await call.message.edit_text('Select product type:', 
                                     reply_markup=catalog())
        
        gender = 'men'
        
    elif call.data == 'women_cloth':
        await call.message.edit_text('Select product type:', 
                                     reply_markup=catalog())
        
        gender = 'women'
        
    elif call.data == 'shirts':
        await call.answer('T-shirts👕')
        
        cloth_type = 'shirts'
        
        await db.clothes(call, tape, cloth_type, gender)
        
    elif call.data == 'shorts':
        await call.answer('Shorts🩳')
        
        cloth_type = 'shorts'
        
        await db.clothes(call,tape, cloth_type, gender)
    
    elif call.data == 'sneakers':
        await call.answer('Sneakers👟')
        
        cloth_type = 'sneakers'
        
        await db.clothes(call, tape, cloth_type, gender)
        
    elif call.data == 'prev_prod':
        
        await db.prev_cloth(call, cloth_type, gender)
    
    elif call.data == 'next_prod':
        
        await db.next_cloth(call, cloth_type, gender)
        
    
    elif call.data == 'buy':
        await Payment.buy.set()
        await pay.buy_process(call, tape, cloth_type, gender)
    
    
    elif call.data == 'back':
        if id_us == int(os.getenv('ADMIN_ID')):
            await call.message.answer('Make a choice:', 
                             reply_markup=if_admin_keyb())
    
        elif id_us != int(os.getenv('ADMIN_ID')):
            await call.message.answer(f"Make a choice:", 
                            reply_markup=if_user_keyb())
        
# ____________________FSM BUY PRODUCT -->
@dp.message_handler(state=Payment.buy)
async def pay_st(mess: types.Message, state=FSMContext):
    global tape, gender, cloth_type
    
    if mess.text == 'Cancel🚫':
        await mess.answer('Okay..', 
                          reply_markup=menu())
        await db.clothes_mess(mess, tape, cloth_type, gender)
        await state.finish()
    else:
        await mess.answer("I don't understand you!")
        
        
@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    
@dp.message_handler(content_types=types.message.ContentType.SUCCESSFUL_PAYMENT, state=Payment.buy)
async def succesful_payment(message: types.Message, state=FSMContext):
    await bot.send_message(message.chat.id, MESSAGES['successful_payment'].format(total_amount=message.successful_payment.total_amount, 
                                                                                  currency=message.successful_payment.currency))
    await state.finish()

# __________________________________CONTACTS -->


@dp.message_handler(Text(equals=['Contacts']))
async def contacts_cmd(message: types.Message):
    await message.answer('Contacts: \n \
        @ProgerPy', 
        reply_markup=contacts())
    
# __________________________________ADMIN_PANEL -->

@dp.message_handler(Text(equals=['Admin-panel']))
async def admin_panel_cmd(message: types.Message):
    
    id_us = message.from_user.id
    
    if id_us == int(os.getenv('ADMIN_ID')):
        await message.answer('You are logged into the admin panel:', 
                         reply_markup=admin_panel())
    else:
        await message.answer("I don't understanding you")


@dp.message_handler(Text(equals=['Delete product']))
async def add_item(message: types.Message):
    
    id_us = message.from_user.id
    
    if id_us == int(os.getenv('ADMIN_ID')):
        await DeleteProduct.name_del.set()
        await message.answer('Please enter product name:', 
                             reply_markup=cancel())
    else:
        await message.answer("I don't understanding you")

# ____________________FSM DELETE PRODUCT -->

@dp.message_handler(state=DeleteProduct.name_del)
async def del_product(message: types.Message, state: FSMContext):
    
    if message.text == 'Cancel🚫':
        await state.finish()
        await message.answer('Make a choice:', 
                             reply_markup=admin_panel())
    else:
        async with state.proxy() as data:
            data['name_del'] = message.text
            
        await db.del_item(message, state)
#___________________________________________________________ 
    
@dp.message_handler(Text(equals=['Add product']))
async def add_item(message: types.Message):
    
    id_us = message.from_user.id
    
    if id_us == int(os.getenv('ADMIN_ID')):
        await NewOrder.type.set()
        await message.answer('Select product type:', 
                             reply_markup=catalog())
    else:
        await message.answer("I don't understanding you")
# ____________________FSM ADD PRODUCT -->

@dp.callback_query_handler(state=NewOrder.type)
async def add_item_type(call: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        data['type'] = call.data
    
    await call.message.answer('Select a product gender:', 
                              reply_markup=select_m_or_w())
    await NewOrder.next()


@dp.message_handler(state=NewOrder.gender)
async def add_item_gender(message: types.Message, state: FSMContext):
    
    if message.text == 'Cancel🚫':
        
        await state.finish()
        await message.answer('Make a choice:', 
                             reply_markup=admin_panel())
    
    elif message.text == 'Back🔙':
        await NewOrder.previous()
        await message.answer('Select a product type:', 
                             reply_markup=catalog())

    else:
        async with state.proxy() as data:
            data['gender'] = message.text
        
        await message.answer('Write a product name:', 
                                reply_markup=cancel())
        await NewOrder.next()


@dp.message_handler(state=NewOrder.name)
async def add_item_name(message: types.Message, state: FSMContext):
    
    if message.text == 'Cancel🚫':
        
        await state.finish()
        await message.answer('Make a choice:', 
                             reply_markup=admin_panel())
    
    elif message.text == 'Back🔙':
        await NewOrder.previous()
        await message.answer('Select a product gender:', 
                             reply_markup=select_m_or_w())
        
    else:
        async with state.proxy() as data:
            data['name'] = message.text
        
        await message.answer('Write a product description:', 
                                reply_markup=cancel())
        await NewOrder.next()


@dp.message_handler(state=NewOrder.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    
    if message.text == 'Cancel🚫':
        await state.finish()
        await message.answer('Make a choice:', 
                             reply_markup=admin_panel())
    
    elif message.text == 'Back🔙':
        await NewOrder.previous()
        await message.answer('Write a product name:')
    
    else:
        async with state.proxy() as data:
            data['desc'] = message.text
        
        await message.answer('Write a product price($):')
        await NewOrder.next()
    
    
@dp.message_handler(state=NewOrder.price)
async def add_item_price(message: types.Message, state: FSMContext):
    
    if message.text == 'Cancel🚫':
        await state.finish()
        await message.answer('Make a choice:', 
                             reply_markup=admin_panel())
    elif message.text == 'Back🔙':
        await NewOrder.previous()
        await message.answer('Write a product description:')
        
    else:
        async with state.proxy() as data:
            data['price'] = message.text + '00'
        
        await message.answer('Send a product photo:')
        await NewOrder.next()


@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def add_item_photo_check(message: types.Message, state: FSMContext):
    
    if message.text == 'Cancel🚫':
        await state.finish()
        await message.answer('Make a choice:', 
                             reply_markup=admin_panel())
        
    elif message.text == 'Back🔙':
        await NewOrder.previous()
        await message.answer('Write a product price($):')
    else:
        await message.answer('This is not a photo!\n Try again.')
    
    
@dp.message_handler(content_types=['photo'], state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):

        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
            
        await db.add_items(state)
        
        await db.give_item(message, state)
        
        
# _________________________________________________________

@dp.callback_query_handler(state=NewOrder.photo)
async def ch_save_item(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'add':
        await call.answer('Add✅')
        await call.message.delete()
        await call.message.answer('Product added.', 
                            reply_markup=admin_panel())
        await state.finish()
    elif call.data == 'cancel':
        await call.answer('Cancel🛑')
        await db.cancel_save_item(state)
        await call.message.delete()
        
        await state.finish()
        
        await call.message.answer('Make a choice:', 
                             reply_markup=admin_panel())


@dp.message_handler()
async def un_understand(message: types.Message):
    await message.answer("I don't understanding you!")


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           on_startup=on_startup,
                           skip_updates=True)
    