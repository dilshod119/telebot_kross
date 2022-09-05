from aiogram.utils import executor
from create_bot import dp
import sqlite3
from handlers import admin, client


async def on_startup(_):
    print('Бот работает')
    base = sqlite3.connect('base.db')
    base.execute('CREATE TABLE IF NOT EXISTS data (id PRIMARY KEY, name, email, phone, bal, products_id, user_name, adress, promo)')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS admin (id)')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS products_id (id)')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS men_kross (title, description, price, size, photo, id)')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS girl_kross (title, description, price, size, photo, id)')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS baby_kross (title, description, price, size, photo, id)')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS order_basket (id_user, id_price, id_order, size, status, user_name, user_phone, user_email, user_adress, price_title, price_price, price_photo, promo)')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS promo (discount_cod, money, state)')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS card (card)')
    base.commit()

admin.register_handlers_admin(dp)
client.register_handlers_client(dp) 




executor.start_polling(dp, skip_updates=True, on_startup= on_startup)
