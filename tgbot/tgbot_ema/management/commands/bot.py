from django.contrib.auth.models import User
from typing import Optional, Any
from django.core.management.base import BaseCommand
from telebot import TeleBot
from .keyboard import keyboard as kb
import os
from dotenv import load_dotenv, find_dotenv

from tgbot_ema.models import Profile, Product, Category

load_dotenv(find_dotenv())

bot = TeleBot(os.getenv('TOKEN'), threaded=False)



class Command(BaseCommand):
    help = "implemented to Django telegram"

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        bot.enable_save_next_step_handlers(delay=2)
        #bot.load_next_step_handlers()
        bot.infinity_polling()


# Запуск бота и регистрация пользователя

@bot.message_handler(commands=['start'])
def welcome(message):
    user_data = message.from_user

    try:
        Profile.objects.get(telegram_user_id=user_data.id)
    except Profile.DoesNotExist:
        user = User.objects.create(
            username=user_data.username or user_data.id,
            first_name=user_data.first_name,
            last_name=user_data.last_name)
        Profile.objects.create(user_id=user.id,
                               telegram_user_id=user_data.id)
    bot.send_message(message.chat.id, f'<i>Добро пожаловать в БОТ, {user_data.first_name} 👋 \n\n'
                                      'МЫ магазин мемориальной архитектуры EMA.by\n\n'
                                      'Поможем ВАМ заказать необходимые товары ✅\n\n'
                                      'Для дальнейшей работы нажмите команду</i> /register', parse_mode='html')


# Обработка команды /register
@bot.message_handler(commands=['register'])
def register(message):
    bot.send_message(message.chat.id, '<i>Вы можете выбрать подходящий товар нажав кнопку Каталог📔\n\n'
                                      'Так же познакомиться с нами на нашем сайте💻</i>',
                     parse_mode='html',
                     reply_markup=kb.menu)


# обработка команды /order и запрос номера телефона клиента
@bot.message_handler(commands=['order'])
def order(message):
    msg = bot.send_message(message.chat.id, '<b>Введите свой номер телефона для связи, в формате:</b>\n'
                                            '29xxxxxxx, 33xxxxxxx, 44xxxxxxx, 25xxxxxxx', parse_mode='html')
    bot.register_next_step_handler(msg, save_order)


def save_order(message):
    user_data = message.from_user
    user_phone = message.text
    telegram_ids = Profile.objects\
        .filter(user__is_staff=True) \
        .exclude(telegram_user_id=message.from_user.id) \
        .values_list('telegram_user_id', flat=True)
    for admin in telegram_ids:
        bot.send_message(admin, f'<b>{user_data.first_name} {user_data.last_name}</b>\n'
                                f'telegram-id {user_data.id} \n'
                                f'<i>Осуществил(а) заказ</i>\n'
                                f'<i>Ждёт связи с администратором</i>', parse_mode='html')
    bot.send_message(message.chat.id, f'<i>Ваша заявка принята</i>, {user_data.first_name}✅\n'
                                      f'<i>Администратор свяжется с вами для уточнения заказа</i>☎️',
                    parse_mode='html')

    doc = open('client.txt', 'a+', encoding='utf-8')
    doc.write(f"Имя - {user_data.first_name}\n Телефон - {user_phone}\n")
    doc.close()





# Обработка текстовых сообщений отправленных клиентом
@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'Каталог📔':
        bot.send_message(message.chat.id, '<u>⬇️Выберите интересующую Вас категорию⬇️</u>',
                         parse_mode='html', reply_markup=kb.catalog_menu)
    elif message.text == 'Наш сайт🌐':
        bot.send_message(message.chat.id, 'https://ema.by/')
    elif message.text == 'Лампады1️⃣':
        category_lamps = Category.objects.get(name='Лампады')
        show_lamps = category_lamps.products.all()
        for obj in show_lamps:
            msg_lamps = f'<i>Вы выбрали категорию Лампады✅</i>\n{obj.name}\n{obj.description}\n{obj.price} руб.'
            if obj.id == 3:
                bot.send_photo(message.chat.id, photo=open('media/Лампада2.jpg', 'rb'),
                               caption=msg_lamps, parse_mode='html', reply_markup=kb.menu_order)
            elif obj.id == 4:
                bot.send_photo(message.chat.id, photo=open('media/Лампада1.jpg', 'rb'),
                               caption=msg_lamps, parse_mode='html', reply_markup=kb.menu_order)
    elif message.text == 'Вазы2️⃣':
        category_vases = Category.objects.get(name='Вазы')
        show_vases = category_vases.products.all()
        for obj in show_vases:
            msg_vases = f'<i>Вы выбрали категорию Вазы✅</i>\n{obj.name}\n{obj.description}\n{obj.price} руб.'
            if obj.id == 1:
                bot.send_photo(message.chat.id, photo=open('media/Ваза1.jpg', 'rb'),
                               caption=msg_vases, parse_mode='html', reply_markup=kb.menu_order)
            elif obj.id == 2:
                bot.send_photo(message.chat.id, photo=open('media/Ваза2.jpg', 'rb'),
                               caption=msg_vases, parse_mode='html', reply_markup=kb.menu_order)
            elif obj.id == 5:
                bot.send_photo(message.chat.id, photo=open('media/Ваза3.jpg', 'rb'),
                               caption=msg_vases, parse_mode='html', reply_markup=kb.menu_order)
    elif message.text == 'Оформить заказ/Купить🛒':
        bot.send_message(message.chat.id, '<b>Для отправки заявки администратору нажмите команду⬇️📌</b>\n'
                                          '/order\n'
                                          'Для возвращения в каталог нажмите кнопку <b>🔙Назад</b>',
                         parse_mode='html',
                         reply_markup=kb.menu_reg)
    elif message.text == '🔙Назад':
        bot.send_message(message.chat.id, '<b>Вы вернулись в каталог</b>',
                         parse_mode='html',
                         reply_markup=kb.catalog_menu)
    else:
        bot.reply_to(message.chat.id, 'Я вас не понимаю😔\n'
                                          'Выполните предложенные действия')
