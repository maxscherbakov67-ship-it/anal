from os import makedirs
from aiogram import Router, F, Bot
from aiogram.filters import Command, or_f
from aiogram.types import FSInputFile, Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from services.wallet_service import get_or_create_wallet
from services.audius_api import upload_track, AudiusError
from services.wallet_service import get_or_create_wallet
from bot.texts import (
    welcomemsg,
    helpmsg,
    authmsg,
    uploadmsg,
    uploadtracktitle,
    uploadtrackdescription,
    uploadtracksubgenre,
    uploadtrackgenre,
    uploadtrackpicture,
    uploadtracktags,
    uploadtrackprivacy,
    cancelmsg,
    uploadbasemsg
)
from bot.keyboards import (
    main_menu_keyboard,
    main_genre_keyboard,
    electro_genre_keyboard,
    hiphop_genre_keyboard,
    rock_genre_keyboard,
    pop_genre_keyboard,
    jazz_genre_keyboard,
    reggae_genre_keyboard,
    privacy_keyboard,
    goback_keyboard
)
from bot.states import UploadTrack

router = Router()

@router.message(Command("start"))
async def cmd_start(message):
    '''photo = FSInputFile("assets/welcome.png")
    await message.answer_photo(photo=photo,caption=welcomemsg,
                                reply_markup=main_menu_keyboard())'''
    await message.answer(welcomemsg, reply_markup=main_menu_keyboard())
@router.message(or_f(Command("help"), F.text == "Помощь"))
async def cmd_help(message):
    await message.answer(helpmsg)
@router.message(F.text == "Авторизация")
async def cmd_auth(message):
#    await message.answer(authmsg)
    wallet = await get_or_create_wallet(message.from_user.id)
    if wallet["is new"]:
        text = (
            "Добро пожаловать!\n"
            "Для тебя был создан криптокошелёк:\n"
            f"<code>{wallet['wallet_address']}</code>"
        )
    else:
        text = (
            "С возвращением!"
            f"Я обнаружил твой кошелёк: <code>{wallet['wallet_address']}</code>"
        )

    await message.answer(text, parse_mode="HTML", reply_markup=main_menu_keyboard())
@router.message(or_f(Command("upload"), F.text == "Загрузить трек"))
async def cmd_upload(message, state: FSMContext):
    await state.set_state(UploadTrack.waiting_audio)
    await message.answer(uploadmsg)
@router.message(F.text == "История загрузок")
async def cmd_uploadbase(message):
    await message.answer(uploadbasemsg)
@router.message(Command("cancel"))
async def cmd_cancel(message, state: FSMContext):
    await state.clear()
    await message.answer(cancelmsg)
@router.message(F.audio, 
                UploadTrack.waiting_audio)
async def gotaudio(message: Message, state: FSMContext):
    await state.update_data(file_id=message.audio.file_id)
    await state.set_state(UploadTrack.waiting_title)
    await message.answer(uploadtracktitle)
'''@router.message(UploadTrack.waiting_title)
async def gottitle(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(UploadTrack.waiting_main_genre)
    await message.answer(uploadtrackgenre,
                         reply_markup=main_genre_keyboard())'''
@router.message(UploadTrack.waiting_title)
async def gottitle(message: Message, state: FSMContext): # Добавили : Message
    try:
        # Сохраняем текст названия
        await state.update_data(title=message.text)
        
        # Переводим в состояние выбора жанра
        await state.set_state(UploadTrack.waiting_main_genre)
        
        # Генерируем клавиатуру в отдельную переменную
        kb = main_genre_keyboard()
        
        # Отправляем сообщение
        await message.answer(text=uploadtrackgenre, reply_markup=kb)
        
    except Exception as e:
        # Если бот упадет, он хотя бы напишет ошибку прямо в чат, и мы поймем, в чем дело
        await message.answer(f"⚠️ Произошла ошибка внутри хэндлера названия: {e}")

@router.callback_query(UploadTrack.waiting_main_genre,
                       F.data.startswith("genre_"))
async def gotmaingenre(callback: CallbackQuery, state:FSMContext):
    callback_data = callback.data
    #await state.set_state(UploadTrack.waiting_genre)

    if callback_data == "genre_electro":
        keyboard = electro_genre_keyboard()
    elif callback_data == "genre_hiprap":
        keyboard = hiphop_genre_keyboard()
    elif callback_data == "genre_rock":
        keyboard = rock_genre_keyboard()
    elif callback_data == "genre_pop":
        keyboard = pop_genre_keyboard()
    elif callback_data == "genre_jazz":
        keyboard = jazz_genre_keyboard()
    elif callback_data == "genre_reggae":
        keyboard = reggae_genre_keyboard()
    elif callback_data == "genre_backtomenu":
            await callback.message.edit_text("🎵 Выбери группу:", 
                                             reply_markup=main_genre_keyboard())
            await callback.answer()
            return
    else :
        genre = callback_data.replace("genre_", "")
        await state.update_data(genre=genre)
        await state.set_state(UploadTrack.waiting_description)
        await callback.message.edit_text(f"Выбран жанр:{genre}")
        await callback.message.answer(uploadtrackdescription)
        await callback.answer()
        return
    await callback.message.edit_text(uploadtracksubgenre,
                           reply_markup=keyboard)
    await callback.answer()

@router.message(UploadTrack.waiting_description)
async def gotdescription(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(UploadTrack.waiting_tags)
    await message.answer(uploadtracktags)
@router.message(UploadTrack.waiting_tags)
async def gottags(message: Message, state: FSMContext):
    await state.update_data(tags=message.text)
    await state.set_state(UploadTrack.waiting_picture)
    await message.answer(uploadtrackpicture)
@router.message(UploadTrack.waiting_picture, F.photo)
async def gotpicture_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    await state.update_data(cover_file_id=photo.file_id)
    await state.set_state(UploadTrack.waiting_privacy)
    await message.answer(uploadtrackprivacy, reply_markup=privacy_keyboard())
@router.message(UploadTrack.waiting_picture, F.document)
async def gotpicture(message: Message, state: FSMContext):
    mime_type = message.document.mime_type
    if mime_type not in ["image/jpeg", "image/png", "image/webp"]:
        await message.answer("Это не изображение, отправьте файл формата jpeg/png/webp")
        return
    await state.update_data(cover_file_id=message.document.file_id)
    await state.set_state(UploadTrack.waiting_privacy)
    await message.answer(uploadtrackprivacy,
                         reply_markup=privacy_keyboard())
@router.callback_query(UploadTrack.waiting_privacy)
async def gotprivacy(callback: CallbackQuery, state: FSMContext):
    callback_data = callback.data.replace("privacy_", "")
    await callback.answer()
    await state.set_state(UploadTrack.final)
    await state.update_data(privacy=callback_data)
    await callback.message.edit_text("Начинаю загрузку трека на площадку")
@router.callback_query(UploadTrack.final, F.data.startswith("privacy_"))
async def uploading(callback, state: FSMContext, bot: Bot):
    data = await state.get_data()
    file_id = data.get("file_id")
    title = data.get("title")
    genre = data.get("genre")
    description = data.get("description")
    tags = data.get("tags")
    cover_file_id = data.get("cover_file_id")
    privacy = data.get("privacy")
    audio_file = await bot.get_file(file_id)
    audio_path = f"tempfiles/{file_id}.mp3"

   