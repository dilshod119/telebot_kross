from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


"""Основное меню АДМИНА"""
bm_1 = KeyboardButton('📊Статистика')
bm_2 = KeyboardButton('📦Товары')
bm_4 = KeyboardButton('🛍Заказы')
bm_5 = KeyboardButton('📨Рассылка')
bm_6 = KeyboardButton('🎁Промокод')
bm_f = ReplyKeyboardMarkup(resize_keyboard=True)
bm_f.add(bm_1).add(bm_2, bm_4).add(bm_5, bm_6)


"""Товары доб/ред/уд в настройках адми"""
bt_1 = InlineKeyboardButton('➕Добавить товар', callback_data='add_product')
bt_2 = InlineKeyboardButton('✏️Редактировать', callback_data='edit_product')
bt_f = InlineKeyboardMarkup(row_width=1)
bt_f.add(bt_1, bt_2)

"""   Инлайн кнопки редактора товаров  КАТЕГОРИИ """
bti_1 = InlineKeyboardButton('👨🏻Мужское', callback_data='edit_product_men')
bti_2 = InlineKeyboardButton('👩🏻‍🦰Женское', callback_data='edit_product_girl')
bti_3 = InlineKeyboardButton('👦🏻Детское', callback_data='edit_product_baby')
bti_f = InlineKeyboardMarkup(row_width=1)
bti_f.add(bti_1, bti_2, bti_3)

"""Пользователи в настройках админа"""
bp_1 = InlineKeyboardButton('🔐Черный список', callback_data='1')
bp_2 = InlineKeyboardButton('🔍Поиск по id', callback_data='2')
bp_f = InlineKeyboardMarkup(row_width=1)
bp_f.add(bp_1, bp_2)


"""Заказы в настройках адми"""
bz_1 = InlineKeyboardButton('🟢Новые заявки', callback_data='new_order')
bz_2 = InlineKeyboardButton('🟢Передано в доствку', callback_data='delivery')
bz_3 = InlineKeyboardButton('🔴Завершенные', callback_data='completed_in')
bz_4 = InlineKeyboardButton('❌Отмененные', callback_data='cancellation')

bz_f = InlineKeyboardMarkup(row_width=1)
bz_f.add(bz_1, bz_2, bz_3, bz_4)


"""Рассылка в настройках админа"""
br_2 = InlineKeyboardButton('🤖Начать рассылку', callback_data='mail_bot_inline')
br_f = InlineKeyboardMarkup(row_width=1)
br_f.add(br_2)


"""Промокод в настройках админа"""
bpromo_1 = InlineKeyboardButton('💰В руб.', callback_data='promo_admin_inline')
bpromo_f = InlineKeyboardMarkup(row_width=1)
bpromo_f.add(bpromo_1)


"""Добавление товара пол, для распределения по база"""
bkey_1 = KeyboardButton('👨🏻Мужское')
bkey_2 = KeyboardButton('👩🏻‍🦰Женское')
bkey_3 = KeyboardButton('👦🏻Детское')
bkey_f = ReplyKeyboardMarkup(resize_keyboard= True, row_width= 1)
bkey_f.add(bkey_1, bkey_2, bkey_3)