from django.core.management import BaseCommand
from aiogram import executor

from main.API_TG import handlers
from main.API_TG.configs.loader import dp

class Command(BaseCommand):
    help = 'Запуск бота'

    def handle(self, *args, **options):
        executor.start_polling(dp, skip_updates=True)