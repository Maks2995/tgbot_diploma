from telebot import types


# Меню при выполнении команды /register
menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn_site = types.KeyboardButton(text='Наш сайт🌐')
btn_ctlg = types.KeyboardButton(text='Каталог📔')
menu.add(btn_ctlg, btn_site)

# меню после выбора категории
menu_order = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn_order = types.KeyboardButton(text='Оформить заказ/Купить🛒')
btn_back = types.KeyboardButton(text='🔙Назад')
menu_order.add(btn_order, btn_back)

# Меню катагории
catalog_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=True)
btn_lamps = types.KeyboardButton('Лампады1️⃣')
btn_vases = types.KeyboardButton('Вазы2️⃣')
catalog_menu.add(btn_lamps, btn_vases)

# Кнока назад
menu_reg = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=True)
btn_back = types.KeyboardButton('🔙Назад')
menu_reg.add(btn_back)
