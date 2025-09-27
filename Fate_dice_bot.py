import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

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
    (1, 1): "Цикл завершён. Начнётся новое.",
    (1, 2): "Первый шаг. Открывается дверь.",
    (1, 3): "Мысли о возможном будущем.",
    (1, 4): "Нужно время. Подожди.",
    (1, 5): "Ломка старого. Новое начинается.",
    (1, 6): "Чудо возможно. Удача на твоей стороне.",
    (2, 2): "Ты видишь себя со стороны. Испытание зеркалом.",
    (2, 3): "Диалог внутри тебя. Внутренний конфликт или гармония.",
    (2, 4): "Баланс сил. Нужно найти равновесие.",
    (2, 5): "Перемены неизбежны. Прими их.",
    (2, 6): "Поддержка свыше. Кто-то помогает тебе.",
    (3, 3): "Создание. Что ты задумал — воплотится.",
    (3, 4): "Строительство. Ты строишь новый этап.",
    (3, 5): "Разрушение для роста. Старое уходит.",
    (3, 6): "Творческая победа. Искусство или проект будут замечены.",
    (4, 4): "Испытание терпением. Сила в стойкости.",
    (4, 5): "Конец одного, начало другого. Переход.",
    (4, 6): "Стабильная поддержка. Успех будет долгим.",
    (5, 5): "Полное разрушение старого. Обновление.",
    (5, 6): "Резкий скачок. Внезапный успех.",
    (6, 6): "Высшая удача. Все звёзды сошлись.",
}

# ==== Функции ====
def throw_dice():
    return random.randint(1, 6), random.randint(1, 6)

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
        "pair_interpretation": DICE_COMBINATIONS.get((a, b), None) if is_pair else None
    }

    return result

# ==== Команда /ask ====
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    message += ">" + interpretation['sum_interpretation']

    await update.message.reply_text(message)

# ==== Запуск бота ====
def main():
    application = Application.builder().token("YOUR_BOT_TOKEN_HERE").build()

    application.add_handler(CommandHandler("ask", ask))

    print("🚀 Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()
