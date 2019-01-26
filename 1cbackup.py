# импорт необходимых модулей и объявление переменных
import os
import subprocess
import datetime

AppData = os.environ['appdata']
ProgramFiles = os.environ['programfiles']
ArchivTime = datetime.date.today()
VBases = open(AppData + '\\1C\\1CEStart\\ibases.v8i', "r", encoding = 'utf-8')

# считываем данные из конфигурационного файла
LineFile = VBases.readline()
while LineFile:
    i = 0
    # получаем название базы и создаем имя архива
    while len(LineFile) > i:
        if LineFile[i] == '[':
            BaseName = LineFile[i+1:-2]
            ArchivName = (str(BaseName) + "_"+ str(ArchivTime))
            break
        else:
            i += 1
    #  находим путь к базе и архивируем базу
    if LineFile[0:12] == "Connect=File":
        PathBase = LineFile[14:-2].replace('\\', '/')
        print(PathBase)
        ArchivingBase = subprocess.call(["C:/Program Files/7-Zip/7z.exe", "a", "-tzip", "-ssw", "-mx7", ArchivName, PathBase])
    LineFile = VBases.readline()

VBases.close()