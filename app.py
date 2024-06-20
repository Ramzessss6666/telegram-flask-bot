from flask import Flask, request, render_template
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os

app = Flask(__name__)

TOKEN = os.getenv('7427027764:AAH10jPkqiqP1o3Z5vWCYC3rczoKv4p6gXc')
bot = Bot(token=TOKEN)

application = ApplicationBuilder().token(TOKEN).build()

messages = []

def start(update, context):
    update.message.reply_text('Привет, Мир!')

def handle_message(update, context):
    messages.append(update.message.text)
    update.message.reply_text('Сообщение получено!')

start_handler = CommandHandler('start', start)
message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)

application.add_handler(start_handler)
application.add_handler(message_handler)

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    application.process_update(update)
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
