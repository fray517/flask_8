"""
Flask приложение для получения случайных вдохновляющих цитат.
Использует рабочие публичные API: Forismatic и FavQs.
"""

import random
import logging
from typing import Dict, Optional, Tuple

import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


API_ENDPOINTS = [
    {
        'name': 'Forismatic',
        'url': 'https://api.forismatic.com/api/1.0/',
        'method': 'get_forismatic'
    },
    {
        'name': 'FavQs',
        'url': 'https://favqs.com/api/qotd',
        'method': 'get_favqs'
    }
]


def get_forismatic() -> Optional[Dict[str, str]]:
    """
    Получает случайную цитату с Forismatic API (русский язык).

    Returns:
        Словарь с ключами 'quote' и 'author' или None при ошибке.
    """
    try:
        params = {
            'method': 'getQuote',
            'format': 'json',
            'lang': 'ru'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36'
        }
        response = requests.get(
            'https://api.forismatic.com/api/1.0/',
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        logger.info('Forismatic: цитата получена')
        
        quote_text = data.get('quoteText', '').strip()
        author_text = data.get('quoteAuthor', '').strip()
        
        # Если автор не указан, используем "Неизвестный автор"
        if not author_text:
            author_text = 'Неизвестный автор'
        
        if quote_text:
            return {
                'quote': quote_text,
                'author': author_text,
                'source': 'Forismatic'
            }
    except requests.Timeout:
        logger.warning('Forismatic: таймаут запроса')
    except requests.RequestException as e:
        logger.error(f'Ошибка при запросе к Forismatic: {e}')
    except (KeyError, TypeError, ValueError) as e:
        logger.error(f'Ошибка при обработке ответа Forismatic: {e}')
    
    return None


def get_favqs() -> Optional[Dict[str, str]]:
    """
    Получает цитату дня с FavQs API (английский язык).

    Returns:
        Словарь с ключами 'quote' и 'author' или None при ошибке.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        response = requests.get(
            'https://favqs.com/api/qotd',
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        logger.info('FavQs: цитата получена')
        
        quote_data = data.get('quote', {})
        quote_text = quote_data.get('body', '').strip()
        author_text = quote_data.get('author', '').strip()
        
        if not author_text:
            author_text = 'Неизвестный автор'
        
        if quote_text:
            return {
                'quote': quote_text,
                'author': author_text,
                'source': 'FavQs'
            }
    except requests.Timeout:
        logger.warning('FavQs: таймаут запроса')
    except requests.RequestException as e:
        logger.error(f'Ошибка при запросе к FavQs: {e}')
    except (KeyError, TypeError, ValueError) as e:
        logger.error(f'Ошибка при обработке ответа FavQs: {e}')
    
    return None


def get_random_quote() -> Tuple[Optional[Dict[str, str]], Optional[str]]:
    """
    Случайным образом выбирает API и получает цитату.

    Returns:
        Кортеж (словарь с цитатой или None, сообщение об ошибке или None).
    """
    api_functions = {
        'get_forismatic': get_forismatic,
        'get_favqs': get_favqs
    }
    
    # Пробуем получить цитату, перебирая API в случайном порядке
    shuffled_apis = list(API_ENDPOINTS)
    random.shuffle(shuffled_apis)
    
    errors = []
    for api in shuffled_apis:
        method_name = api['method']
        if method_name in api_functions:
            try:
                quote = api_functions[method_name]()
                if quote:
                    logger.info(f'Успешно получена цитата с {api["name"]}')
                    return quote, None
            except Exception as e:
                error_msg = f'{api["name"]}: {str(e)}'
                errors.append(error_msg)
                logger.error(error_msg)
    
    error_message = 'Не удалось получить цитату ни с одного API'
    if errors:
        error_message += f'. Ошибки: {"; ".join(errors)}'
    
    return None, error_message


@app.route('/')
def index():
    """Главная страница приложения."""
    quote, error = get_random_quote()
    return render_template('index.html', quote=quote, error=error)


@app.route('/refresh')
def refresh():
    """Обновление цитаты через AJAX."""
    quote, error = get_random_quote()
    if quote:
        return jsonify({
            'success': True,
            'quote': quote['quote'],
            'author': quote['author'],
            'source': quote['source']
        })
    return jsonify({
        'success': False,
        'error': error or 'Неизвестная ошибка'
    }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
