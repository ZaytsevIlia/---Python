"""
Написать код, который выполняет пинг веб-ресурсов yandex.ru, youtube.com и преобразовывает результат
из байтовового типа данных в строковый без ошибок для любой кодировки операционной системы.
"""
import chardet
import subprocess
import platform

websites = ['yandex.ru', 'youtube.com']

for website in websites:
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '3', website]
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in process.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))
