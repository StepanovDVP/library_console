from constant import LST_COMMANDS
from handlers import router


def main():
    print('Добро пожаловать в приложение для управления книгами!')
    while True:
        print('\nВыберите действие:')
        for command, description in LST_COMMANDS:
            print(f'{command}. {description}')

        user_input = input('Введите номер действия: ').strip()
        try:
            router.handle(user_input)
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    main()
