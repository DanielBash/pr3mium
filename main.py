import sqlite3
from telethon import TelegramClient, events
import asyncio
import random

API_ID = 0
API_HASH = "hash"
SESSION_NAME = "userbot"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
db = {'messages': {}, 'me': None}
animations = {
    'загрузка': {
        'frames': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'] * 3,
        'speed': 0.1
    }
}
recording = False
current_recording = {}

async def log(message):
    await client.send_message('me', f'[pr3mium] {message}')
    print(message)

async def animate(event, animation):
    for frame in animation['frames']:
        await event.edit(frame)
        await asyncio.sleep(animation['speed'])

async def effect(event, text):
    for i in range(len(text)):
        if text[i] not in '\n \t':
            await event.edit(text[:i+1])
            await asyncio.sleep(0.05)

async def handle_command(event):
    global recording, current_recording
    text = event.raw_text
    if text.startswith('/п'):
        await log('Хьюстон, у нас нет проблем!')
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
            await log('Использование: /э[ффетно] <текст>')
            return
        await effect(event, parts[1])
    elif text.startswith('/с'):
        await log('Pr3mium - бот: /п, /а, /э, /с')

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