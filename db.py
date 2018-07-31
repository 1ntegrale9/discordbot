import discord

DEVELOPER = discord.User(id='314387921757143040')

def command_db(r, msg):
    """
    /db Key
    /db Key Value
    /db -help
    /db -flushall
    /db -flushdb
    /db -list
    /db -delete Key
    /db -delete Key Value
    """
    args = msg.content.split()
    id = msg.server.id
    if len(args) == 2:
        if args[1] == '-help':
            return help()
        if args[1] == '-list':
            return get_keys(r, id)
        if args[1] == '-flushall':
            if msg.author == DEVELOPER:
                return flushall(r)
            return '開発者のみ実行可能なコマンドです。'
        if args[1] == '-flushdb':
            if msg.author == DEVELOPER:
                return flushdb(r)
            return '開発者のみ実行可能なコマンドです。'
        else:
            return get_values(r, id, args[1])
    elif len(args) == 3:
        if args[1] == '-delete':
            return del_key(r, id, args[2])
        else:
            return set_value(r, id, args[1], args[2])
    elif len(args) == 4:
        if args[1] == '-delete':
            return del_value(r, id, args[2], args[3])
        else:
            '不正な形式です。'
    else:
        return '不正な形式です。'


def get_keys(r, id):
    if r.exists(id):
        data = r.smembers(id)
        return normalize(data)
    return 'データが存在しません。'


def get_values(r, id, k):
    key = f'{id}:{k}'
    if r.exists(key):
        data = r.smembers(key)
        return normalize(data)
    return f'{k} は存在しません。'


def set_value(r, id, k, v):
    r.sadd(f'{id}:{k}', v)
    r.sadd(id, k)
    return f'{k} に {v} を追加しました。'


def del_key(r, id, k):
    key = f'{id}:{k}'
    if r.exists(key):
        r.delete(key)
        r.srem(id, k)
        return f'{k} を削除しました。'
    return f'{k} は存在しません。'


def del_value(r, id, k, v):
    key = f'{id}:{k}'
    if r.exists(key):
        r.srem(key, v)
        return f'{k} から {v} を削除しました。'
    return f'{k} は存在しません。'


def flushall(r):
    r.flushall()
    return 'Deleted all keys in all databases on the current host.'


def flushdb(r):
    r.flushdb()
    return 'Deleted all keys in the current database.'


def help():
    return '後で書く'


def normalize(data):
    return ' '.join(sorted([d.decode() for d in data]))