from aiogram.fsm.state import State, StatesGroup

class UploadTrack(StatesGroup):
    waiting_audio = State()
    waiting_title = State()
    waiting_picture = State()
    waiting_main_genre = State()
    waiting_genre = State()
    waiting_tags = State()
    waiting_description = State()
    waiting_privacy = State()
    final = State()
class Settings(StatesGroup):
    main_menu = State()