def get_int_input(prompt: str, error_msg: str = 'Укажите число!') -> int:
    """Обработка ввода числового значения."""
    try:
        return int(input(prompt))
    except ValueError:
        raise ValueError(error_msg)


def get_choice_input(
        prompt: str, valid_choices: list,
        error_msg: str = 'Неверный выбор.'
) -> str:
    """Обработка ввода выбора из нескольких вариантов."""

    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        else:
            print(error_msg)
