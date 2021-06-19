import os.path
import time
from dataclasses import dataclass
from functools import wraps
from typing import Tuple, Any, Dict, Callable

if not os.path.exists('log_info') and not os.path.exists('log_error'):
    os.mkdir('log_info')
    os.mkdir('log_error')


@dataclass
class LogfileCount:
    log_info: str = 'log_info/log-info_1.log'
    log_error: str = 'log_error/log-error_1.log'
    log_info_num: int = 1
    log_error_num: int = 1


def log_decorator(row: int, module: str, arguments: Tuple[str, ...]) -> Callable:
    """
    Декоратор для логирования, формат лога:
                                Модуль
                                Имя функции
                                Строка начала функции
                                Дата и время логирования
                                Строка документации
                                Аргументы
                                Возвращаемое значение или Тип ошибки
    :param row: Строка объявления функции или метода
    :param module: Модуль в котором находится функция или метод
    :param arguments: Аргументы функции или метода
    :return: Декоратор
    """

    def decorator(func: Callable) -> Callable:
        cache = {}

        @wraps(func)
        async def wrapper(*args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Callable:
            try:
                key = f'{args + tuple(sorted(kwargs.items()))}'
                if key not in cache:
                    cache[key] = await func(*args, **kwargs)
                open(LogfileCount.log_info, 'a').close()
                if os.path.getsize(LogfileCount.log_info) > 5e+6:
                    LogfileCount.log_info_num += 1
                    LogfileCount.log_info = LogfileCount.log_info.replace(f'{LogfileCount.log_info_num - 1}',
                                                                          f'{LogfileCount.log_info_num}')
                with open(LogfileCount.log_info, 'a', encoding='UTF-8') as file:
                    data = f'DateTime: {time.asctime()}  Module: {module}  Function: {func.__name__}  Row: {row}\n' \
                           f'Doc: {func.__doc__}\nArguments: {*arguments, args, kwargs}\nReturn: {cache[key]}\n\n'
                    file.write(data)

                return cache[key]

            except Exception as e:

                open(LogfileCount.log_error, 'a').close()
                if os.path.getsize(LogfileCount.log_error) > 5e+6:
                    LogfileCount.log_error_num += 1
                    LogfileCount.log_error = LogfileCount.log_error.replace(f'{LogfileCount.log_error_num - 1}',
                                                                            f'{LogfileCount.log_error_num}')
                with open(LogfileCount.log_error, 'a', encoding='UTF-8') as file:
                    data = f'DateTime: {time.asctime()}  Module: {module}  Function: {func.__name__}  Row: {row}\n' \
                           f'Doc: {func.__doc__}\nArguments: {*arguments, args, kwargs}\nException: {Exception(e),}\n\n'
                    file.write(data)
                raise

        return wrapper

    return decorator
