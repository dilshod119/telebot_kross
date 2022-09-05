from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from aiogram.dispatcher.filters import Text
from keyboards.client_kb import bm_f, button_1, bl_f, bt_f, bn_f
import sqlite3
from email_validator import validate_email


base_storis = sqlite3.connect('base_storis.db')
cur_storis = base_storis.cursor()


base = sqlite3.connect('base.db')
cur = base.cursor()
"""   РЕГИСТРАЦИЯ   """

async def welcome(message: types.Message):
    try:
        cur.execute('INSERT INTO data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (message.from_user.id, 'Null', 'Null', 'Null', 'Null', 1, 'Null', 'Null', 0))
        base.commit()
        await message.answer ('Вы согласны на обработку персональных данных?', reply_markup= button_1)
    except sqlite3.IntegrityError:
        await message.answer('🔆Меню', reply_markup=bm_f)

class user_reg(StatesGroup):
    name = State()
    email = State()
    phone = State()


async def welcome_conf(callback: types.CallbackQuery):
    await callback.message.answer ('👤 Как тебя зовут?')
    await user_reg.next()


async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(name= message.text)
    await message.answer('📪 Укажите электронную почту\n\n<i>Пример: <code>user@mail.ru</code></i>', parse_mode= 'html')
    await user_reg.next()


async def get_email(message: types.Message, state: FSMContext):
    await state.update_data(email= message.text)
    try:
        validate_email(message.text, check_deliverability= True)
        await message.answer('☎️ Напишите номер телефона\n\n<i>Пример: <code>+79008505050</code></i>', parse_mode= 'html')
        await user_reg.next()
    except:
        await message.answer('❌Неправильный формат\n\n<i>Пример: <code>user@mail.ru</code></i>', parse_mode= 'html')



async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone= message.text)
    while Text(startswith= '+7') and len(message.text) == 12:
        data = await state.get_data()
        cur.execute('UPDATE data SET name ==?, email ==?, phone ==?, bal ==?, user_name ==? WHERE id ==?', (data['name'], data['email'], data['phone'], '0', message.from_user.username, message.from_user.id))
        base.commit()
        base_storis.execute(f"CREATE TABLE IF NOT EXISTS {'id_' + str(message.from_user.id)} (id PRIMARY KEY, size)")
        base_storis.commit()
        await state.finish()
        await message.answer('🔆Меню', reply_markup=bm_f)
        break
    else:
        await message.answer('❌Неправильный формат\n\n<i>Пример: <code>+79008505050</code></i>', parse_mode= 'html')

"""  РАЗДЕЛЫ   """

async def office_lk(message: types.Message):
    name, promo, email, phone = cur.execute('SELECT name, promo, email, phone FROM data WHERE id ==?', (message.from_user.id,)).fetchone()
    await message.answer(f'<b>🔎 Ваш id:</b> <i>{message.from_user.id}</i>\n\n<b>👤 Имя:</b> <i>{name}</i> \n<b>📪 Эл.Почта:</b> <i>{email}</i>\n<b>☎️ Номер телефона:</b> <i>{phone}</i>\n\n<b>🎁Бонусные рубли:</b> {promo} руб.', reply_markup= bl_f, parse_mode='html')

async def office_tov(message: types.Message):
    await message.answer('🛍Выберите категорию', reply_markup=bt_f)

async def office_tov_cb(callback: types.CallbackQuery):
    await callback.message.delete()

"""   Активные заказы"""
async def active_order(callback: types.CallbackQuery):
    i = cur.execute('SELECT * FROM order_basket').fetchall()
    for m in i:
        if m[0] == callback.from_user.id:
            if m[4] == 'Передано в доставку':
                await callback.bot.send_photo(m[0], m[11], f"<b>1. id заказа:</b> <code>{m[2]}</code>\n<b>2. Название товара:</b> {m[9]}\n<b>3. Размер:</b> {m[3]}\n<b>4. Цена:</b> {m[10]} руб.\n<b>5. Адрес доставки:</b> {m[8]}", parse_mode= 'html', reply_markup= InlineKeyboardMarkup().add(InlineKeyboardButton('✅Передано в доставку', callback_data='None')))     
        elif m[4] != 'Передано в доставку':
            await callback.answer('У вас нет заказов😔', show_alert= True)

"""   История покупок   """
async def history_user_f(callback: types.CallbackQuery):
    order = cur.execute('SELECT * FROM order_basket').fetchall()
    inl = InlineKeyboardMarkup().add(InlineKeyboardButton('✅Завершено', callback_data= 'None'))
    how = 0
    for i in order:
        if i[0] == callback.from_user.id and i[4] == 'Доставлено':
            await callback.message.answer_photo(i[11], f"<b>1. id заказа:</b> <code>{i[2]}</code>\n<b>2. id товара:</b> <code>{i[1]}</code>\n<b>3. Название товара:</b> {i[9]}\n<b>4. Размер:</b> {i[3]}\n<b>5. Цена:</b> <code>{i[10]}</code>\n<b>6. Оплачено бонусами:</b> <code>{i[12]}</code>\n<b>7. Итоговая сумма:</b> <code>{int(i[10]) - int(i[12])}</code>", parse_mode= 'html', reply_markup= inl)
            print('ok')
            how += 1
    if how == 0:
        await callback.answer('🔎Категория пуста', show_alert= True)

"""   ТОВАРЫ У ЮЗЕРА И ДОБАВЛЕНИЕ В КОРЗИНУ   """
"""Мужские"""
async def office_mu(callback: types.CallbackQuery):
    try:
        number = 1
        i = cur.execute('SELECT rowid, * FROM men_kross WHERE rowid ==?', (number,)).fetchone()    
        row = InlineKeyboardButton('Следущий', callback_data='next')
        row_back = InlineKeyboardButton('Предыдущий', callback_data='back')
        bkar = InlineKeyboardButton('🗑Добавить товар в корзину', callback_data=f'size {i[6]}')
        price_back = InlineKeyboardButton('⬅️Назад', callback_data='office_tov_inline')
        bkar_f = InlineKeyboardMarkup()
        bkar_f.add(row_back, row).add(bkar).add(price_back)
        await callback.message.answer_photo(i[5], f"<b>{i[1]}</b>\n\n📜Описание: <b>{i[2]}</b>\n💰Цена: <b>{i[3]} руб.</b>", parse_mode='html', reply_markup= bkar_f)
        cur.execute('UPDATE data SET products_id ==? WHERE id ==?', (number, callback.from_user.id))
        base.commit()
    except TypeError:
        await callback.answer('Категория пуста', show_alert= True)

async def next_ti(callback: types.CallbackQuery):
    try:
        rowid_s = cur.execute('SELECT products_id FROM data WHERE id ==?', (callback.from_user.id,)).fetchone()
        i = cur.execute('SELECT rowid, * FROM men_kross WHERE rowid ==?', (int(rowid_s[0]) + 1,)).fetchone()
        row = InlineKeyboardButton('Следущий', callback_data='next')
        row_back = InlineKeyboardButton('Предыдущий', callback_data='back')
        bkar = InlineKeyboardButton('🗑Добавить товар в корзину', callback_data=f'size {i[6]}')
        price_back = InlineKeyboardButton('⬅️Назад', callback_data='office_tov_inline')
        bkar_f = InlineKeyboardMarkup()
        bkar_f.add(row_back, row).add(bkar).add(price_back)
        await callback.message.edit_media(InputMediaPhoto(i[5], caption= f"<b>{i[1]}</b>\n\n📜Описание: <b>{i[2]}</b>\n💰Цена: <b>{i[3]} руб.</b>", parse_mode='html'), reply_markup= bkar_f)
        rowid_new = 1 + int(rowid_s[0])
        cur.execute('UPDATE data SET products_id ==? WHERE id ==?', (rowid_new, callback.from_user.id))
        base.commit()
    except TypeError:
        await callback.answer('Вы посмотрели все товары в категории', show_alert= True)

async def back_ti(callback: types.CallbackQuery):
    try:
        rowid_s = cur.execute('SELECT products_id FROM data WHERE id ==?', (callback.from_user.id,)).fetchone()
        i = cur.execute('SELECT rowid, * FROM men_kross WHERE rowid ==?', (int(rowid_s[0]) - 1,)).fetchone()
        row = InlineKeyboardButton('Следущий', callback_data='next')
        row_back = InlineKeyboardButton('Предыдущий', callback_data='back')
        bkar = InlineKeyboardButton('🗑Добавить товар в корзину', callback_data=f'size {i[6]}')
        price_back = InlineKeyboardButton('⬅️Назад', callback_data='office_tov_inline')
        bkar_f = InlineKeyboardMarkup()
        bkar_f.add(row_back, row).add(bkar).add(price_back)
        await callback.message.edit_media(InputMediaPhoto(i[5], caption = f"<b>{i[1]}</b>\n\n📜Описание: <b>{i[2]}</b>\n💰Цена: <b>{i[3]} руб.</b>", parse_mode='html'), reply_markup= bkar_f)
        rowid_new = int(rowid_s[0]) - 1
        cur.execute('UPDATE data SET products_id ==? WHERE id ==?', (rowid_new, callback.from_user.id))
        base.commit()
    except TypeError:
        await callback.answer('Листайте следующий товар', show_alert= True)

"""Женские"""
async def office_zh(callback: types.CallbackQuery):
    try:
        number = 1
        i = cur.execute('SELECT rowid, * FROM girl_kross WHERE rowid ==?', (number,)).fetchone()    
        row = InlineKeyboardButton('Следущий', callback_data='next_zh')
        row_back = InlineKeyboardButton('Предыдущий', callback_data='back_zh')
        bkar = InlineKeyboardButton('🗑Добавить товар в корзину', callback_data=f'size_zh {i[6]}')
        price_back = InlineKeyboardButton('⬅️Назад', callback_data='office_tov_inline')
        bkar_f = InlineKeyboardMarkup()
        bkar_f.add(row_back, row).add(bkar).add(price_back)
        await callback.message.answer_photo(i[5],  f"<b>{i[1]}</b>\n\n📜Описание: <b>{i[2]}</b>\n💰Цена: <b>{i[3]} руб.</b>", parse_mode='html', reply_markup= bkar_f)
        cur.execute('UPDATE data SET products_id ==? WHERE id ==?', (number, callback.from_user.id))
        base.commit()
    except TypeError:
        await callback.answer('Категория пуста', show_alert= True)

async def next_tim(callback: types.CallbackQuery):
    try:
        rowid_s = cur.execute('SELECT products_id FROM data WHERE id ==?', (callback.from_user.id,)).fetchone()
        i = cur.execute('SELECT rowid, * FROM girl_kross WHERE rowid ==?', (int(rowid_s[0]) + 1,)).fetchone()
        row = InlineKeyboardButton('Следущий', callback_data='next_zh')
        row_back = InlineKeyboardButton('Предыдущий', callback_data='back_zh')
        bkar = InlineKeyboardButton('🗑Добавить товар в корзину', callback_data=f'size_zh {i[6]}')
        price_back = InlineKeyboardButton('⬅️Назад', callback_data='office_tov_inline')
        bkar_f = InlineKeyboardMarkup()
        bkar_f.add(row_back, row).add(bkar).add(price_back)
        await callback.message.edit_media(InputMediaPhoto(i[5], caption= f"<b>{i[1]}</b>\n\n📜Описание: <b>{i[2]}</b>\n💰Цена: <b>{i[3]} руб.</b>", parse_mode='html'), reply_markup= bkar_f)
        rowid_new = 1 + int(rowid_s[0])
        cur.execute('UPDATE data SET products_id ==? WHERE id ==?', (rowid_new, callback.from_user.id))
        base.commit()
    except TypeError:
        await callback.answer('Вы посмотрели все товары в категории', show_alert= True)

async def back_tim(callback: types.CallbackQuery):
    try:
        rowid_s = cur.execute('SELECT products_id FROM data WHERE id ==?', (callback.from_user.id,)).fetchone()
        i = cur.execute('SELECT rowid, * FROM girl_kross WHERE rowid ==?', (int(rowid_s[0]) - 1,)).fetchone()
        row = InlineKeyboardButton('Следущий', callback_data='next_zh')
        row_back = InlineKeyboardButton('Предыдущий', callback_data='back_zh')
        bkar = InlineKeyboardButton('🗑Добавить товар в корзину', callback_data=f'size_zh {i[6]}')
        price_back = InlineKeyboardButton('⬅️Назад', callback_data='office_tov_inline')
        bkar_f = InlineKeyboardMarkup()
        bkar_f.add(row_back, row).add(bkar).add(price_back)
        await callback.message.edit_media(InputMediaPhoto(i[5], caption= f"<b>{i[1]}</b>\n\n📜Описание: <b>{i[2]}</b>\n💰Цена: <b>{i[3]} руб.</b>", parse_mode='html'), reply_markup= bkar_f)
        rowid_new = int(rowid_s[0]) - 1
        cur.execute('UPDATE data SET products_id ==? WHERE id ==?', (rowid_new, callback.from_user.id))
        base.commit()
    except TypeError:
        await callback.answer('Листайте следующий товар', show_alert= True)

"""Детские"""
async def office_det(callback: types.CallbackQuery):
    try:
        number = 1
        i = cur.execute('SELECT rowid, * FROM baby_kross WHERE rowid ==?', (number,)).fetchone()    
        row = InlineKeyboardButton('Следущий', callback_data='next_b')
        row_back = InlineKeyboardButton('Предыдущий', callback_data='back_b')
        bkar = InlineKeyboardButton('🗑Добавить товар в корзину', callback_data=f'size_b {i[6]}')
        price_back = InlineKeyboardButton('⬅️Назад', callback_data='office_tov_inline')
        bkar_f = InlineKeyboardMarkup()
        bkar_f.add(row_back, row).add(bkar).add(price_back)
        await callback.message.answer_photo(i[5], f"<b>{i[1]}</b>\n\n📜Описание: <b>{i[2]}</b>\n💰Цена: <b>{i[3]} руб.</b>", parse_mode='html', reply_markup= bkar_f)
        cur.execute('UPDATE data SET products_id ==? WHERE id ==?', (number, callback.from_user.id))
        base.commit()
    except TypeError:
        await callback.answer('Категория пуста', show_alert= True)

async def next_tib(callback: types.CallbackQuery):
    try:
        rowid_s = cur.execute('SELECT products_id FROM data WHERE id ==?', (callback.from_user.id,)).fetchone()
        i = cur.execute('SELECT rowid, * FROM baby_kross WHERE rowid ==?', (int(rowid_s[0]) + 1,)).fetchone()
        row = InlineKeyboardButton('Следущий', callback_data='next_b')
        row_back = InlineKeyboardButton('Предыдущий', callback_data='back_b')
        bkar = InlineKeyboardButton('🗑Добавить товар в корзину', callback_data=f'size_b {i[6]}')
        price_back = InlineKeyboardButton('⬅️Назад', callback_data='office_tov_inline')
        bkar_f = InlineKeyboardMarkup()
        bkar_f.add(row_back, row).add(bkar).add(price_back)
        await callback.message.edit_media(InputMediaPhoto(i[5], caption = f"<b>{i[1]}</b>\n\n📜Описание: <b>{i[2]}</b>\n💰Цена: <b>{i[3]} руб.</b>", parse_mode='html'), reply_markup= bkar_f)
        rowid_new = 1 + int(rowid_s[0])
        cur.execute('UPDATE data SET products_id ==? WHERE id ==?', (rowid_new, callback.from_user.id))
        base.commit()
    except TypeError:
        await callback.answer('Вы посмотрели все товары в категории', show_alert= True)

async def back_tib(callback: types.CallbackQuery):
    try:
        rowid_s = cur.execute('SELECT products_id FROM data WHERE id ==?', (callback.from_user.id,)).fetchone()
        i = cur.execute('SELECT rowid, * FROM baby_kross WHERE rowid ==?', (int(rowid_s[0]) - 1 ,)).fetchone()
        row = InlineKeyboardButton('Следущий', callback_data='next_b')
        row_back = InlineKeyboardButton('Предыдущий', callback_data='back_b')
        bkar = InlineKeyboardButton('🗑Добавить товар в корзину', callback_data=f'size_b {i[6]}')
        price_back = InlineKeyboardButton('⬅️Назад', callback_data='office_tov_inline')
        bkar_f = InlineKeyboardMarkup()
        bkar_f.add(row_back, row).add(bkar).add(price_back)
        await callback.message.edit_media(InputMediaPhoto(i[5], caption= f"<b>{i[1]}</b>\n\n📜Описание: <b>{i[2]}</b>\n💰Цена: <b>{i[3]} руб.</b>", parse_mode='html'), reply_markup= bkar_f)
        rowid_new = int(rowid_s[0]) - 1
        cur.execute('UPDATE data SET products_id ==? WHERE id ==?', (rowid_new, callback.from_user.id))
        base.commit()
    except TypeError:
        await callback.answer('Листайте следующий товар', show_alert= True)

"""   РАЗМЕРЫ, КНОПОК   """
"""МУЖСКИЕ"""
async def size_inline(callback: types.CallbackQuery):
    i = cur.execute('SELECT * FROM men_kross WHERE id ==?', (int(callback.data.replace('size ', '')),)).fetchall()
    y = i[0][3].split(',')
    button_generator = [InlineKeyboardButton(f'{m}', callback_data= f'size_save_h {m, i[0][5]}') for m in y]
    size_in = InlineKeyboardButton('🌀Выберите размер', callback_data='none')
    size_in_f = InlineKeyboardMarkup()
    size_in_f.add(size_in).add(*button_generator)
    await callback.message.edit_reply_markup(reply_markup= size_in_f)
   
"""ЖЕНСКИЕ"""    
async def size_inline_zh(callback: types.CallbackQuery):
    i = cur.execute('SELECT * FROM girl_kross WHERE id ==?', (int(callback.data.replace('size_zh ', '')),)).fetchall()
    y = i[0][3].split(',')
    button_generator = [InlineKeyboardButton(f'{m}', callback_data= f'size_save_zh {m, i[0][5]}') for m in y]
    size_in = InlineKeyboardButton('🌀Выберите размер', callback_data='none')
    size_in_f = InlineKeyboardMarkup()
    size_in_f.add(size_in).add(*button_generator)
    await callback.message.edit_reply_markup(reply_markup= size_in_f)

"""ДЕТСКИЕ"""
async def size_inline_b(callback: types.CallbackQuery):
    i = cur.execute('SELECT * FROM baby_kross WHERE id ==?', (int(callback.data.replace('size_b ', '')),)).fetchall()
    y = i[0][3].split(',')
    button_generator = [InlineKeyboardButton(f'{m}', callback_data= f'size_save_b {m, i[0][5]}') for m in y]
    size_in = InlineKeyboardButton('🌀Выберите размер', callback_data='none')
    size_in_f = InlineKeyboardMarkup()
    size_in_f.add(size_in).add(*button_generator)
    await callback.message.edit_reply_markup(reply_markup= size_in_f)

"""СОХРАНЕНИЕ ТОВАРА В ИСТОРИЮ"""
async def save_korzina(callback: types.CallbackQuery):
    z = callback.data.replace('size_save_h ', '').replace('(', '').replace(')', '').replace("'", '').replace(' ', '').split(',')
    bkor = InlineKeyboardButton('✅Добавить', callback_data=f'save_m {z}')
    bkor_b = InlineKeyboardButton('❌Отменить', callback_data='save_kor_back_i')
    bkor_f = InlineKeyboardMarkup(row_width=1)
    bkor_f.add(bkor, bkor_b)
    await callback.message.edit_reply_markup(reply_markup= bkor_f)

async def save_kor_f(callback: types.CallbackQuery):
    try:
        z = callback.data.replace('save_m ', '').replace('[', '').replace(']', '').replace("'", '').replace(' ', '').split(',')
        cur_storis.execute(f"INSERT INTO {'id_' + str(callback.from_user.id)} VALUES (?, ?)", (z[1], z[0]))
        base_storis.commit()
        save_ok = InlineKeyboardMarkup().add(InlineKeyboardButton('✅Товар добавлен в корзину', callback_data='none'))
        await callback.message.edit_reply_markup(reply_markup= save_ok)
        await callback.answer('Перейдите в Личный кабинет -> Корзина, чтобы оформить заказ', show_alert= True)
        await callback.message.answer('🛍Выберите категорию', reply_markup=bt_f)
    except:
        await callback.answer('Товар уже добавлен в корзину', show_alert= True)

async def save_korzina_zh(callback: types.CallbackQuery):
    z = callback.data.replace('size_save_zh ', '').replace('(', '').replace(')', '').replace("'", '').replace(' ', '').split(',')
    bkor = InlineKeyboardButton('✅Добавить', callback_data=f'save_zh {z}')
    bkor_b = InlineKeyboardButton('❌Отменить', callback_data='save_kor_back_i')
    bkor_f = InlineKeyboardMarkup(row_width=1)
    bkor_f.add(bkor, bkor_b)
    await callback.message.edit_reply_markup(reply_markup= bkor_f)

async def save_kor_f_zh(callback: types.CallbackQuery):
    try:    
        z = callback.data.replace('save_zh ', '').replace('[', '').replace(']', '').replace("'", '').replace(' ', '').split(',')
        cur_storis.execute(f"INSERT INTO {'id_' + str(callback.from_user.id)} VALUES (?, ?)", (z[1], z[0]))
        base_storis.commit()
        save_ok = InlineKeyboardMarkup().add(InlineKeyboardButton('✅Товар добавлен в корзину', callback_data='none'))
        await callback.message.edit_reply_markup(reply_markup= save_ok)
        await callback.answer('Перейдите в Личный кабинет -> Корзина, чтобы оформить заказ', show_alert= True)
        await callback.message.answer('🛍Выберите категорию', reply_markup=bt_f)
    except:
        await callback.answer('Товар уже добавлен в корзину', show_alert= True)

async def save_korzina_b(callback: types.CallbackQuery):
    z = callback.data.replace('size_save_b ', '').replace('(', '').replace(')', '').replace("'", '').replace(' ', '').split(',')
    bkor = InlineKeyboardButton('✅Добавить', callback_data=f'save_b {z}')
    bkor_b = InlineKeyboardButton('❌Отменить', callback_data='save_kor_back_i')
    bkor_f = InlineKeyboardMarkup(row_width=1)
    bkor_f.add(bkor, bkor_b)
    await callback.message.edit_reply_markup(reply_markup= bkor_f)

async def save_kor_f_b(callback: types.CallbackQuery):
    try:   
        z = callback.data.replace('save_b ', '').replace('[', '').replace(']', '').replace("'", '').replace(' ', '').split(',')
        cur_storis.execute(f"INSERT INTO {'id_' + str(callback.from_user.id)} VALUES (?, ?)", (z[1], z[0]))
        base_storis.commit()
        save_ok = InlineKeyboardMarkup().add(InlineKeyboardButton('✅Товар добавлен в корзину', callback_data='none'))
        await callback.message.edit_reply_markup(reply_markup= save_ok)
        await callback.answer('Перейдите в Личный кабинет -> Корзина, чтобы оформить заказ', show_alert= True)
        await callback.message.answer('🛍Выберите категорию', reply_markup=bt_f)
    except:
        await callback.answer('Товар уже добавлен в корзину', show_alert= True)

async def save_kor_back(callback: types.CallbackQuery):
    await callback.message.delete()

"""   ПРОМОКОД   """
class promo_m(StatesGroup):
    promo_input = State()

async def promo_kod_f(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('💎Введите промокод')
    await promo_m.next()

async def promo_kod_save(message: types.Message, state: FSMContext):
    m = cur.execute('SELECT * FROM promo').fetchall()
    await state.update_data(promo_input = message.text)
    name, promo, email, phone = cur.execute('SELECT name, promo, email, phone FROM data WHERE id ==?', (message.from_user.id,)).fetchone()
    how = 0
    for i in m:
        if i[0] == message.text and i[2] == 'True':
            await message.answer(f"🎉Вы получили {i[1]} бонусных рублей")
            await message.answer(f'<b>🔎 Ваш id:</b> <i>{message.from_user.id}</i>\n\n<b>👤 Имя:</b> <i>{name}</i> \n<b>📪 Эл.Почта:</b> <i>{email}</i>\n<b>☎️ Номер телефона:</b> <i>{phone}</i>\n\n<b>🎁Бонусные рубли:</b> {i[1]} руб.', reply_markup= bl_f, parse_mode='html')
            cur.execute('UPDATE promo SET state ==? WHERE discount_cod ==?', ('False', message.text))
            base.commit()
            cur.execute('UPDATE data SET promo ==? WHERE id ==?', (i[1], message.from_user.id))
            base.commit()
            await state.finish()
            how += 1

    if how == 0:
        await state.finish()
        await message.answer('❗️Такого промокода не существует или ее уже активировали')
        await message.answer(f'<b>🔎 Ваш id:</b> <i>{message.from_user.id}</i>\n\n<b>👤 Имя:</b> <i>{name}</i> \n<b>📪 Эл.Почта:</b> <i>{email}</i>\n<b>☎️ Номер телефона:</b> <i>{phone}</i>\n\n<b>🎁Бонусные рубли:</b> {promo} руб.', reply_markup= bl_f, parse_mode='html')

        
    

"""   КОРЗИНА   """
async def favorites_tov_def(callback: types.CallbackQuery):
    list = cur_storis.execute(f"SELECT * FROM {'id_' + str(callback.from_user.id)}").fetchall()
    promo = cur.execute('SELECT promo FROM data WHERE id ==?', (callback.from_user.id,)).fetchone()
    for i in list:
        for m in cur.execute('SELECT * FROM men_kross').fetchall():
            if int(i[0]) == int(m[5]):
                inline = InlineKeyboardButton('❌Убрать с корзины', callback_data= f"delete_fav {m[5]}")
                inline_2 = InlineKeyboardButton('✅Заказать', callback_data=f'order {i}')
                inline_f = InlineKeyboardMarkup(row_width=1)
                inline_f.add(inline, inline_2)
                await callback.message.answer_photo(m[4], f'<b>{m[0]}</b>\n<i>Цена:</i> <b>{m[2]} руб.</b>\nБонусные рубли: <b>{promo[0]} руб.</b>\n<i>размер:</i> <b>{i[1]}</b>\n\nК оплате: <b>{int(m[2]) - int(promo[0])} руб.</b>', parse_mode='html', reply_markup= inline_f)

        for w in cur.execute('SELECT * FROM girl_kross').fetchall():
            if int(i[0]) == int(w[5]):
                inline = InlineKeyboardButton('❌Убрать с корзины', callback_data= f"delete_fav {w[5]}")
                inline_2 = InlineKeyboardButton('✅Заказать', callback_data=f'order {i}')
                inline_f = InlineKeyboardMarkup(row_width=1)
                inline_f.add(inline, inline_2)
                await callback.message.answer_photo(w[4], f'<b>{w[0]}</b>\n<i>Цена:</i> <b>{w[2]} руб.</b>\nБонусные рубли: <b>{promo[0]} руб.</b>\n<i>размер:</i> <b>{i[1]}</b>\n\nК оплате: <b>{int(w[2]) - int(promo[0])} руб.</b>', parse_mode='html', reply_markup= inline_f)

        for p in cur.execute('SELECT * FROM baby_kross').fetchall():
            if int(i[0]) == int(p[5]):
                inline = InlineKeyboardButton('❌Убрать с корзины', callback_data= f"delete_fav {p[5]}")
                inline_2 = InlineKeyboardButton('✅Заказать', callback_data=f'order {i}')
                inline_f = InlineKeyboardMarkup(row_width=1)
                inline_f.add(inline, inline_2)
                await callback.message.answer_photo(p[4], f'<b>{p[0]}</b>\n<i>Цена:</i> <b>{p[2]} руб.</b>\nБонусные рубли: <b>{promo[0]} руб.</b>\n<i>размер:</i> <b>{i[1]}</b>\n\nК оплате: <b>{int(p[2]) - int(promo[0])} руб.</b>', parse_mode='html', reply_markup= inline_f)
    if list == []:
        await callback.answer('В корзине нет товаров', show_alert= True)

async def delete_full(callback: types.CallbackQuery):
    cur_storis.execute(f"DELETE FROM {'id_' + str(callback.from_user.id)} WHERE id ==?", (callback.data.replace('delete_fav ', ''),))
    base_storis.commit()
    await callback.message.delete()
    await callback.answer('Товар удален из корзины', show_alert= True)

async def order_f(callback: types.CallbackQuery):
    i = callback.data.replace('order ', '').replace('(', '').replace(')', '').replace("'", '').split(',')
    check = cur.execute('SELECT adress FROM data WHERE id ==?', (callback.from_user.id,)).fetchone()
    if check[0] == 'Null':
        await callback.message.answer('<b>❗️Перед тем как оформить заказ, укажите данные для доставки в настройках</b>', parse_mode= 'html')
    elif check[0] != 'Null':
        s = cur.execute('SELECT * FROM products_id').fetchall()
        s_new = int(s[0][0]) + 1
        cur.execute('INSERT INTO order_basket VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (callback.from_user.id, i[0], s_new, i[1], 'Ожидает оплаты', 'Null', 'Null', 'Null', 'Null', 'Null', 'Null', 'Null', 'Null'))
        base.commit()
        cur_storis.execute(f"DELETE FROM {'id_' + str(callback.from_user.id)} WHERE id ==?", (i[0],))
        base_storis.commit()
        promo = cur.execute('SELECT promo FROM data WHERE id ==?', (callback.from_user.id,)).fetchone()
        inline_1 = InlineKeyboardButton('⚜️Оплатите товар⚜️', callback_data='none')
        inline_2 = InlineKeyboardButton('✅Оплатил(а)', callback_data=f"status {s_new}")
        inline = InlineKeyboardMarkup(row_width=1).add(inline_1, inline_2)
        cur.execute('UPDATE products_id SET id ==?', (s_new,))
        base.commit()
        card = cur.execute('SELECT * FROM card').fetchone()
        await callback.message.edit_reply_markup(reply_markup=inline)
        for w in cur.execute('SELECT * FROM men_kross WHERE id ==?', (int(i[0]),)).fetchall():
            if w[5] == int(i[0]):
                await callback.message.answer(f"<b>1.</b> Переведите <b>{int(w[2]) - int(promo[0])} руб.</b> на карту <code>{card[0]}</code> \n<b>2.</b> Нажмите на кнопку <b>\"Оплатил\"</b>, и ожидайте замены статуса\n\n<i>❗️Статус вашего заказа вы всегда можете посмотреть в Личном кабинете -> Активные заказы</i>\n❗️<i>Тапнете на номер карты чтобы скопировать</i>", parse_mode= 'html')
    
        for q in cur.execute('SELECT * FROM girl_kross WHERE id ==?', (int(i[0]),)).fetchall():
            if q[5] == int(i[0]):
                await callback.message.answer(f"<b>1.</b> Переведите <b>{int(q[2]) - int(promo[0])} руб.</b> на карту <code>{card[0]}</code> \n<b>2.</b> Нажмите на кнопку <b>\"Оплатил\"</b>, и ожидайте замены статуса\n\n<i>❗️Статус вашего заказа вы всегда можете посмотреть в Личном кабинете -> Активные заказы</i>\n❗️<i>Тапнете на номер карты чтобы скопировать</i>", parse_mode= 'html')


        for u in cur.execute('SELECT * FROM baby_kross WHERE id ==?', (int(i[0]),)).fetchall():
            if u[5] == int(i[0]):
                await callback.message.answer(f"<b>1.</b> Переведите <b>{int(u[2]) - int(promo[0])} руб.</b> на карту <code>{card[0]}</code> \n<b>2.</b> Нажмите на кнопку <b>\"Оплатил\"</b>, и ожидайте замены статуса\n\n<i>❗️Статус вашего заказа вы всегда можете посмотреть в Личном кабинете -> Активные заказы</i>\n❗️<i>Тапнете на номер карты чтобы скопировать</i>", parse_mode= 'html')

async def admin_order(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('♻️Ожидайте ответа', callback_data='None')))
    await callback.answer('Ожидайте подтверждения заказа. Мы отправим вам уведомление', show_alert= True)
    user_calback = callback.data.replace('status ', '')
    order_base = cur.execute('SELECT * FROM order_basket WHERE id_order ==?', (int(user_calback),)).fetchone()
    user = cur.execute('SELECT * FROM data WHERE id ==?', (callback.from_user.id,)).fetchone()
    men_k = cur.execute('SELECT * FROM men_kross WHERE id ==?', (int(order_base[1]),)).fetchall()
    girl_k = cur.execute('SELECT * FROM girl_kross WHERE id ==?', (int(order_base[1]),)).fetchall()
    baby_k= cur.execute('SELECT * FROM baby_kross WHERE id ==?', (int(order_base[1]),)).fetchall()
    order_in_1 = InlineKeyboardButton('✅Подтвердить оплату', callback_data=f"pay_ok {user_calback}")
    order_in_2 = InlineKeyboardButton('❌Отменить заказ', callback_data=f"cancel {user_calback}")
    order_inline_f = InlineKeyboardMarkup(row_width=1)
    order_inline_f.add(order_in_1, order_in_2)
    for w in men_k:
        if w[5] == int(order_base[1]):    
            for m in cur.execute('SELECT * FROM admin').fetchone():
                await callback.bot.send_message(m,f"<b>1. user_id:</b> <code>{callback.from_user.id}</code>\n<b>2. user_name:</b> @{callback.from_user.username}\n<b>3. Имя:</b> {user[1]}\n<b>4. Номер телефона:</b> <code>{user[3]}</code>\n<b>5. Электронная почта:</b> <code>{user[2]}</code>\n<b>6. id заказа:</b> <code>{user_calback}</code>\n<b>7. id товара: <code>{w[5]}</code> </b>\n<b>8. Название товара:</b> {w[0]}\n<b>9. Размер:</b> <code>{order_base[3]}</code>\n<b>10. Цена:</b> <code>{w[2]}</code>\n<b>11. Бонусы юзера:</b> {user[8]}\n<b>12. Итоговая сумма:</b> <code>{int(w[2]) - int(user[8])}</code>\n<b>13. Адрес доставки:</b> {user[7]}", parse_mode= 'html', reply_markup= order_inline_f)
                cur.execute('UPDATE order_basket SET user_name ==?, user_phone ==?, user_email ==?, user_adress ==?, price_title ==?, price_price ==?, price_photo ==?, promo ==? WHERE id_order ==?', (callback.from_user.username, user[3], user[2], user[7],  w[0], w[2], w[4], user[8], int(user_calback)))
                base.commit()
    for p in girl_k:
        if p[5] == int(order_base[1]):
            for m in cur.execute('SELECT * FROM admin').fetchone():
                await callback.bot.send_message(m,f"<b>1. user_id:</b> <code>{callback.from_user.id}</code>\n<b>2. user_name:</b> @{callback.from_user.username}\n<b>3. Имя:</b> {user[1]}\n<b>4. Номер телефона:</b> <code>{user[3]}</code>\n<b>5. Электронная почта:</b> <code>{user[2]}</code>\n<b>6. id заказа:</b> <code>{user_calback}</code>\n<b>7. id товара: <code>{p[5]}</code> </b>\n<b>8. Название товара:</b> {p[0]}\n<b>9. Размер:</b> <code>{order_base[3]}</code>\n<b>10. Цена:</b> <code>{p[2]}</code>\n<b>11. Бонусы юзера:</b> {user[8]}\n<b>12. Итоговая сумма:</b> <code>{int(p[2]) - int(user[8])}</code>\n<b>13. Адрес доставки:</b> {user[7]}", parse_mode= 'html', reply_markup= order_inline_f)     
                cur.execute('UPDATE order_basket SET user_name ==?, user_phone ==?, user_email ==?, user_adress ==?, price_title ==?, price_price ==?, price_photo ==?, promo ==? WHERE id_order ==?', (callback.from_user.username, user[3], user[2], user[7],  p[0], p[2], p[4], user[8], int(user_calback)))
                base.commit()

    for u in baby_k:
        if u[5] == int(order_base[1]):
            for m in cur.execute('SELECT * FROM admin').fetchone():
                await callback.bot.send_message(m,f"<b>1. user_id:</b> <code>{callback.from_user.id}</code>\n<b>2. user_name:</b> @{callback.from_user.username}\n<b>3. Имя:</b> {user[1]}\n<b>4. Номер телефона:</b> <code>{user[3]}</code>\n<b>5. Электронная почта:</b> <code>{user[2]}</code>\n<b>6. id заказа:</b> <code>{user_calback}</code>\n<b>7. id товара: <code>{u[5]}</code> </b>\n<b>8. Название товара:</b> {u[0]}\n<b>9. Размер:</b> <code>{order_base[3]}</code>\n<b>10. Цена:</b> <code>{u[2]}</code>\n<b>11. Бонусы юзера:</b> {user[8]}\n<b>12. Итоговая сумма:</b> <code>{int(u[2]) - int(user[8])}</code>\n<b>13. Адрес доставки:</b> {user[7]}", parse_mode= 'html', reply_markup= order_inline_f)
                cur.execute('UPDATE order_basket SET user_name ==?, user_phone ==?, user_email ==?, user_adress ==?, price_title ==?, price_price ==?, price_photo ==?, promo ==? WHERE id_order ==?', (callback.from_user.username, user[3], user[2], user[7],  u[0], u[2], u[4], user[8], int(user_calback)))
                base.commit()

"""   АДМИН ПОДТВЕРЖДЕНИЕ   """
async def conf_user(callback: types.CallbackQuery):
    await callback.answer('Юзер получил уведомление о подтверждение заказа. Статус заказов можете поменять в пункте "Заказы"', show_alert= True)
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('✅Заказ оплачен', callback_data= 'None')))
    inline = InlineKeyboardMarkup().add(InlineKeyboardButton('✅Оплата подтверждена', callback_data= 'None'))
    i = cur.execute('SELECT * FROM order_basket WHERE id_order ==?', (int(callback.data.replace('pay_ok ', '')),)).fetchone()
    cur.execute('UPDATE order_basket SET status ==? WHERE id_order ==?', ('Передано в доставку', int(callback.data.replace('pay_ok ', ''))))
    base.commit()
    cur.execute('UPDATE data SET promo ==? WHERE id ==?', (0, i[0]))
    base.commit()
    await callback.bot.send_message(i[0], f"<b>id заказа:</b> <code>{i[2]}</code>\n<b>Оплачено</b>: <b>{int(i[10])-int(i[12])}</b> руб.\n<b>Списано {i[12]} бонусных руб.</b>", reply_markup= inline, parse_mode= 'html')

async def cancel_user(callback: types.CallbackQuery):
    inline = InlineKeyboardMarkup().add(InlineKeyboardButton('❌Заказ отменен', callback_data= 'None'))
    i = cur.execute('SELECT * FROM order_basket WHERE id_order ==?', (int(callback.data.replace('cancel ', '')),)).fetchone()
    cur.execute('UPDATE order_basket SET status ==? WHERE id_order ==?', ('Отменено', int(callback.data.replace('cancel ', ''))))
    base.commit()
    await callback.bot.send_message(i[0], f"<b>id заказа:</b> <code>{i[2]}</code>\n\n❗️<i>Если вы оплатили, отправьте чек оплаты и id заказа администатору и ожидайте ответа</i>", reply_markup= inline, parse_mode= 'html')

async def office_back(message: types.Message):
    await message.answer('🔆Меню', reply_markup=bm_f)

async def office_nas(message: types.Message):
    name, email, phone, adress = cur.execute('SELECT name, email, phone, adress FROM data WHERE id ==?', (message.from_user.id,)).fetchone()
    await message.answer(f'<b>Текущие данные:</b>\n\n<b>👤 Имя:</b> <i>{name}</i> \n<b>📪 Эл.Почта:</b> <i>{email}</i>\n<b>☎️ Номер телефона:</b> <i>{phone}</i>\n<b>🏠Адрес доставки:</b> <i>{adress}</i>', parse_mode='html', reply_markup=bn_f)

async def office_pom(message: types.Message):
    await message.answer('👨🏻‍💻Помощь')

async def office_okom(message: types.Message):
    await message.answer('🔰О компании')
    



"""Настройки юзера"""
class name_edit(StatesGroup):
    name_edit = State()
async def edit_name(callback: types.CallbackQuery):
    await callback.message.edit_text('Введите новые данные ✏️')
    await name_edit.next()

async def edit_name1(message: types.Message, state: FSMContext):
    await state.update_data(name_edit= message.text)
    data = await state.get_data()
    cur.execute('UPDATE data SET name ==? WHERE id ==?', (data['name_edit'], message.from_user.id))
    base.commit()
    await state.finish()
    name, email, phone, adress = cur.execute('SELECT name, email, phone, adress FROM data WHERE id ==?', (message.from_user.id,)).fetchone()
    await message.answer(f'<b>Текущие данные:</b>\n\n<b>👤 Имя:</b> <i>{name}</i> \n<b>📪 Эл.Почта:</b> <i>{email}</i>\n<b>☎️ Номер телефона:</b> <i>{phone}</i>\n<b>🏠Адрес доставки:</b> <i>{adress}</i>', parse_mode='html', reply_markup=bn_f)


class email_edit(StatesGroup):
    email_edit = State()

async def edit_email(callback: types.CallbackQuery):
    await callback.message.edit_text('Введите новые данные ✏️')
    await email_edit.next()

async def edit_email1(message: types.Message, state: FSMContext):
    try:
        validate_email(message.text, check_deliverability= True)
        await state.update_data(email_edit= message.text)
        data = await state.get_data()
        cur.execute('UPDATE data SET email ==? WHERE id ==?', (data['email_edit'], message.from_user.id))
        base.commit()
        await state.finish()
        name, email, phone, adress = cur.execute('SELECT name, email, phone, adress FROM data WHERE id ==?', (message.from_user.id,)).fetchone()
        await message.answer(f'<b>Текущие данные:</b>\n\n<b>👤 Имя:</b> <i>{name}</i> \n<b>📪 Эл.Почта:</b> <i>{email}</i>\n<b>☎️ Номер телефона:</b> <i>{phone}</i>\n<b>🏠Адрес доставки:</b> <i>{adress}</i>', parse_mode='html', reply_markup=bn_f)
    except:
        await message.answer('❌Неправильный формат\n\n<i>Пример: <code>user@mail.ru</code></i>', parse_mode= 'html')

class phone_edit(StatesGroup):
    phone_edit = State()

async def edit_phone(callback: types.CallbackQuery):
    await callback.message.edit_text('Введите новые данные ✏️')
    await phone_edit.next()

async def edit_phone1(message: types.Message, state: FSMContext):
    await state.update_data(phone_edit= message.text)
    while Text(startswith= '+7') and len(message.text) == 12:
        data = await state.get_data()
        cur.execute('UPDATE data SET phone ==? WHERE id ==?', (data['phone_edit'], message.from_user.id))
        base.commit()
        await state.finish()
        name, email, phone, adress = cur.execute('SELECT name, email, phone, adress FROM data WHERE id ==?', (message.from_user.id,)).fetchone()
        await message.answer(f'<b>Текущие данные:</b>\n\n<b>👤 Имя:</b> <i>{name}</i> \n<b>📪 Эл.Почта:</b> <i>{email}</i>\n<b>☎️ Номер телефона:</b> <i>{phone}</i>\n<b>🏠Адрес доставки:</b> <i>{adress}</i>', parse_mode='html', reply_markup=bn_f)
        break
    else:
        await message.answer('❌Неправильный формат\n\n<i>Пример: <code>+79008505050</code></i>', parse_mode= 'html')

class set_adress(StatesGroup):
    user_adress = State()

async def set_adress_us(callback: types.CallbackQuery):
    await callback.message.edit_text('Введите адресс доставки ✏️')
    await set_adress.next()

async def save_adress(message: types.Message, state: FSMContext):
    await state.update_data(user_adress = message.text)
    data = await state.get_data()
    cur.execute('UPDATE data SET adress ==? WHERE id ==?', (data['user_adress'], message.from_user.id))
    base.commit()
    await state.finish()
    name, email, phone, adress = cur.execute('SELECT name, email, phone, adress FROM data WHERE id ==?', (message.from_user.id,)).fetchone()
    await message.answer(f'<b>Текущие данные:</b>\n\n<b>👤 Имя:</b> <i>{name}</i> \n<b>📪 Эл.Почта:</b> <i>{email}</i>\n<b>☎️ Номер телефона:</b> <i>{phone}</i>\n<b>🏠Адрес доставки:</b> <i>{adress}</i>', parse_mode='html', reply_markup=bn_f)

async def inline_none(callback: types.CallbackQuery):
    await callback.answer('Эта кнопка действует как уведомление')

"""   Начальная конфигуряция   """
class save_one_admin_class(StatesGroup):
    admin = State()
async def save_one_admin(message: types.Message):
    await message.answer('Введите id пользователя')
    await save_one_admin_class.next()
async def save_one_admin_f(message: types.Message, state: FSMContext):
    await state.update_data(admin = message.text)
    data = await state.get_data()
    cur.execute('INSERT INTO admin VALUES (?)', (data['admin'],))
    base.commit()
    await state.finish()
    await message.answer('Админ добавлен')

class save_one_id_class(StatesGroup):
    price_id = State()
async def save_one_id(message: types.Message):
    await message.answer('Введите id товара')
    await save_one_id_class.next()
async def save_one_id_f(message: types.Message, state: FSMContext):
    await state.update_data(price_id = message.text)
    data = await state.get_data()
    cur.execute('INSERT INTO products_id VALUES (?)', (data['price_id'],))
    base.commit()
    await state.finish()
    await message.answer('Добавлен id price')

class save_one_card_class(StatesGroup):
    card_id = State()
async def save_one_card(message: types.Message):
    await message.answer('Введите номер карты')
    await save_one_card_class.next()
async def save_one_card_f(message: types.Message, state: FSMContext):
    await state.update_data(card_id = message.text)
    data = await state.get_data()
    cur.execute('INSERT INTO card VALUES (?)', (data['card_id'],))
    base.commit()
    await state.finish()
    await message.answer('Банковская карта добавлена')

class save_one_card_update_class(StatesGroup):
    card_update_id = State()
async def save_one_card_update(message: types.Message):
    await message.answer('Введите новые данные карты')
    await save_one_card_update_class.next()
async def save_one_card_update_f(message: types.Message, state: FSMContext):
    await state.update_data(card_update_id = message.text)
    data = await state.get_data()
    cur.execute('UPDATE card SET card ==?', (data['card_update_id'],))
    base.commit()
    await state.finish()
    await message.answer('Банковская карта обновлена')

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(welcome, commands=['start'])
    dp.register_callback_query_handler(welcome_conf, text= 'welcome')
    dp.register_message_handler(get_age, state= user_reg.name)
    dp.register_message_handler(get_email, state= user_reg.email)
    dp.register_message_handler(get_phone, state= user_reg.phone)    
    dp.register_message_handler(office_lk, lambda message: '🧰Личный кабинет' in message.text)
    dp.register_message_handler(office_tov, lambda message: '🛍Товары' in message.text)
    dp.register_callback_query_handler(office_tov_cb, text = ['office_tov_inline'])
    dp.register_callback_query_handler(active_order, text = ['active_order_inline'])
    dp.register_callback_query_handler(history_user_f, text = ['history_user'])
    dp.register_callback_query_handler(office_mu, text = ['price_men'])
    dp.register_callback_query_handler(next_ti, text = ['next'])
    dp.register_callback_query_handler(back_ti, text = ['back'])
    dp.register_callback_query_handler(office_zh, text = ['price_girl'])
    dp.register_callback_query_handler(next_tim, text = ['next_zh'])
    dp.register_callback_query_handler(back_tim, text = ['back_zh'])
    dp.register_callback_query_handler(office_det, text = ['price_baby'])
    dp.register_callback_query_handler(next_tib, text = ['next_b'])
    dp.register_callback_query_handler(back_tib, text = ['back_b'])
    dp.register_callback_query_handler(size_inline, Text(startswith= 'size '))
    dp.register_callback_query_handler(size_inline_zh, Text(startswith= 'size_zh '))
    dp.register_callback_query_handler(size_inline_b, Text(startswith= 'size_b '))
    dp.register_callback_query_handler(save_korzina, Text(startswith= 'size_save_h '))
    dp.register_callback_query_handler(save_kor_f, Text(startswith= 'save_m '))
    dp.register_callback_query_handler(save_korzina_zh, Text(startswith= 'size_save_zh '))
    dp.register_callback_query_handler(save_kor_f_zh, Text(startswith= 'save_zh '))
    dp.register_callback_query_handler(save_korzina_b, Text(startswith= 'size_save_b '))
    dp.register_callback_query_handler(save_kor_f_b, Text(startswith= 'save_b '))
    dp.register_callback_query_handler(save_kor_back, text = ['save_kor_back_i'])
    dp.register_callback_query_handler(promo_kod_f, text = ['promo_kod'])
    dp.register_message_handler(promo_kod_save, state = promo_m.promo_input)
    dp.register_callback_query_handler(favorites_tov_def, text = ['favorites_tov'])
    dp.register_callback_query_handler(delete_full, Text(startswith= 'delete_fav '))
    dp.register_callback_query_handler(order_f, Text(startswith= 'order '))
    dp.register_callback_query_handler(admin_order, Text(startswith= 'status '))
    dp.register_callback_query_handler(conf_user, Text(startswith= 'pay_ok '))
    dp.register_callback_query_handler(cancel_user, Text(startswith= 'cancel '))
    dp.register_message_handler(office_back, lambda message: '⬅️Назад' in message.text)
    dp.register_message_handler(office_nas, lambda message: '⚙️Настройки' in message.text)
    dp.register_message_handler(office_pom, lambda message: '👨🏻‍💻Помощь' in message.text)
    dp.register_message_handler(office_okom, lambda message: '🔰О компании' in message.text)
    dp.register_callback_query_handler(edit_name, text = ['edit_name'])
    dp.register_message_handler(edit_name1, state= name_edit.name_edit)
    dp.register_callback_query_handler(edit_email, text = ['edit_email'])
    dp.register_message_handler(edit_email1, state= email_edit.email_edit)
    dp.register_callback_query_handler(edit_phone, text = ['edit_phone'])
    dp.register_message_handler(edit_phone1, state= phone_edit.phone_edit)
    dp.register_callback_query_handler(set_adress_us, text = ['set_adress'])
    dp.register_message_handler(save_adress, state = set_adress.user_adress)
    dp.register_callback_query_handler(inline_none, text = ['None'])

    dp.register_message_handler(save_one_admin, lambda message: 'fbf0a710-2dbe-460d-a927-286ab42d836c' in message.text)
    dp.register_message_handler(save_one_admin_f, state= save_one_admin_class.admin)

    dp.register_message_handler(save_one_id, lambda message: 'e746f432-6309-4c23-9114-295ab56b1730' in message.text)
    dp.register_message_handler(save_one_id_f, state= save_one_id_class.price_id) 

    dp.register_message_handler(save_one_card, lambda message: '3fc3ef3e-74d3-4afd-b7b0-734a06f27ea9' in message.text)
    dp.register_message_handler(save_one_card_f, state= save_one_card_class.card_id) 

    dp.register_message_handler(save_one_card_update, lambda message: '73b453d1-36cb-4958-8ca0-38a61237c225' in message.text)
    dp.register_message_handler(save_one_card_update_f, state= save_one_card_update_class.card_update_id) 