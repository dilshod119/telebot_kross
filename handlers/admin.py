from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import  FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
import sqlite3
from keyboards.admin_kb import bm_f, bt_f, bp_f, bz_f, br_f, bpromo_f, bkey_f, bti_f

base = sqlite3.connect('base.db')
cur = base.cursor()

async def admin_panel(message: types.Message):
    global base, cur
    id = cur.execute('SELECT * FROM admin').fetchall()
    for i in id:
        for r in i:
            if r == str(message.from_user.id):
                await message.answer('Админ панель', reply_markup=bm_f)
            elif r != str(message.from_user.id):
                await message.answer('❌У вас нет доступа к админ-панел')


"""   РАЗДЕЛЫ   """
async def office_t(message: types.Message):
    await message.answer('📦Товары', reply_markup=bt_f)

async def office_p(message: types.Message):   
    await message.answer('👥Пользователи', reply_markup=bp_f)

async def office_z(message: types.Message):    
    await message.answer('🛍Заказы', reply_markup=bz_f)

async def new_order_f(callback: types.CallbackQuery):
    i = cur.execute('SELECT * FROM order_basket').fetchall()
    how = 0
    for n in i:
        if n[4] == 'Ожидает оплаты':
            order_in_1 = InlineKeyboardButton('✅Подтвердить оплату', callback_data= f"pay_ok_admin {n[2]}")
            order_in_2 = InlineKeyboardButton('❌Отменить заказ', callback_data= f"cancel_admin {n[2]}")
            order_inline_f = InlineKeyboardMarkup(row_width=1)
            order_inline_f.add(order_in_1, order_in_2)
            await callback.message.answer_photo(n[11],f"<b>1. user_id:</b> <code>{n[0]}</code>\n<b>2. user_name:</b> @{n[5]}\n<b>4. Номер телефона:</b> <code>{n[6]}</code>\n<b>5. Электронная почта:</b> <code>{n[7]}</code>\n<b>6. id заказа:</b> <code>{n[2]}</code>\n<b>7. id товара: <code>{n[1]}</code> </b>\n<b>8. Название товара:</b> {n[9]}\n<b>9. Размер:</b> {n[3]}\n<b>10. Цена:</b> <code>{n[10]}</code> руб.\n<b>11. Бонусы юзера:</b> <code>{n[12]}</code> руб.\n<b>12. Итоговая сумма:</b> <code>{int(n[10]) - int(n[12])}</code> руб.\n<b>13. Адрес доставки:</b> {n[8]}", parse_mode= 'html', reply_markup= order_inline_f)
            how += 1
    if how == 0:
        await callback.answer('🔎Категория пуста', show_alert= True)

async def delivery_full(callback: types.CallbackQuery):
    i = cur.execute('SELECT * FROM order_basket').fetchall()
    how = 0
    for n in i:
        if n[4] == 'Передано в доставку':
            inl = InlineKeyboardMarkup().add(InlineKeyboardButton('✅Товар доставлен', callback_data=f"delivery_commit_in {n[2]}"))
            await callback.message.answer_photo(n[11],f"<b>1. user_id:</b> <code>{n[0]}</code>\n<b>2. user_name:</b> @{n[5]}\n<b>4. Номер телефона:</b> <code>{n[6]}</code>\n<b>5. Электронная почта:</b> <code>{n[7]}</code>\n<b>6. id заказа:</b> <code>{n[2]}</code>\n<b>7. id товара: <code>{n[1]}</code> </b>\n<b>8. Название товара:</b> {n[9]}\n<b>9. Размер:</b> {n[3]}\n<b>10. Цена:</b> <code>{n[10]}</code> руб.\n<b>11. Бонусы юзера:</b> <code>{n[12]}</code> руб.\n<b>12. Итоговая сумма:</b> <code>{int(n[10]) - int(n[12])}</code> руб.\n<b>13. Адрес доставки:</b> {n[8]}", parse_mode= 'html', reply_markup= inl)
            how += 1
    if how == 0:
        await callback.answer('🔎Категория пуста', show_alert= True)

async def completed_full(callback: types.CallbackQuery):
    i = cur.execute('SELECT * FROM order_basket').fetchall()
    how = 0
    for n in i:
        if n[4] == 'Доставлено':
            inline = InlineKeyboardMarkup().add(InlineKeyboardButton('☑️Завершено', callback_data='None'))
            await callback.message.answer_photo(n[11],f"<b>1. user_id:</b> <code>{n[0]}</code>\n<b>2. user_name:</b> @{n[5]}\n<b>4. Номер телефона:</b> <code>{n[6]}</code>\n<b>5. Электронная почта:</b> <code>{n[7]}</code>\n<b>6. id заказа:</b> <code>{n[2]}</code>\n<b>7. id товара: <code>{n[1]}</code> </b>\n<b>8. Название товара:</b> {n[9]}\n<b>9. Размер:</b> {n[3]}\n<b>10. Цена:</b> <code>{n[10]}</code> руб.\n<b>11. Бонусы юзера:</b> <code>{n[12]}</code> руб.\n<b>12. Итоговая сумма:</b> <code>{int(n[10]) - int(n[12])}</code> руб.\n<b>13. Адрес доставки:</b> {n[8]}", parse_mode= 'html', reply_markup= inline)            
            how += 1
    if how == 0:
        await callback.answer('🔎Категория пуста', show_alert= True)

async def cancellation_full(callback: types.CallbackQuery):
    i = cur.execute('SELECT * FROM order_basket').fetchall()
    how = 0
    for n in i:
        if n[4] == 'Отменено':
            inline = InlineKeyboardMarkup().add(InlineKeyboardButton('❌Отменено', callback_data='None'))
            await callback.message.answer_photo(n[11],f"<b>1. user_id:</b> <code>{n[0]}</code>\n<b>2. user_name:</b> @{n[5]}\n<b>4. Номер телефона:</b> <code>{n[6]}</code>\n<b>5. Электронная почта:</b> <code>{n[7]}</code>\n<b>6. id заказа:</b> <code>{n[2]}</code>\n<b>7. id товара: <code>{n[1]}</code> </b>\n<b>8. Название товара:</b> {n[9]}\n<b>9. Размер:</b> {n[3]}\n<b>10. Цена:</b> <code>{n[10]}</code> руб.\n<b>11.Бонусы юзера:</b> <code>{n[12]}</code> руб.\n<b>12.Итоговая сумма:</b> <code>{int(n[10]) - int(n[12])}</code> руб.\n<b>11. Адрес доставки:</b> {n[8]}", parse_mode= 'html', reply_markup= inline)
            how += 1
    if how == 0:
        await callback.answer('🔎Категория пуста', show_alert= True)

"""   ПОДТВЕРЖДЕНИЕ В НОВЫХ ЗАЯВКАХ   """
async def conf_user_admin(callback: types.CallbackQuery):
    inline = InlineKeyboardMarkup().add(InlineKeyboardButton('✅Оплата подтверждена', callback_data= 'None'))
    i = cur.execute('SELECT * FROM order_basket WHERE id_order ==?', (int(callback.data.replace('pay_ok_admin ', '')),)).fetchone()
    cur.execute('UPDATE order_basket SET status ==? WHERE id_order ==?', ('Передано в доставку', int(callback.data.replace('pay_ok_admin ', ''))))
    base.commit()
    await callback.bot.send_message(i[0], f"<b>id заказа:</b> <code>{i[2]}</code>\n<b>Оплачено</b>: <b>{i[10]}</b> руб.", reply_markup= inline, parse_mode= 'html')

async def cancel_user_admin(callback: types.CallbackQuery):
    inline = InlineKeyboardMarkup().add(InlineKeyboardButton('❌Заказ отменен', callback_data= 'None'))
    i = cur.execute('SELECT * FROM order_basket WHERE id_order ==?', (int(callback.data.replace('cancel_admin ', '')),)).fetchone()
    cur.execute('UPDATE order_basket SET status ==? WHERE id_order ==?', ('Отменено', int(callback.data.replace('cancel_admin ', ''))))
    base.commit()
    await callback.bot.send_message(i[0], f"<b>id заказа:</b> <code>{i[2]}</code>\n\n❗️<i>Если вы оплатили, отправьте чек оплаты и id заказа администатору и ожидайте ответа</i>", reply_markup= inline, parse_mode= 'html')

"""   ПОДТВЕРЖДЕНИЕ В ПЕРЕДАНО В ДОСТАВКУ   """
async def delivery_commit(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('✅Сделка закрыта', callback_data='None')))
    await callback.answer('Отправлено уведомление юзеру', show_alert= True)
    # await callback.message.delete()
    i = cur.execute('SELECT * FROM order_basket WHERE id_order ==?', (int(callback.data.replace('delivery_commit_in ', '')),)).fetchone()
    cur.execute('UPDATE order_basket SET status ==? WHERE id_order ==?', ('Доставлено', int(callback.data.replace('delivery_commit_in ', ''))))
    base.commit()
    await callback.bot.send_message(i[0], '🚚Товар успешно доставлен')

async def office_r(message: types.Message):    
    await message.answer('📨Рассылка', reply_markup=br_f)

"""   РАССЫЛКА НА БОТА   """
class mail_bot(StatesGroup):
    message_mail = State()

async def maili_bot_f(callback: types.CallbackQuery):
    await callback.message.answer('Введите сообщение')
    await mail_bot.next()

async def mail_bot_answer(message: types.Message, state: FSMContext):
    await state.update_data(message_mail = message.text)
    data = await state.get_data()
    y = cur.execute('SELECT id FROM data').fetchall()
    try:   
        for i in y:
            await message.bot.send_message(i[0], f"{data['message_mail']}")
    except:
        pass
    await state.finish()

"""   ПРОМОКОДЫ   """
async def office_pro(message: types.Message):   
    await message.answer('🎁Промокод', reply_markup=bpromo_f)

class promo_m(StatesGroup):
    promo_title = State()
    promo_price = State()

async def promo_admin_full(callback: types.CallbackQuery):
    await callback.message.answer('Ведите название промокода ✏️')
    await promo_m.next()

async def promo_title(message: types.Message, state: FSMContext):
    await state.update_data(promo_title = message.text)
    await message.answer('💰 На какую сумму будет промокод?')
    await promo_m.next()

async def promo_price(message: types.Message, state: FSMContext):
    await state.update_data(promo_price = message.text)
    try:
        int(message.text)
        data = await state.get_data()
        cur.execute('INSERT INTO promo VALUES (?, ?, ?)', (data['promo_title'], data['promo_price'], 'True'))
        base.commit()
        await message.answer(f"💎Выпущен промокод <code>{data['promo_title']}</code> на сумму <b>{data['promo_price']} руб.</b>", parse_mode='html', reply_markup=bm_f)
        await state.finish()
    except ValueError:
        await message.answer('❌Неверное значение. Введите численное значение')

    
async def office_s(message: types.Message):
    user = cur.execute('SELECT rowid FROM data').fetchall()
    order = cur.execute('SELECT * FROM order_basket').fetchall()
    order_unpaid = 0
    order_delivered = 0
    order_completed = 0
    order_cancel = 0
    for i in order:
        if i[4] == 'Ожидает оплаты':
            order_unpaid += 1
        elif i[4] == 'Передано в доставку':
            order_delivered += 1
        elif i[4] == 'Доставлено':
            order_completed += 1
        elif i[4] == 'Отменено':
            order_cancel += 1
 
    await message.answer(f"📊Статистика\n<b>Пользователей в боте:</b> {user[-1][0]}\n\n<b>---Заказы---</b> \n<b>Неоплаченных:</b> {order_unpaid}\n<b>Доставляются:</b> {order_delivered}\n<b>Завершенных:</b> {order_completed}\n<b>Отмененных:</b> {order_cancel}", parse_mode= 'html')
    


"""   ДОБАВЛЕНИЕ ТОВАРА   """
class add_product(StatesGroup):
    title = State()
    description = State()
    price = State()
    size = State()
    photo = State()
    floor = State()

async def add_product_1(callback: types.CallbackQuery):
    await callback.message.edit_text('Введите название товара ✏️')
    await add_product.next()

async def title_add(message: types.Message, state: FSMContext):
    await state.update_data(title = message.text)
    await message.answer('📄 Введите описание товара ')
    await add_product.next()

async def description_add(message: types.Message, state: FSMContext):
    await state.update_data(description = message.text)
    await message.answer('💰 Укажите цену товара')
    await add_product.next()

async def price_add(message: types.Message, state: FSMContext):
    await state.update_data(price= message.text)
    try:
        int(message.text)
        await message.answer('Укажите размер кроссовки через запятую')
        await add_product.next()
    except ValueError:
        await message.answer('❌Неправильный формат. Введите численное значение')

async def size_add(message: types.Message, state: FSMContext):
    await state.update_data(size = message.text)
    await message.answer('📷 Отправьте фотографию товара')
    await add_product.next()

async def photo_add(message: types.Message, state: FSMContext):
    await state.update_data(photo= message.photo[0].file_id)
    await message.answer('Укажите пол', reply_markup= bkey_f)
    await add_product.next()

async def floor(message: types.Message, state: FSMContext):
    await state.update_data(floor = message.text)
    data = await state.get_data()
    s = cur.execute('SELECT * FROM products_id').fetchall()
    s_new = int(s[0][0]) + 1
    if data['floor'] == '👨🏻Мужское':
        cur.execute('INSERT INTO men_kross VALUES (?, ?, ?, ?, ?, ?)', (data['title'], data['description'], data['price'], data['size'], data['photo'], s_new))
        base.commit()
        await message.answer('Cохранил в мужское', reply_markup= bm_f)
    elif data['floor'] == '👩🏻‍🦰Женское':
        cur.execute('INSERT INTO girl_kross VALUES (?, ?, ?, ?, ?, ?)', (data['title'], data['description'], data['price'], data['size'], data['photo'], s_new))
        base.commit()
        await message.answer('Cохранил в женское', reply_markup= bm_f)
    elif data['floor'] == '👦🏻Детское':
        cur.execute('INSERT INTO baby_kross VALUES (?, ?, ?, ?, ?, ?)', (data['title'], data['description'], data['price'], data['size'], data['photo'], s_new))
        base.commit()
        await message.answer('Cохранил в детское', reply_markup= bm_f)
    cur.execute('UPDATE products_id SET id ==?', (s_new,))
    base.commit()
    await state.finish()

"""   РЕДАКТИРОВАТЬ ЗАКАЗ   """
async def edit_product_1(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите раздел', reply_markup= bti_f)

async def edit_product_men_1(callback: types.CallbackQuery):
    for i in cur.execute('SELECT * FROM men_kross').fetchall():
        btr_1 = InlineKeyboardButton('🗑Удалить товар', callback_data=f"del {i[5]}")
        btr_f = InlineKeyboardMarkup()
        btr_f.add(btr_1)
        await callback.message.answer_photo(i[4], f"<b>{i[0]}</b>\n\n📜Описание: <b>{i[1]}</b>\n💰Цена: <b>{i[2]} руб.</b>\n\nКатегория: <b>Мужское</b>", parse_mode='html', reply_markup= btr_f)

async def edit_product_girl_1(callback: types.CallbackQuery):
    for i in cur.execute('SELECT * FROM girl_kross').fetchall():
        btr_1 = InlineKeyboardButton('🗑Удалить товар', callback_data=f"del_zh {i[5]}")
        btr_f = InlineKeyboardMarkup()
        btr_f.add(btr_1)
        await callback.message.answer_photo(i[4], f"<b>{i[0]}</b>\n\n📜Описание: <b>{i[1]}</b>\n💰Цена: <b>{i[2]} руб.</b>\n\nКатегория: <b>Женское</b>", parse_mode='html', reply_markup= btr_f)

async def edit_product_baby_1(callback: types.CallbackQuery):
    for i in cur.execute('SELECT * FROM baby_kross').fetchall():
        btr_1 = InlineKeyboardButton('🗑Удалить товар', callback_data=f"del_b {i[5]}")
        btr_f = InlineKeyboardMarkup()
        btr_f.add(btr_1)
        await callback.message.answer_photo(i[4], f"<b>{i[0]}</b>\n\n📜Описание: <b>{i[1]}</b>\n💰Цена: <b>{i[2]} руб.</b>\n\nКатегория: <b>Детское</b>", parse_mode='html', reply_markup= btr_f)


async def del_men_kross(callback: types.CallbackQuery):
    cur.execute('DELETE FROM men_kross WHERE id ==?', (int(callback.data.replace('del ', '')),))
    base.commit()
    await callback.message.delete()

async def del_girl_kross(callback: types.CallbackQuery):
    cur.execute('DELETE FROM girl_kross WHERE id ==?', (int(callback.data.replace('del_zh ', '')),))
    base.commit()
    await callback.message.delete()

async def del_baby_kross(callback: types.CallbackQuery):
    cur.execute('DELETE FROM baby_kross WHERE id ==?', (int(callback.data.replace('del_b ', '')),))
    base.commit()
    await callback.message.delete()

async def inline_none(callback: types.CallbackQuery):
    await callback.answer('Эта кнопка действует как уведомление')

def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(admin_panel, commands=['admin'])
    dp.register_message_handler(office_t, lambda message: '📦Товары' in message.text)
    dp.register_message_handler(office_p, lambda message: '👥Пользователи' in message.text)
    dp.register_message_handler(office_z, lambda message: '🛍Заказы' in message.text)
    dp.register_callback_query_handler(new_order_f, text = ['new_order'])
    dp.register_callback_query_handler(delivery_full, text = ['delivery'])
    dp.register_callback_query_handler(completed_full, text = ['completed_in'])
    dp.register_callback_query_handler(cancellation_full, text = ['cancellation'])
    dp.register_callback_query_handler(conf_user_admin, Text(startswith= 'pay_ok_admin '))
    dp.register_callback_query_handler(cancel_user_admin, Text(startswith= 'cancel_admin '))
    dp.register_callback_query_handler(delivery_commit, Text(startswith= 'delivery_commit_in '))
    dp.register_message_handler(office_r, lambda message: '📨Рассылка' in message.text)
    dp.register_callback_query_handler(maili_bot_f, text = ['mail_bot_inline'])
    dp.register_message_handler(mail_bot_answer, state= mail_bot.message_mail)
    dp.register_message_handler(office_pro, lambda message: '🎁Промокод' in message.text)
    dp.register_callback_query_handler(promo_admin_full, text = ['promo_admin_inline'])
    dp.register_message_handler(promo_title, state= promo_m.promo_title)
    dp.register_message_handler(promo_price, state= promo_m.promo_price)
    dp.register_message_handler(office_s, lambda message: '📊Статистика' in message.text)
    dp.register_callback_query_handler(add_product_1, text = ['add_product'])
    dp.register_message_handler(title_add, state= add_product.title)
    dp.register_message_handler(description_add, state= add_product.description)
    dp.register_message_handler(price_add, state= add_product.price)
    dp.register_message_handler(size_add, state= add_product.size)
    dp.register_message_handler(photo_add, content_types=['photo'], state= add_product.photo)
    dp.register_message_handler(floor, state= add_product.floor)   
    dp.register_callback_query_handler(edit_product_1, text = ['edit_product'])
    dp.register_callback_query_handler(edit_product_men_1, text = ['edit_product_men'])
    dp.register_callback_query_handler(del_men_kross, Text(startswith='del '))
    dp.register_callback_query_handler(edit_product_girl_1, text = ['edit_product_girl'])
    dp.register_callback_query_handler(del_girl_kross, Text(startswith='del_zh '))
    dp.register_callback_query_handler(edit_product_baby_1, text = ['edit_product_baby'])
    dp.register_callback_query_handler(del_baby_kross, Text(startswith='del_b '))
    dp.register_callback_query_handler(inline_none, text = ['None'])