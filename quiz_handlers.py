import asyncio
import random
import aiohttp
from collections import Counter

from aiogram import types
from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router
from aiogram.types import Message
from aiogram.types import CallbackQuery

#################################
from token_data import TOKEN
from questions_bank import bank

##################################
router = Router()

async def start_quiz(message: types.Message, state: FSMContext):
    await state.set_state(QuizStates.START)
    await state.set_data({
        'question_1': None,
        'question_2': None,
        'question_3': None,
        'question_4': None,
        'question_5': None,
        'question_6': None,
        'question_7': None,
        'question_8': None,
        'question_9': None,
        'question_10': None,
    })
class QuizStates(StatesGroup):
    START = State()
    QUESTION_1 = State()
    QUESTION_2 = State()
    QUESTION_3 = State()
    QUESTION_4 = State()
    QUESTION_5 = State()
    QUESTION_6 = State()
    QUESTION_7 = State()
    QUESTION_8 = State()
    QUESTION_9 = State()
    QUESTION_10 = State()
    RESULT = State()
    Feedback = State()

async def download_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            image_data = await response.read()
            print("Image downloaded successfully:", url)
            return image_data

animal_images = {
    "Бурый медведь": "https://sib100.ru/wp-content/uploads/2018/10/Buriy-misha_4.jpg",
    "Горный козёл": "https://redbookrf.ru/wp-content/uploads/2020/12/imgonline-com-ua-resize-lkeb4yshlu.jpg",
    "Зебра": "https://zoopark-vl.ru/wp-content/uploads/2022/12/afrikanskaya-zebra-1.jpg",
    "Пингвин": "https://ic.pics.livejournal.com/solfar_m/24027171/7374/7374_900.jpg"
}


async def send_toteam_animal_image(message: types.Message, totem_animal: str):
    image_url = animal_images.get(totem_animal)
    image_data = await download_image(image_url)
    await message.answer_photo(photo=image_data, caption=f"Ваше тотемное животное: {totem_animal}")


@router.message(lambda message: message.text in animal_images.keys())
async def handle_toteam_animal_message(message: types.Message):
    await send_toteam_animal_image(message, message.text)

def get_most_common_answer_overall(answers):
    question_texts = []
    for answer in answers:
        question_text = answer.split(")", 1)[1].strip()
        question_texts.append(question_text)
    answer_counter = Counter(question_texts)
    most_common_answer_text = answer_counter.most_common(1)

    if most_common_answer_text:
        return most_common_answer_text[0][0]
    else:
        return None

@router.message(lambda message: 'начать викторину' in message.text.lower())
async def command_start_handler(message: Message, state: FSMContext):
    await state.set_state(QuizStates.QUESTION_1)
    await message.answer("Какой из этих природных ландшафтов вы предпочитаете?",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="а) Густой лес"),
                                     KeyboardButton(text="б) Высокие горы"),
                                 ],
                                 [
                                     KeyboardButton(text="в) Широкие просторы пустыни"),
                                     KeyboardButton(text="г) Берег океана"),
                                 ],
                             ],
                             resize_keyboard=True
                         ))



@router.message(lambda message: message.text in ['а) Густой лес', 'б) Высокие горы', 'в) Широкие просторы пустыни', 'г) Берег океана'])
async def handle_question_1_answer(message: types.Message, state: FSMContext):
    answer = message.text
    print("Обработчик вопроса 1")
    await state.update_data(question_1=answer)
    print("Ответ на вопрос 1:", answer)
    await state.set_state(QuizStates.QUESTION_2)
    await message.answer("Какое время суток вам ближе всего?",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="а) Утро"),
                                     KeyboardButton(text="б) День"),
                                 ],
                                 [
                                     KeyboardButton(text="в) Вечер"),
                                     KeyboardButton(text="г) Ночь"),
                                 ],
                             ],
                             resize_keyboard=True
                         ))

@router.message(lambda message: message.text in ['а) Утро', 'б) День', 'в) Вечер', 'г) Ночь'])
async def handle_question_2_answer(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(question_2=answer)
    await state.set_state(QuizStates.QUESTION_3)
    await message.answer("Вы предпочитаете проводить время?",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="а) Один/одна"),
                                     KeyboardButton(text="б) В компании друзей"),
                                 ],
                                 [
                                     KeyboardButton(text="в) С семьей"),
                                     KeyboardButton(text="г) Среди природы"),
                                 ],
                             ],
                             resize_keyboard=True
                         ))

@router.message(lambda message: message.text in ['а) Один/одна', 'б) В компании друзей', 'в) С семьей', 'г) Среди природы'])
async def handle_question_3_answer(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(question_3=answer)
    await state.set_state(QuizStates.QUESTION_4)
    await message.answer("Ваша любимая еда?",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="а) Мясо"),
                                     KeyboardButton(text="б) Фрукты"),
                                 ],
                                 [
                                     KeyboardButton(text="в) Овощи"),
                                     KeyboardButton(text="г) Рыба"),
                                 ],
                             ],
                             resize_keyboard=True
                         ))

@router.message(lambda message: message.text in ['а) Мясо', 'б) Фрукты', 'в) Овощи', 'г) Рыба'])
async def handle_question_4_answer(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(question_4=answer)
    await state.set_state(QuizStates.QUESTION_5)
    await message.answer("Какое свойство вы цените больше всего?",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="а) Сила"),
                                     KeyboardButton(text="б) Ум"),
                                 ],
                                 [
                                     KeyboardButton(text="в) Социальная связь"),
                                     KeyboardButton(text="г) Способность к адаптации"),
                                 ],
                             ],
                             resize_keyboard=True
                         ))

@router.message(lambda message: message.text in ['а) Сила', 'б) Ум', 'в) Социальная связь', 'г) Способность к адаптации'])
async def handle_question_5_answer(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(question_5=answer)
    await state.set_state(QuizStates.QUESTION_6)
    await message.answer("Ваше предпочтение в выборе транспорта?",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="а) Пешком"),
                                     KeyboardButton(text="б) На велосипеде"),
                                 ],
                                 [
                                     KeyboardButton(text="в) На автомобиле"),
                                     KeyboardButton(text="г) На самолете"),
                                 ],
                             ],
                             resize_keyboard=True
                         ))

@router.message(lambda message: message.text in ['а) Пешком', 'б) На велосипеде', 'в) На автомобиле', 'г) На самолете'])
async def handle_question_6_answer(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(question_6=answer)
    await state.set_state(QuizStates.QUESTION_7)
    await message.answer("В какой из предложенных стран вы бы хотели побывать?",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="а) Канада"),
                                     KeyboardButton(text="б) Кения"),
                                 ],
                                 [
                                     KeyboardButton(text="в) Австралия"),
                                     KeyboardButton(text="г) Япония"),
                                 ],
                             ],
                             resize_keyboard=True
                         ))

@router.message(lambda message: message.text in ['а) Канада', 'б) Кения', 'в) Австралия', 'г) Япония'])
async def handle_question_7_answer(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(question_7=answer)
    await state.set_state(QuizStates.QUESTION_8)
    await message.answer("Ваше любимое время года?",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="а) Весна"),
                                     KeyboardButton(text="б) Лето"),
                                 ],
                                 [
                                     KeyboardButton(text="в) Зима"),
                                     KeyboardButton(text="г) Осень"),
                                 ],
                             ],
                             resize_keyboard=True
                         ))

@router.message(lambda message: message.text in ['а) Весна', 'б) Лето', 'в) Зима', 'г) Осень'])
async def handle_question_8_answer(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(question_8=answer)
    await state.set_state(QuizStates.QUESTION_9)
    await message.answer("Какой из этих предметов бы вам хотелось получить в подарок?",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="а) Книга"),
                                     KeyboardButton(text="б) Палатка"),
                                 ],
                                 [
                                     KeyboardButton(text="в) Фотоаппарат"),
                                     KeyboardButton(text="г) Бинокль"),
                                 ],
                             ],
                             resize_keyboard=True
                         ))

@router.message(lambda message: message.text in ['а) Книга', 'б) Палатка', 'в) Фотоаппарат', 'г) Бинокль'])
async def handle_question_9_answer(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(question_9=answer)
    await state.set_state(QuizStates.QUESTION_10)
    await message.answer("Как вы проводите отпуск?",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="а) Активно, на природе"),
                                     KeyboardButton(text="б) Путешествуя по городам и странам"),
                                 ],
                                 [
                                     KeyboardButton(text="в) Отдыхая на пляже"),
                                     KeyboardButton(text="г) В горном курорте"),
                                 ],
                             ],
                             resize_keyboard=True
                         ))

@router.message(lambda message: message.text in ['а) Активно, на природе', 'б) Путешествуя по городам и странам', 'в) Отдыхая на пляже', 'г) В горном курорте'])
async def handle_question_10_answer(message: types.Message, state: FSMContext):
    answer = message.text.split(")")[0].strip()[-1]
    await state.update_data(question_10=answer)
    button1 = InlineKeyboardButton(text="О нас", callback_data="about")
    button2 = InlineKeyboardButton(text="Обратная связь", callback_data="feedback")
    button3 = InlineKeyboardButton(text="Telegram", callback_data="webs", url = 'https://t.me/Moscowzoo_official')
    button4 = InlineKeyboardButton(text="VK", callback_data="webs", url = 'https://vk.com/moscow_zoo')
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1, button2,button3, button4]])
    data = await state.get_data()
    all_answers = [data[f"question_{i}"] for i in range(1, 11)]
    answer_counter = Counter(all_answers)
    most_common_answer = answer_counter.most_common(1)[0][0]
    totem_animal = {
        'а': "Бурый медведь",
        'б': "Горный козёл",
        'в': "Зебра",
        'г': "Пингвин"
    }.get(answer)
    animal_image_url = animal_images.get(totem_animal)
    await state.update_data(totem_animal=totem_animal)
    await state.set_state(QuizStates.RESULT)
    await message.answer(f"Спасибо за участие в викторине! Мы получили ваши ответы.\n"
                         f"Ваше тотемное животное: {totem_animal}\n"
                         f"<a href='{animal_image_url}'>&#8205;</a>",  # Вставляем изображение с помощью HTML
                         parse_mode='HTML',
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="Начать заново"),
                                 ],
                             ],
                             resize_keyboard=True
                         ))
    await message.answer("Вот информация о нас и обратная связь:", reply_markup=inline_keyboard)



@router.callback_query(lambda query: query.data == 'about')
async def process_about_callback(query: types.CallbackQuery):
    await query.answer()
    await query.message.answer("Московский зоопарк — один из старейших зоопарков Европы с уникальной коллекцией животных и профессиональным сообществом."
                         "Важная задача зоопарка — вносить вклад в сохранение биоразнообразия планеты."
                         "При нынешних темпах развития цивилизации к 2050 году могут погибнуть около "
                         "10 000 биологических видов. Московский зоопарк пытается сохранить их."
                         "«Возьми животное под опеку» («Клуб друзей») — это одна из программ, помогающих "
                         "зоопарку заботиться о его обитателях."
                         " Программа позволяет с помощью пожертвования на любую сумму внести свой вклад"
                         " в развитие зоопарка и сохранение биоразнообразия планеты.")

@router.callback_query(lambda query: query.data == 'feedback')
async def process_feedback_callback(query: types.CallbackQuery):
    await query.answer()
    await query.message.answer("Для обратной связи, пожалуйста, напишите нам на адрес: directorzoo@culture.mos.ru")


async def send_toteam_animal_image(message: types.Message, totem_animal: str):
    image_url = animal_images.get(totem_animal)
    image_data = await download_image(image_url)
    await message.answer_photo(photo=image_data, caption=f"Ваше тотемное животное: {totem_animal}")

@router.message(lambda message: message.text in animal_images.keys())
async def handle_toteam_animal_message(message: types.Message):
    await send_toteam_animal_image(message, message.text)

@router.message(lambda message: message.text == "Начать заново")
async def start_over_text(message: types.Message, state: FSMContext):
    await state.set_state(QuizStates.START)
    await message.answer("Начинаем викторину заново! Какой из этих природных ландшафтов вы предпочитаете?",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="а) Густой лес"),
                                     KeyboardButton(text="б) Высокие горы"),
                                 ],
                                 [
                                     KeyboardButton(text="в) Широкие просторы пустыни"),
                                     KeyboardButton(text="г) Берег океана"),
                                 ],
                             ],
                             resize_keyboard=True
                         ))

@router.message(lambda message: message.text == "Начать заново")
async def feedback_handler(query: types.CallbackQuery):
    # Отправляем пользователю сообщение с приветствием и предложением написать свой вопрос или отзыв
    await query.message.answer("Спасибо за обратную связь! Напишите ваш вопрос или отзыв, и мы постараемся ответить вам как можно скорее.")
    # Сохраняем в состоянии информацию о том, что пользователь хочет отправить обратную связь
    await state.set_state(States.FEEDBACK)


