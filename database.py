import sqlite3 as sq
from aiogram import types
from keyboards import admin_panel, add_item, goods_tape, menu

db = sq.connect('tg.db')

cur = db.cursor()

tape_db = 0
async def db_start():
    cur.execute("""CREATE TABLE IF NOT EXISTS accounts(
        id INTEGER PRIMERY KEY,
        tg_id INTEGER,
        cart_id TEXT
        )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS items(
        id INTEGER PRIMERY KEY,
        name TEXT,
        desc TEXT,
        price TEXT,
        photo TEXT,
        type TEXT, 
        gender TEXT
        )""")
    
    db.commit()


async def cmd_start_db(user_id):
    user = cur.execute("""SELECT * FROM accounts WHERE tg_id == {key}""".format(key=user_id)).fetchone()
    if not user:
        cur.execute("""INSERT INTO accounts (tg_id) VALUES ({key})""".format(key=user_id))
        db.commit()
        
        
async def add_items(state):
    async with state.proxy() as data:
        cur.execute("""INSERT INTO items(name, desc, price, photo, type, gender) VALUES (?, ?, ?, ?, ?, ?)""", 
                    (data['name'], data['desc'], data['price'], data['photo'], data['type'], data['gender']))
        
        db.commit()

async def del_item(message: types.Message, state):
    
    async with state.proxy() as data:
        have = cur.execute("""SELECT * FROM items WHERE name == '{key}'""".format(key=data['name_del'])).fetchone()
        
        if message.text == 'Cancel':
            await state.finish()
            await message.answer('Make a choice:', 
                         reply_markup=admin_panel())
        elif not have:
            await message.answer('There is no product with this name\nTry again:')
            
        else:
            cur.execute("""DELETE FROM items WHERE name == '{key}'""".format(key=data['name_del']))
            db.commit()
            await state.finish()
            await message.answer('Delete succesfuly', 
                                 reply_markup=admin_panel())


async def give_item(message: types.Message, state):
    async with state.proxy() as data:
        item = cur.execute("""SELECT * FROM items WHERE photo == '{key}'""".format(key=data['photo'])).fetchone()
        
        await message.answer_photo(photo=item[4], caption=f'<i><b>Type:</b></i> {item[5]}\n<i><b>Name:</b></i> {item[1]}\n\
<i><b>Desc:</b></i> {item[2]}\n<i><b>Price:</b></i> <b>{item[3]} $</b>', 
                             parse_mode='html', 
                             reply_markup=add_item())
        

async def cancel_save_item(state):
    async with state.proxy() as data:
        cur.execute("""DELETE FROM items WHERE photo == '{key}'""".format(key=data['photo']))
        db.commit()
        

async def clothes(call: types.CallbackQuery, tape, cloth_type, gender):
    clothes = cur.execute(f"""SELECT * FROM items WHERE gender == '{gender}' and type == '{cloth_type}'""").fetchall()
    count = len(clothes) 
    if tape == count:
        pass
    
    else:
        prod = clothes[tape]
        await call.message.delete()
        
        await call.message.answer('Okay', 
                                  reply_markup=menu())
        await call.message.answer_photo(photo=prod[4], 
                                    caption=f'<b>{prod[1]}</b>\n\n<i>{prod[2]}</i>\n\n<code>Price: </code><b>{prod[3]} $</b>💵',
                                    parse_mode='html',
                                    reply_markup=goods_tape(tape, count))
        



async def next_cloth(call: types.CallbackQuery, cloth_type, gender):
    global tape_db
    clothes = cur.execute(f"""SELECT * FROM items WHERE gender == '{gender}' and type == '{cloth_type}'""").fetchall()
    count = len(clothes) 
    if tape_db + 1 >= count:
        pass
    
    else:
        tape_db += 1
        prod = clothes[tape_db]
        await call.message.delete()
        
        await call.message.answer('Okay', 
                                  reply_markup=menu())
        await call.message.answer_photo(photo=prod[4], 
                                    caption=f'<b>{prod[1]}</b>\n\n<i>{prod[2]}</i>\n\n<code>Price: </code><b>{prod[3]} $</b>💵',
                                    parse_mode='html',
                                    reply_markup=goods_tape(tape_db, count))
        

async def prev_cloth(call: types.CallbackQuery, cloth_type, gender):
    global tape_db
    clothes = cur.execute(f"""SELECT * FROM items WHERE gender == '{gender}' and type == '{cloth_type}'""").fetchall()
    count = len(clothes) 
    if tape_db == 0:
        pass
    else:
        tape_db -= 1
        prod = clothes[tape_db]
        await call.message.delete()
        
        await call.message.answer('Okay', 
                                  reply_markup=menu())
        await call.message.answer_photo(photo=prod[4], 
                                    caption=f'<b>{prod[1]}</b>\n\n<i>{prod[2]}</i>\n\n<code>Price: </code><b>{prod[3]} $</b>💵',
                                    parse_mode='html',
                                    reply_markup=goods_tape(tape_db, count))
        

async def clothes_mess(mess: types.Message, tape, cloth_type, gender):
    clothes = cur.execute(f"""SELECT * FROM items WHERE gender == '{gender}' and type == '{cloth_type}'""").fetchall()
    count = len(clothes) 
    if tape == count:
        pass
    else:
        prod = clothes[tape]
        
        await mess.answer_photo(photo=prod[4], 
                                    caption=f'<b>{prod[1]}</b>\n\n<i>{prod[2]}</i>\n\n<code>Price: </code><b>{prod[3]} $</b>💵',
                                    parse_mode='html',
                                    reply_markup=goods_tape(tape, count))
    
