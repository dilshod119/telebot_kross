from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

"""Кнопка политики конфидициальности"""
button_ok = InlineKeyboardButton('✅Согласен', callback_data='welcome')
button_1 = InlineKeyboardMarkup()
button_1.add(button_ok)

"""Основное меню ЮЗЕРА"""
bm_1 = KeyboardButton('🧰Личный кабинет')
bm_2 = KeyboardButton('🛍Товары')
bm_3 = KeyboardButton('⚙️Настройки')
bm_4 = KeyboardButton('👨🏻‍💻Помощь')
bm_5 = KeyboardButton('🔰О компании')
bm_f = ReplyKeyboardMarkup(resize_keyboard=True)
bm_f.add(bm_1).add(bm_2, bm_3).add(bm_4, bm_5)

"""Инлайн кнопки личного кабинета юзера"""
bl_1 = InlineKeyboardButton('🛍Активные заказы', callback_data= 'active_order_inline')
bl_3 = InlineKeyboardButton('🗂История покупок', callback_data= 'history_user')
bl_4 = InlineKeyboardButton('🎁Ввести промокод', callback_data= 'promo_kod')
bl_5 = InlineKeyboardButton('🗑Корзина', callback_data='favorites_tov')
bl_f = InlineKeyboardMarkup()
bl_f.add(bl_1).add(bl_5).add(bl_3, bl_4)

"""Кнопки товаров юзера"""
bt_2 = InlineKeyboardButton ('👨🏻Мужские', callback_data= 'price_men')
bt_3 = InlineKeyboardButton ('👩🏻‍🦰Женские', callback_data= 'price_girl')
bt_4 = InlineKeyboardButton ('👦🏻Детские', callback_data= 'price_baby')
bt_f = InlineKeyboardMarkup(row_width= 1)
bt_f.add(bt_2, bt_3, bt_4)



"""Кнопки настройки юзера"""
bn_2 = InlineKeyboardButton('📇Поменять Имя', callback_data='edit_name')
bn_3 = InlineKeyboardButton('📧Поменять Эл.Почту', callback_data='edit_email')
bn_4 = InlineKeyboardButton('📞Поменять номер', callback_data='edit_phone')
bn_ad = InlineKeyboardButton('🚚Добавить адрес доставки', callback_data='set_adress')
bn_5 = InlineKeyboardButton('🗑Очистить историю покупок', callback_data='5')
bn_f = InlineKeyboardMarkup()
bn_f.add(bn_2).add(bn_3).add(bn_4).add(bn_ad).add(bn_5)

