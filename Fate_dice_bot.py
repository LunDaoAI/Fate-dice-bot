
import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# ==== ОРАКУЛ СУДЬБЫ: данные ====

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

PAIR_INTERPRETATION = {
    (1, 1): "Цикл завершён. Начнётся новое.",
    (2, 2): "Ты видишь себя со стороны. Испытание зеркалом.",
    (3, 3): "Создание. Что ты задумал — воплотится.",
    (4, 4): "Испытание терпением. Сила в стойкости.",
    (5, 5): "Полное разрушение старого. Обновление.",
    (6, 6): "Высшая удача. Все звёзды сошлись.",
}

DICE_COMBINATIONS = {
    (1, 2): "Первый шаг. Открывается дверь.",
    (1, 3): "Мысли о возможном будущем.",
    (1, 4): "Нужно время. Подожди.",
    (1, 5): "Ломка старого. Новое начинается.",
    (1, 6): "Чудо возможно. Удача на твоей стороне.",
    (2, 3): "Диалог внутри тебя. Внутренний конфликт или гармония.",
    (2, 4): "Баланс сил. Нужно найти равновесие.",
    (2, 5): "Перемены неизбежны. Прими их.",
    (2, 6): "Поддержка свыше. Кто-то помогает тебе.",
    (3, 4): "Строительство. Ты строишь новый этап.",
    (3, 5): "Разрушение для роста. Старое уходит.",
    (3, 6): "Творческая победа. Искусство или проект будут замечены.",
    (4, 5): "Конец одного, начало другого. Переход.",
    (4, 6): "Стабильная поддержка. Успех будет долгим.",
    (5, 6): "Резкий скачок. Внезапный успех.",
}

def throw_dice():
    a = random.randint(1, 6)
    b = random.randint(1, 6)
    return a, b

def interpret(a, b):
    total = a + b
    is_pair = a == b
    energy = "a > b" if a > b else ("a < b" if a < b else "a = b")

    result = {
        "dice": (a, b),
        "total": total,
        "is_pair": is_pair,
        "energy": energy,
        "sum_interpretation": SUM_INTERPRETATION[total],
        "combination_interpretation": DICE_COMBINATIONS.get((a, b), None),
        "pair_interpretation": PAIR_INTERPRETATION.get((a, b), None) if is_pair else None
    }

    return result

# ==== КОМАНДА /ask ====
def ask(update: Update, context: CallbackContext):
    user_question = " ".join(context.args) if context.args else "Не задан."

    a, b = throw_dice()
    interpretation = interpret(a, b)

    message = f"🔮 **Вопрос:** {user_question}\n\n"
    message += f"🎲 **Выпали кости:** ({a}, {b}) → сумма: {interpretation['total']}\n\n"
    message += f"📜 **Основной ответ:** {interpretation['sum_interpretation']}\n"

    if interpretation["combination_interpretation"]:
        message += f"\n🧩 **Комбинация ({a},{b}):** {interpretation['combination_interpretation']}"

    if interpretation["pair_interpretation"]:
        message += f"\n\n🔄 **Это пара!** {interpretation['pair_interpretation']}"

    energy_meaning = {
        "a > b": "🔸 Ты ведёшь ситуацию. Можешь влиять.",
        "a < b": "🔸 Ситуация ведёт тебя. Нужно прислушаться к обстоятельствам.",
        "a = b": "🔸 Гармония между тобой и миром."
    }

    message += f"\n\n⚡ **Энергия:** {energy_meaning[interpretation['energy']]}"
    message += "\n\n🌌 **Толкование Оракула:**\n"
    message += ">\n"

    message += ">\n".join(
        [line for line in interpretation['sum_interpretation'].split(" ") if line]
    )

    update.message.reply_text(message)

# ==== ЗАПУСК БОТА ====
def main():
    updater = Updater("YOUR_BOT_TOKEN_HERE", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("ask", ask))

    print("🚀 Бот запущен...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()