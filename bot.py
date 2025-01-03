from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os
from dotenv import load_dotenv
import google.generativeai as ai

load_dotenv()

class Chatbot:

    def __init__(self,token,ai_apikey):
        self.token:str = token
        self.ai_apikey:str = ai_apikey
        self.mode:str = "normal"
        self.allow_mode:list[str] = ["ai_chatbot","normal"]

    # change if you want use other ai
    def generateAI(self):
        api_key = self.ai_apikey
        ai.configure(
            api_key=api_key
        )

        model = ai.GenerativeModel("gemini-1.5-flash-002")
        chat = model.start_chat()

        return chat

    async def change_mode(self, update: Update, context: CallbackContext):
        command = context.args[0] if context.args else "normal"
        if command in self.allow_mode:
            self.mode = command
            await update.message.reply_text(f"Mode telah diubah ke: {self.mode}")
        else:
            await update.message.reply_text(f"no mode with name ({command})\nuse:\n\n{'\n'.join([f"/mode {mode}" for mode in self.allow_mode])}")

    async def start(self,update: Update, context: CallbackContext):
        await update.message.reply_text('Halo! Saya adalah bot sederhana di tenagai oleh meta ai!. Kirimkan pesan untuk memulai!')
    
    async def help(self,update:Update,context:CallbackContext):
        await update.message.reply_text(f"command yang tersedia: \n\n/mode mengubah mode({','.join(self.allow_mode)})\n/help melihat command yang ada")
    
    # Fungsi untuk menanggapi pesan teks
    async def echo(self,update: Update, context: CallbackContext):
        message_user = update.message.text

        match self.mode:
            case "ai_chatbot":
                try:

                    # change if you want use other ai
                    chat = self.generateAI()

                    response = chat.send_message(message_user)
                    
                    await update.message.reply_text(response.text)
                except Exception as e:
                    await update.message.reply_text(f"an error occured: {e}")
            case "normal":
                await update.message.reply_text(f"anda mengirim {message_user}")


    def main(self):
        app = Application.builder().token(self.token).pool_timeout(30).build()

        app.add_handler(CommandHandler("start",self.start))
        app.add_handler(CommandHandler("mode",self.change_mode))
        app.add_handler(CommandHandler("help",self.help))

        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))

        # Memulai bot
        app.run_polling()

if __name__ == '__main__':
    program = Chatbot(
        os.getenv("SECRET_TELEGRAM_KEY"),
        os.getenv("SECRET_AI_APIKEY"),
    )
    program.main()