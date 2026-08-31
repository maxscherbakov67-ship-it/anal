from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="Загрузить трек"), KeyboardButton(text="Авторизация")]
        [KeyboardButton(text="Помощь"), KeyboardButton(text="История загрузок")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def main_genre_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Электроника / EDM", callback_data="genre_electro"),
            InlineKeyboardButton(text="Hip-Hop / Rap / Trap", callback_data="genre_hiprap"),
        ],
        [
            InlineKeyboardButton(text="Рок / Метал / Альтернатива", callback_data="genre_rock"),
            InlineKeyboardButton(text="Поп / R&B / Соул", callback_data="genre_pop"),
        ],
        [
            InlineKeyboardButton(text="Джаз / Классика / Эмбиент", callback_data="genre_jazz"),
            InlineKeyboardButton(text="Регги / Саундтреки / Другое", callback_data="genre_reggae"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard=keyboard)

def electro_genre_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Electronic", callback_data="genre_Electronic"),
            InlineKeyboardButton(text="Dance / EDM", callback_data="genre_Dance"),
        ],
        [
            InlineKeyboardButton(text="House", callback_data="genre_House"),
            InlineKeyboardButton(text="Deep House", callback_data="genre_Deep House"),
        ],
        [
            InlineKeyboardButton(text="Tech House", callback_data="genre_Tech House"),
            InlineKeyboardButton(text="Progressive House", callback_data="genre_Progressive House"),
        ],
        [
            InlineKeyboardButton(text="Techno", callback_data="genre_Techno"),
            InlineKeyboardButton(text="Trance", callback_data="genre_Trance"),
        ],
        [
            InlineKeyboardButton(text="Dubstep", callback_data="genre_Dubstep"),
            InlineKeyboardButton(text="Drum & Bass", callback_data="genre_Drum & Bass"),
        ],
        [
            InlineKeyboardButton(text="Назад в меню", callback_data="genre_backtomenu")
        ],
    ]
    return InlineKeyboardMarkup(keyboard=keyboard)

def hiphop_genre_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Hip-Hop", callback_data="genre_Hip-Hop"),
            InlineKeyboardButton(text="Rap", callback_data="genre_Rap"),
        ],
        [
            InlineKeyboardButton(text="Trap", callback_data="genre_Trap"),
        ],
        [
            InlineKeyboardButton(text="Назад в меню", callback_data="genre_backtomenu")
        ],
    ]
    return InlineKeyboardMarkup(keyboard=keyboard)

def rock_genre_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Rock", callback_data="genre_Rock"),
        ],
        [
            InlineKeyboardButton(text="Metal", callback_data="genre_Metal"),
        ],
        [
            InlineKeyboardButton(text="Alternative", callback_data="genre_Alternative"),
        ],
        [
            InlineKeyboardButton(text="Назад в меню", callback_data="genre_backtomenu")
        ],
    ]
    return InlineKeyboardMarkup(keyboard=keyboard)

def pop_genre_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Pop", callback_data="genre_Pop"),
        ],
        [
            InlineKeyboardButton(text="R&B", callback_data="genre_R&B"),
            InlineKeyboardButton(text="Soul", callback_data="genre_Soul"),
        ],
        [
            InlineKeyboardButton(text="Назад в меню", callback_data="genre_backtomenu")
        ],
    ]
    return InlineKeyboardMarkup(keyboard=keyboard)

def jazz_genre_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Jazz", callback_data="genre_Jazz"),
        ],
        [
            InlineKeyboardButton(text="Classical", callback_data="genre_Classical"),
        ],
        [
            InlineKeyboardButton(text="Ambient", callback_data="genre_Ambient"),
        ],
        [
            InlineKeyboardButton(text="Назад в меню", callback_data="genre_backtomenu")
        ],
    ]
    return InlineKeyboardMarkup(keyboard=keyboard)

def reggae_genre_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Reggae / Dancehall", callback_data="genre_Reggae / Dancehall"),
        ],
        [
            InlineKeyboardButton(text="Soundtrack", callback_data="genre_Soundtrack"),
        ],
        [
            InlineKeyboardButton(text="Folk", callback_data="genre_Folk"),
        ],
        [
            InlineKeyboardButton(text="Audiobook / Podcast", callback_data="genre_Audiobook / Podcast"),
        ],
        [
            InlineKeyboardButton(text="Назад в меню", callback_data="genre_backtomenu")
        ],
    ]
    return InlineKeyboardMarkup(keyboard=keyboard)

def privacy_keyboard() -> InlineKeyboardMarkup:
    keyboard=[
        [
            InlineKeyboardButton(text="Публичный", callback_data="privacy_public"),
            InlineKeyboardButton(text="Доступ по ссылке", callback_data="privacy_hidden")
        ],
        [
            InlineKeyboardButton(text="Назад в меню", callback_data="genre_backtomenu")
        ],
    ]
    return InlineKeyboardMarkup(keyboard=keyboard)

def goback_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Назад", callback_data="goback")
        ],
    ]
    return InlineKeyboardMarkup(keyboard=keyboard)
