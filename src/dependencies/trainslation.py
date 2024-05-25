from fastapi import Depends
from pydantic_i18n import PydanticI18n


def get_translations_dict() -> dict[str, dict[str, str]]:
    return {
        "ru_RU": {
            "String should match pattern '{}'": "Строка должна подходить под паттерн '{}'",
            "Field required": "Обязательное поле",
            "String should have at least {} characters": "Строка должна содержать минимум {} символов",
            "value is not a valid email address: The email address is not valid. It must have exactly one @-sign.": (
                "Адрес электронной почты недействителен. В нем должен быть ровно один символ '@'"
            ),
            "value is not a valid email address: The part after the @-sign is not valid. It should have a period.": (
                "Часть после символа '@' недопустима. В ней должна быть точка"
            ),
            "value is not a valid email address: The email address contains invalid characters before the @-sign: SPACE.": (
                "Адрес электронной почты содержит недопустимые символы перед символом '@': ПРОБЕЛ."
            ),
            "value is not a valid email address: The part after the @-sign contains invalid characters: SPACE.": (
                "Часть после символа '@' содержит недопустимые символы: ПРОБЕЛ."
            )
        },
    }


def get_errors_translator(
    translations_dict: dict[str, dict[str, str]] = Depends(get_translations_dict)
) -> PydanticI18n:
    return PydanticI18n(translations_dict, default_locale="ru_RU")


def get_register_form_loc_map_ru() -> dict[str, str]:
    return {
        "login": "Логин",
        "password": "Пароль",
        "display_name": "Отображаемое имя",
        "email": "Почта",
    }
