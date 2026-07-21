import sqlite3
from telethon import TelegramClient, events
import asyncio
import random

API_ID = a
API_HASH = "a"
SESSION_NAME = "userbot"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
db = {'messages': {}, 'me': None}
animations = {
    'загрузка': {
        'frames': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'] * 3,
        'speed': 0.0
    }
}
recording = False
current_recording = {}

_heart_mask = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,0,0,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,0,1,1,1,1,1,1,0,0],
    [0,0,0,1,1,1,1,0,0,0],
    [0,0,0,0,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
]

_W  = '🤍'
_R  = '❤️'
_hc = ['❤️','🧡','💛','💚','💙','💜','🤎','🖤','🤍','💖']
_rc = _hc

_love_frames = []

for _f in range(12):
    _t = _f / 11.0
    _rows = []
    for _row in _heart_mask:
        _ch = []
        for _v in _row:
            if _v:
                _ch.append(_R if random.random() < _t else random.choice(_rc))
            else:
                _ch.append(random.choice(_rc)
                           if random.random() < (1 - _t) * 0.4
                           else _W)
        _rows.append(''.join(_ch).rstrip())
    _love_frames.append('\n'.join(_rows))

_yv = ['You', 'yOu', 'yoU']
for _i in range(10):
    _love_frames.append(f"I {_hc[_i % 10]} {_yv[_i % 3]}")
_w = "Love"
for _k in range(30):
    _rows = []
    for _r in range(8):
        _ch = []
        for _c in range(10):
            _p = _r * 10 + (_c if _r % 2 == 0 else 9 - _c)
            _ch.append(_w[(_p + _k) % 4])
        _rows.append(''.join(_ch).rstrip())
    _love_frames.append('\n'.join(_rows))

_love_frames.append("Любовь морковь")

animations['любовь'] = {
    'frames': _love_frames,
    'speed': 0.1
}

_fuck_frames = []

for _emoji in ['✊', '🖐', '✌️', '🖕']:
    for _ in range(3):
        _fuck_frames.append(_emoji)
for _ in range(6):
    _fuck_frames.append('🤨🖕')
    _fuck_frames.append('🤨🖕')
    _fuck_frames.append('🖕🤨')
    _fuck_frames.append('🖕🤨')

_kao_1 = '╭∩╮(•̀_·́)╭∩╮'
_kao_2 = '╭∩╮(·́_•̀)╭∩╮'
for _ in range(3):
    _fuck_frames.append(_kao_1)
    _fuck_frames.append(_kao_1)
    _fuck_frames.append(_kao_2)
    _fuck_frames.append(_kao_2)


_txt = 'ᶠᶸᶜᵏᵧₒᵤ!🖕'
for _i in range(1, len(_txt) + 1):
    _fuck_frames.append(_txt[:_i])
    _fuck_frames.append(_txt[:_i])

animations['фак'] = {
    'frames': _fuck_frames,
    'speed': 0.1
}

async def log(message):
    await client.send_message('me', f'[pr3mium] {message}')
    print(message)

async def animate(event, animation):
    for frame in animation['frames']:
        try:
            await event.edit(frame)
        except Exception:
            pass
        await asyncio.sleep(animation['speed'])

async def effect(event, text):
    for i in range(len(text)):
        if text[i] not in '\n \t':
            try:
                await event.edit(text[:i+1])
            except Exception:
                pass
            await asyncio.sleep(0.05)

async def handle_command(event):
    global recording, current_recording
    text = event.raw_text
    if text.startswith('/п'):
        await evend.edit('Хьюстон, у нас нет проблем!')
        await event.delete()
    elif text.startswith('/а'):
        if text == '/а':
            await event.edit('/а <название> — проиграть\n/а список\n/а запись <название> <скорость>\n/а стоп\n/а удалить <название>')
            return
        args = text[3:].strip()
        if args == 'список':
            if animations:
                lines = [f'{name} ({len(a["frames"])} кадров)' for name, a in animations.items()]
                await event.edit('Анимации:\n' + '\n'.join(lines))
            else:
                await event.edit('Нет сохранённых анимаций.')
        elif args.startswith('запись '):
            rest = args[7:].strip()
            parts = rest.rsplit(maxsplit=1)
            if len(parts) != 2:
                await event.edit('Использование: /а запись <название> <скорость>')
                return
            name, speed_str = parts
            try:
                speed = float(speed_str)
            except ValueError:
                await event.edit('Скорость должна быть числом.')
                return
            if recording:
                await event.edit(f'Идёт запись "{current_recording["name"]}". Остановите: /а стоп')
                return
            recording = True
            current_recording = {'name': name, 'speed': speed, 'frames': []}
            await event.edit(f'Запись "{name}" начата (скорость {speed}). Отправляйте сообщения.')
        elif args == 'стоп':
            if not recording:
                await event.edit('Нет активной записи.')
                return
            animations[current_recording['name']] = {
                'frames': current_recording['frames'][:],
                'speed': current_recording['speed']
            }
            count = len(current_recording['frames'])
            name = current_recording['name']
            recording = False
            current_recording = {}
            await event.edit(f'Анимация "{name}" сохранена, {count} кадров.')
        elif args.startswith('удалить '):
            name = args[8:].strip()
            if name in animations:
                del animations[name]
                await event.edit(f'Анимация "{name}" удалена.')
            else:
                await event.edit(f'Анимация "{name}" не найдена.')
        else:
            if args in animations:
                await animate(event, animations[args])
            else:
                await event.edit(f'Анимация "{args}" не найдена.')
    elif text.startswith('/э'):
        parts = text.split(maxsplit=1)
        if len(parts) != 2:
            await event.edit('Использование: /э[ффетно] <текст>')
            return
        await effect(event, parts[1])
    elif text.startswith('/с'):
        await event.edit('Pr3mium - бот: /п, /а, /э, /с')

@client.on(events.NewMessage(outgoing=True))
async def on_my_message(event):
    global recording, current_recording
    if recording and not event.raw_text.startswith('/'):
        current_recording['frames'].append(event.raw_text)
        return
    if event.raw_text.startswith('/'):
        await handle_command(event)

@client.on(events.NewMessage)
async def on_new(event):
    key = event.id
    db['messages'][key] = {
        'chat_id': event.chat_id,
        'message_id': event.id,
        'sender_id': event.sender_id,
        'text': event.raw_text or "",
    }

@client.on(events.MessageDeleted)
async def on_deleted(event):
    chat_id = event.chat_id
    for msg_id in event.deleted_ids:
        key = msg_id
        if key in db['messages']:
            if db['messages'][key]['sender_id']:
                sender = await client.get_entity(db['messages'][key]['sender_id'])
                await log(f'Удалено сообщение от @{sender.username}. Текст: {db["messages"][key]["text"]}')
            else:
                await log(f'Удалено сообщение от Анонима. Текст: {db["messages"][key]["text"]}')

async def main():
    await client.start()
    me = await client.get_me()
    db['me'] = me
    username = me.username or "Анонимус"
    await log(f'Телеграм pr3mium активирован для пользователя: @{username}')

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()