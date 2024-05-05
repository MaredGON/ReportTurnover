#import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from asgiref.sync import sync_to_async
from functools import wraps
from datetime import datetime
from main.API_TG.configs.loader import dp, bot
from main.models import (
    CustomUser,
    Student,
    Laboratory_Status,
    EducationalGroup,
)
from utils import (
    AsyncAtomicContext,
    is_student_register,
    create_laboratory_status_one_student,
    generator_qr,
    get_laboratory_status,
)

commands = ["/start","/menu","/help"]
goMenu = ["Главное меню"]
buttonRregister = ["Регистрация"]
backButton = ["️Назад ⬅️"]
main_menu_button = ["Меню"]
mainMenu = ["Генерация","Статистика"]
labs = ["Информатика","Программирование","Дискретная математика"]
informationLabs = ["#1","#2","#3","#4","#5","Робот"]
programingLabs = ["#6","#7","#8","#9"]
discretLabs = ["#1","#2","#3","#4","#5"]

GroopList = ['1302']
peopleName = ['Илья']
REG = ['213231','43151341']
class menu(StatesGroup):
    start = State()
    main = State()
    generate = State()
    stat = State()

class register(StatesGroup):
    Start = State()
    Groop = State()
    FullName = State()
class subjects(StatesGroup):
    waitingLabsGenerated = State()
    waitingLabsStates = State()
    add_comment = State()
    display_laboratory = State()

class Full_Name(StatesGroup):
    Name = State()

class InformationLabs(StatesGroup):
    lab1 = State()
    lab2 = State()
    lab3 = State()
    lab4 = State()
    lab5 = State()
    Robot = State()

Welcom = (
    'Привет! 👋\n'
    'Тебя приветсвует Бот.\n \n'
    'Я могу сгенерировать для тебя QR-code и отобразить всю информацию по твоим лабораторным работам.\n'
    'Всё управление осуществояется нажатием кнопок внизу или через сообщение сответсвующее названию кнопок\n \n'
    'Список доступных команд:\n'
    '📍 /start - начало работы (❗️- если что-то пошло нет так, попробуйте перезапустить меня этой командой)\n'
    '📍 /menu - главное меню\n'
    '📍 /help - список доступных команд\n'
)

printHelp = (
    'Запутался? Держи список команд:\n'
    '📍 /start - начало работы (❗️- если что-то пошло нет так, попробуйте перезапустить меня этой командой\n'
    '📍 /menu - главное меню\n'
    '📍 /help - список доступных команд\n'
)

printMainMenu = (
    'Выбери действие:\n'
    '📍Генерация - сгенерировать QR-code по выбранной вами лабораторной работе\n'
    '📍Статистика - показать информацию о ваших лабораторных работах'
)

printRegister = (
    'Вы не заригестрированны. Пожалйста, пройдите регистрацию'
)


def student_registration_required(handler):
    @wraps(handler)
    async def wrapper(message: types.Message, state: FSMContext, *args, **kwargs):
        chat_id = message.chat.id
        if await is_student_register(chat_id):
            return await handler(message, state, *args, **kwargs)
        else:
            await register.Start.set()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*buttonRregister)
            await message.answer(printRegister, reply_markup=keyboard)

    return wrapper


@dp.message_handler(commands=['start'], state="*")
@student_registration_required
async def main(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*goMenu)
    await message.answer(Welcom, reply_markup=keyboard)
    await menu.start.set()


@dp.message_handler(state=register.Start)
async def startRegister(message: types.Message, state: FSMContext):
    await state.update_data(user_Register=message.text)
    if message.text not in buttonRregister:
        await message.answer("Вам необходимо зарегистрироваться!")
        return
    await register.Groop.set()
    await message.answer("Введите свою группу", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=menu.start)
async def startMenu(message: types.Message, state: FSMContext):
    await state.update_data(user_Start=message.text)
    if message.text not in goMenu:
        await message.answer("❗️ Нажмите на кнопку или введите: Главное меню ❗️")
        return
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*mainMenu)
    await message.answer(printMainMenu,reply_markup=keyboard)
    await menu.main.set()

@dp.message_handler(commands=['menu'])
@student_registration_required
async def commadMenu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*mainMenu)
    await menu.main.set()

@dp.message_handler(commands=['help'])
async def helpMenu(message: types.Message):
    await message.answer(printHelp)

@dp.message_handler(state=register.Groop)
async def register_FullName(message: types.Message, state: FSMContext):
    await state.update_data(Groop=message.text)
    try:
        get_group = sync_to_async(EducationalGroup.objects.get)
        group = await get_group(number=message.text)
    except EducationalGroup.DoesNotExist:
        await message.answer("Такой группы нет в базе")
        return
    await state.update_data(group=group)
    await message.answer("Введите своё ФИО. Убедитесь в правильности написания:")
    await register.FullName.set()

@dp.message_handler(state=register.FullName)
async def register_FullName(message: types.Message, state: FSMContext):
    await state.update_data(FullName=message.text)
    #Обработка ФИО (Разбиение на отдельные слова, запоминание id, отправление в БД(Имя, Фамилия, Отчество, группа, id))
    try:
        name, surname, patronymic = message.text.split(' ')
        chat = message.chat.id
        async with AsyncAtomicContext():
            user, created = await sync_to_async(CustomUser.objects.get_or_create)(
                name=name,
                surname=surname,
                patronymic=patronymic,
                username=message.from_user.id,
                role=CustomUser.ROLE_STUDENT,
            )

            if created:
                data = await state.get_data()
                group = data.get('group')
                student = await sync_to_async(Student.objects.create)(
                    user=user,
                    group=group,
                    chat=chat,
                )
                await sync_to_async(create_laboratory_status_one_student)(student)
                await message.answer(f"Студент {user.name} {user.surname} успешно создан")
            else:
                await message.answer("Пользователь уже существует и является студентом")

    except Exception as e:
        await message.answer("Не удалось создать студента: " + str(e))
        return
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*mainMenu)
    await message.answer(printMainMenu,reply_markup=keyboard)
    await menu.main.set()

@dp.message_handler(state=menu.main)
async def wait_menu(message: types.Message, state: FSMContext):
    await state.update_data(subject_Lab=message.text)
    try:
        async with AsyncAtomicContext():
            student = await sync_to_async(Student.objects.get)(chat=message.chat.id)
            laboratory_states = await sync_to_async(Laboratory_Status.objects.filter)(student=student)
            subjects_title = set(
                await sync_to_async(lambda: [
                    item.laboratory.educational.title for item in laboratory_states])()
            )
            await state.update_data(laboratory_states=laboratory_states)
            await state.update_data(subjects_title=subjects_title)
            await state.update_data(student=student)

    except Exception as e:
        print(str(e))
    if (message.text not in mainMenu):
        await message.answer("❗️ Такого действия нет, попробуйте снова ❗️️")
        return
    if (message.text == "Генерация"):
        await menu.generate.set()
    elif (message.text == "Статистика"):
        await menu.stat.set()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*subjects_title)
    keyboard.add(*backButton)
    await message.answer("Выбери предмет: ", reply_markup=keyboard)


@dp.message_handler(state=[menu.stat, menu.generate])
async def laboratory_handler(message: types.Message, state: FSMContext):
    await state.update_data(lab=message.text)
    data = await state.get_data()
    if message.text in backButton[0]:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*mainMenu)
        await message.answer(printMainMenu, reply_markup=keyboard)
        await menu.main.set()
    else:
        try:
            laboratory_states = data.get('laboratory_states')
            laboratory_states_filter_subject =  await sync_to_async(
                lambda: [
                    x for x in laboratory_states if x.laboratory.educational.title == message.text
                ]
            )()
            laboratory_states_title = [x.laboratory.title for x in laboratory_states_filter_subject]
            await state.update_data(laboratory_states_title=laboratory_states_title)
            await state.update_data(educational=message.text)
        except Exception as e:
            print(str(e))

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*laboratory_states_title)
        keyboard.add(*backButton)
        current_state = await state.get_state()
        if current_state == menu.generate.state:
            await subjects.waitingLabsGenerated.set()
        elif current_state == menu.stat.state:
            await subjects.waitingLabsStates.set()

        await message.answer("Выберете лабораторную работу: ", reply_markup=keyboard)


@dp.message_handler(state=[subjects.waitingLabsGenerated, subjects.waitingLabsStates])
async def InfNumberLab(message: types.Message, state: FSMContext):
    await state.update_data(numbers=message.text)
    data = await state.get_data()
    if message.text == backButton[0]:
        await menu.generate.set() # Получаем сохраненные данные из состояния
        subjects_title = data.get('subjects_title')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*subjects_title)
        keyboard.add(*backButton)
        await message.answer("Выберите предмет: ", reply_markup=keyboard)
    else:
        student = data.get('student')
        educational_title = data.get('educational')
        current_state = await state.get_state()
        await state.update_data(title_lab=message.text)
        if current_state == subjects.waitingLabsGenerated.state:
            await message.answer(f"Вы выбрали лабораторную {message.text.lower()} по дисциплине {educational_title}.\n")
            await subjects.add_comment.set()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*main_menu_button)
            await message.answer("Введите комментарий", reply_markup=keyboard)
        elif current_state == subjects.waitingLabsStates.state:
            await display_laboratory_state(state, message.chat.id)



@dp.message_handler(state=subjects.add_comment)
async def add_comment_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == main_menu_button[0]:
        await menu.main.set()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*mainMenu)
        await message.answer("Выберете дейстиве: ", reply_markup=keyboard)
    else:
        try:
            laboratory_status = await get_laboratory_status(data)
            laboratory_status_id = laboratory_status.id
            current_datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if laboratory_status.student_status == laboratory_status.STUDENT_STATUS_NOT_GENERATED:
                path_photo = await generator_qr(laboratory_status_id)
                laboratory_status.student_comment = f"({current_datetime_str}): {message.text}\n\n"
                laboratory_status.student_status = laboratory_status.STUDENT_STATUS_GENERATED
                with open(path_photo, 'rb') as photo:
                    await message.answer("QR успешно сгенерирован")
                    await bot.send_photo(chat_id=message.chat.id, photo=photo)
            else:
                laboratory_status.student_comment = f"{laboratory_status.student_comment}({current_datetime_str}): {message.text}\n\n"
                await message.answer("Данные изменены, воспользуйтесь qr кодом с прошлой генерации")

            await sync_to_async(laboratory_status.save)()
            await menu.main.set()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*mainMenu)
            await message.answer("Выбирете дейстиве: ", reply_markup=keyboard)

        except Exception as e:
            print(str(e))


async def display_laboratory_state(state: FSMContext, chat_id):
    data = await state.get_data()
    laboratory_title = data.get('title_lab')
    laboratory_status = await get_laboratory_status(data)
    laboratory_status_info = (f"Статус лабораторной работы {laboratory_title}, id {laboratory_status.id}:\n\n"
                              f"Состояние сдачи - {laboratory_status.status}\n\n"
                              f"Соятояние просмотра преподавателем - {laboratory_status.additional_status}\n\n"
                              f"Состояние генерации QR кода - {laboratory_status.student_status}\n\n"
                              f"Комментари преподавателя - \n{laboratory_status.lecturer_comment}\n\n"
                              f"Ваши комментарии - \n{laboratory_status.student_comment}\n\n")
    await bot.send_message(text=laboratory_status_info, chat_id=chat_id)
    await menu.main.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*mainMenu)
    await bot.send_message(text="Выберете дейстиве: ", reply_markup=keyboard, chat_id=chat_id)


@dp.message_handler(state=Full_Name.Name)
async def User_Name(message: types.Message, state: FSMContext):
    await state.update_data()

@dp.message_handler(state=menu.stat)
async def statistic(message: types.Message, state: FSMContext):
    await state.update_data(states = message.text)
    if message.text == backButton[0]:
        await menu.main.set()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*mainMenu)
        await message.answer("Выберете дейстиве: ", reply_markup=keyboard)

