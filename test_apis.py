"""
Тестовый скрипт для проверки работы API цитат.
"""

import requests
import json
import sys

# Устанавливаем UTF-8 для вывода
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def test_zenquotes():
    """Тестирует ZenQuotes API."""
    print('\n=== Тест ZenQuotes ===')
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36'
        }
        response = requests.get(
            'https://zenquotes.io/api/random',
            headers=headers,
            timeout=10
        )
        print(f'Статус: {response.status_code}')
        print(f'Заголовки: {dict(response.headers)}')
        data = response.json()
        print(f'Ответ: {json.dumps(data, indent=2, ensure_ascii=False)}')
        return True
    except Exception as e:
        print(f'Ошибка: {e}')
        return False


def test_api_ninjas():
    """Тестирует API Ninjas."""
    print('\n=== Тест API Ninjas ===')
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        response = requests.get(
            'https://api-ninjas.com/api/quotes',
            headers=headers,
            timeout=10
        )
        print(f'Статус: {response.status_code}')
        print(f'Заголовки: {dict(response.headers)}')
        if response.status_code == 200:
            data = response.json()
            print(f'Ответ: {json.dumps(data, indent=2, ensure_ascii=False)}')
        else:
            print(f'Текст ответа: {response.text}')
        return response.status_code == 200
    except Exception as e:
        print(f'Ошибка: {e}')
        return False


def test_quoteslate():
    """Тестирует QuotesLate API."""
    print('\n=== Тест QuotesLate ===')
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        # Пробуем разные endpoints
        endpoints = [
            'https://quoteslate.vercel.app/api/random',
            'https://quoteslate.vercel.app/'
        ]
        for endpoint in endpoints:
            try:
                response = requests.get(
                    endpoint,
                    headers=headers,
                    timeout=10
                )
                print(f'Статус ({endpoint}): {response.status_code}')
                content_type = response.headers.get('Content-Type', '')
                print(f'Content-Type: {content_type}')
                if 'application/json' in content_type:
                    data = response.json()
                    print(f'Ответ: {json.dumps(data, indent=2, ensure_ascii=False)}')
                    return True
                else:
                    print(f'Получен HTML вместо JSON (первые 200 символов):')
                    print(response.text[:200])
            except Exception as e:
                print(f'Ошибка для {endpoint}: {e}')
        return False
    except Exception as e:
        print(f'Ошибка: {e}')
        return False


def test_quotable():
    """Тестирует Quotable API."""
    print('\n=== Тест Quotable ===')
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        response = requests.get(
            'https://api.quotable.io/random',
            headers=headers,
            timeout=10
        )
        print(f'Статус: {response.status_code}')
        print(f'Заголовки: {dict(response.headers)}')
        data = response.json()
        print(f'Ответ: {json.dumps(data, indent=2, ensure_ascii=False)}')
        return True
    except Exception as e:
        print(f'Ошибка: {e}')
        return False


if __name__ == '__main__':
    print('Тестирование API цитат...')
    results = {
        'ZenQuotes': test_zenquotes(),
        'QuotesLate': test_quoteslate(),
        'Quotable': test_quotable(),
        'API Ninjas': test_api_ninjas()
    }
    
    print('\n=== Результаты ===')
    for api, success in results.items():
        status = '[OK] Работает' if success else '[FAIL] Не работает'
        print(f'{api}: {status}')

