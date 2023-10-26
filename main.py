import telebot
import config
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def greet_user(message):
    bot.send_message(message.chat.id, "Привет! Я Victor! Могу строить различные графики по твоим данным. Пожалуйста, выбери, что ты хочешь сделать.", reply_markup=build_keyboard())

def build_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    graph_button = telebot.types.KeyboardButton(text='Построить гистограмму')
    pie_chart_button = telebot.types.KeyboardButton(text='Построить круговую диаграмму')
    line_graph_button = telebot.types.KeyboardButton(text='Построить линейный график')
    scatter_button = telebot.types.KeyboardButton(text='Построить точечную диаграмму')
    keyboard.add(graph_button, pie_chart_button, line_graph_button,scatter_button)
    return keyboard

def build_inlinekeyboard():
    markup_inline = telebot.types.InlineKeyboardMarkup()
    item_example = telebot.types.InlineKeyboardButton(text='Пример ввода', callback_data='example')
    markup_inline.add(item_example)
    return markup_inline

def build_inlinekeyboard_scatter_button():
    markup_inline = telebot.types.InlineKeyboardMarkup()
    item_example = telebot.types.InlineKeyboardButton(text='Пример ввода', callback_data='example_scatter')
    markup_inline.add(item_example)
    return markup_inline

@bot.callback_query_handler(func=lambda call: call.data == 'example')
def callback_query(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 'Пример:\n\n20, 30, 50; Название 1, Название 2, Название 3; Имя графика\n\nПримечание: Количество значений равно количеству названий.\nНе забывай расставлять знаки( , и ; ) и указывать имя графика!')
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'example_scatter')
def callback_query_scatter_button(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 'Пример:\n\n20, 30, 50; 30, 50, 20; Имя графика\n\nПримечание: Количество значений по оси X равно количеству значений по оси Y.\nНе забывай расставлять знаки( , и ; ) и указывать имя графика!')
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Построить гистограмму':
        bot.send_message(message.chat.id, 'Введи значения 👨🏼‍🏫', reply_markup=build_inlinekeyboard())
        bot.register_next_step_handler(message, build_graph)
    elif message.text == 'Построить круговую диаграмму':
        bot.send_message(message.chat.id, 'Введи значения 👨🏼‍💻', reply_markup=build_inlinekeyboard())
        bot.register_next_step_handler(message, build_pie_chart)
    elif message.text == 'Построить линейный график':
        bot.send_message(message.chat.id, 'Введи значения 👨🏼‍🏫', reply_markup=build_inlinekeyboard())
        bot.register_next_step_handler(message, build_line_graph)
    elif message.text == 'Построить точечную диаграмму':
        bot.send_message(message.chat.id, 'Введи значения 👨🏼‍💻', reply_markup=build_inlinekeyboard_scatter_button())
        bot.register_next_step_handler(message, build_scatter)
    else:
        bot.send_message(message.chat.id, "Извини, я не понимаю. Пожалуйста, выбери, что ты хочешь построить", reply_markup=build_keyboard())

def build_graph(message):
    try:
        values, labels, title = message.text.split(';')
        values = [float(v) for v in values.split(',')]
        labels = labels.split(',')
        plt.clf()  # clear the current plot
        plt.bar(labels, values)
        plt.title(title)  # Set the title based on user input
        '''
        plt.xlabel('')
        plt.ylabel('')
        '''
        plt.savefig('bar_graph.png')  # save plot to image file
        with open('bar_graph.png', 'rb') as f:
            bot.send_photo(message.chat.id, f)  # send image as photo
        bot.send_message(message.chat.id, "Хочешь построить ещё один график?", reply_markup=build_keyboard())
    except:
        bot.send_message(message.chat.id, "Извини, я не смог построить график. Пожалуйста, попробуй еще раз.", reply_markup=build_keyboard())

def build_pie_chart(message):
    try:
        values, labels, title = message.text.split(';')
        values = [float(v) for v in values.split(',')]
        labels = labels.split(',')
        plt.clf() # Clear the current figure
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title(title)  # Set the title based on user input
        plt.savefig('pie_chart.png')  # save plot to image file
        with open('pie_chart.png', 'rb') as f:
            bot.send_photo(message.chat.id, f)  # send image as photo
        bot.send_message(message.chat.id, "Хочешь построить ещё один график?", reply_markup=build_keyboard())
    except:
        bot.send_message(message.chat.id, "Извини, я не смог построить диаграмму. Пожалуйста, попробуй еще раз.", reply_markup=build_keyboard())

def build_line_graph(message):
    try:
        values, labels, title = message.text.split(';')
        values = [float(v) for v in values.split(',')]
        labels = labels.split(',')
        plt.clf() # Clear the current figure
        plt.plot(labels, values, marker='o')
        plt.title(title)  # Set the title based on user input
        plt.savefig('line_graph.png')  # save plot to image file
        with open('line_graph.png', 'rb') as f:
            bot.send_photo(message.chat.id, f)  # send image as photo
        bot.send_message(message.chat.id, "Хочешь построить ещё один график?", reply_markup=build_keyboard())
    except:
        bot.send_message(message.chat.id, "Извини, я не смог построить график. Пожалуйста, попробуй еще раз.", reply_markup=build_keyboard())

def build_scatter(message):
    try:
        x_values, y_values, title = message.text.split(';')
        x_values = [float(v) for v in x_values.split(',')]
        y_values = [float(v) for v in y_values.split(',')]
        plt.clf() # Clear the current figure
        plt.scatter(x_values, y_values)
        plt.title(title)  # Set the title based on user input
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.savefig('scatter_plot.png')  # save plot to image file
        with open('scatter_plot.png', 'rb') as f:
            bot.send_photo(message.chat.id, f)  # send image as photo
        bot.send_message(message.chat.id, "Хочешь построить ещё один график?", reply_markup=build_keyboard())
    except:
        bot.send_message(message.chat.id, "Извини, я не смог построить точечную диаграмму. Пожалуйста, попробуй еще раз.", reply_markup=build_keyboard())

if __name__ == '__main__':
     bot.infinity_polling()
