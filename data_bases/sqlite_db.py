import sqlite3 as sq

from create_bot import bot


def sql_start():
    global base, curs
    base = sq.connect('pizza_cool.db')
    curs = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        curs.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in curs.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОпис: {ret[2]}\nЦіна {ret[-1]}')


async def sql_read2():
    return curs.execute('SELECT * FROM menu').fetchall()


async def sql_delete_command(data):
    curs.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()
