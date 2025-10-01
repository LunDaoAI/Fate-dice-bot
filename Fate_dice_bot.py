import random
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# ==== Функция авто-пробуждения ====
def keep_alive():
    """Периодически отправляет запросы чтобы бот не засыпал"""
    while True:
        try:
            # Пингуем разные сервисы для надежности
            requests.get('https://www.google.com', timeout=10)
            print(f"🔄 Keep-alive ping sent at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"⚠️ Keep-alive error: {e}")
        time.sleep(300)  # Каждые 5 минут

# ==== Толкования ====
SUM_INTERPRETATION = {
    2: "❌ Невозможно. Не время, не ты, не судьба.",
    3: "🕯️ Тень шанса. Очень маленький проблеск.",
    4: "⚖️ Всё зависит от обстоятельств. Нужны усилия.",
    5: "🌀 Непредсказуемость. Перемены в движении.",
    6: "🌫️ Возможность есть, но скрыта. Требуется интуиция.",
    7: "💫 Получится, но не так, как ты думаешь.",
    8: "🔮 Высокая вероятность успеха. Действуй!",
    9: "🌟 Да, если действовать умно и вовремя.",
    10: "🏆 Успех почти гарантирован. Победа близка.",
    11: "🌈 Чудо или неожиданный поворот. Благоприятный знак.",
    12: "✅ Положительный ответ. Судьба говорит 'да'.",
}

DICE_COMBINATIONS = {
    # (1,1) - (1,6)
    (1, 1): "Цикл завершён. Начнётся новое.",
    (1, 2): "Первый шаг. Открывается дверь.",
    (1, 3): "Мысли о возможном будущем.",
    (1, 4): "Нужно время. Подожди.",
    (1, 5): "Ломка старого. Новое начинается.",
    (1, 6): "Чудо возможно. Удача на твоей стороне.",
    
    # (2,1) - (2,6)
    (2, 1): "Первый шаг. Открывается дверь.",
    (2, 2): "Ты видишь себя со стороны. Испытание зеркалом.",
    (2, 3): "Диалог внутри тебя. Внутренний конфликт или гармония.",
    (2, 4): "Баланс сил. Нужно найти равновесие.",
    (2, 5): "Перемены неизбежны. Прими их.",
    (2, 6): "Поддержка свыше. Кто-то помогает тебе.",
    
    # (3,1) - (3,6)
    (3, 1): "Мысли о возможном будущем.",
    (3, 2): "Диалог внутри тебя. Внутренний конфликт или гармония.",
    (3, 3): "Создание. Что ты задумал — воплотится.",
    (3, 4): "Строительство. Ты строишь новый этап.",
    (3, 5): "Разрушение для роста. Старое уходит.",
    (3, 6): "Творческая победа. Искусство или проект будут замечены.",
    
    # (4,1) - (4,6)
    (4, 1): "Нужно время. Подожди.",
    (4, 2): "Баланс сил. Нужно найти равновесие.",
    (4, 3): "Строительство. Ты строишь новый этап.",
    (4, 4): "Испытание терпением. Сила в стойкости.",
    (4, 5): "Конец одного, начало другого. Переход.",
    (4, 6): "Стабильная поддержка. Успех будет долгим.",
    
    # (5,1) - (5,6)
    (5, 1): "Ломка старого. Новое начинается.",
    (5, 2): "Перемены неизбежны. Прими их.",
    (5, 3): "Разрушение для роста. Старое уходит.",
    (5, 4): "Конец одного, начало другого. Переход.",
    (5, 5): "Полное разрушение старого. Обновление.",
    (5, 6): "Резкий скачок. Внезапный успех.",
    
    # (6,1) - (6,6)
    (6, 1): "Чудо возможно. Удача на твоей стороне.",
    (6, 2): "Поддержка свыше. Кто-то помогает тебе.",
    (6, 3): "Творческая победа. Искусство или проект будут замечены.",
    (6, 4): "Стабильная поддержка. Успех будет долгим.",
    (6, 5): "Резкий скачок. Внезапный успех.",
    (6, 6): "Высшая удача. Все звёзды сошлись."
}

def throw_dice():
    return random.randint(1, 6), random.randint(1, 6)

def interpret(a, b):
    total = a + b
    is_pair = a == b
    
    return {
        "dice": (a, b),
        "total": total,
        "is_pair": is_pair,
        "energy": "a > b" if a > b else ("a < b" if a < b else "a = b"),
        "sum_interpretation": SUM_INTERPRETATION.get(total, "📊 Результат требует осмысления."),
        "combination_interpretation": DICE_COMBINATIONS.get((a, b), "🎯 Уникальная комбинация.")
    }

def start(update: Update, context: CallbackContext):
    welcome_text = """
🌟 Добро пожаловать в Оракул Костей! 🌟

Используйте команду /ask и ваш вопрос для получения предсказания.

📝 Пример:
/ask Ждать ли мне перемен в жизни?
/ask Стоит ли начинать новый проект?
    """
    update.message.reply_text(welcome_text)

def ask(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("❌ Задайте вопрос после команды /ask")
        return

    user_question = " ".join(context.args)
    a, b = throw_dice()
    interpretation = interpret(a, b)

    message = f"🔮 Вопрос: {user_question}\n\n"
    message += f"🎲 Кости: ({a}, {b}) → Сумма: {interpretation['total']}\n\n"
    message += f"📜 Толкование: {interpretation['sum_interpretation']}\n"

    if "Уникальная" not in interpretation['combination_interpretation']:
        message += f"\n🧩 Комбинация ({a},{b}): {interpretation['combination_interpretation']}"

    if interpretation["is_pair"]:
        message += f"\n\n🔄 Это пара {a}! Особое совпадение."

    energy_meaning = {
        "a > b": "🔸 Ты ведёшь ситуацию. Можешь влиять на события.",
        "a < b": "🔸 Ситуация ведёт тебя. Прислушайся к обстоятельствам.",
        "a = b": "🔸 Гармония между тобой и миром."
    }
    message += f"\n\n⚡ Энергия: {energy_meaning[interpretation['energy']]}"

    update.message.reply_text(message)

def help_command(update: Update, context: CallbackContext):
    help_text = """
📋 Доступные команды:
/start - Начать работу
/ask [вопрос] - Получить предсказание
/help - Помощь

🎲 Бот бросает кости и интерпретирует результат!
    """
    update.message.reply_text(help_text)

def main():
    BOT_TOKEN = "7963571696:AAFEkKbe_V4eVf9TPhnaW4yQOijX-hI6tYk"
    
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ask", ask))
    dp.add_handler(CommandHandler("help", help_command))

    print("🚀 Бот Оракул Костей запущен...")
    
    # ==== ДЛЯ RENDER.COM ====
    # Используем polling вместо webhook для простоты
    # Webhook требует HTTPS домена и сложной настройки
    updater.start_polling()
    print("🤖 Бот начал прослушивание сообщений...")
    updater.idle()

if __name__ == '__main__':
    main()
