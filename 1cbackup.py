import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design  # Это наш конвертированный файл дизайна

import os
import subprocess
import datetime
import re

class ExampleApp(QtWidgets.QDialog, design.Ui_Dialog):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.buttonBox.accepted.connect(self.shutdownYes)
        self.buttonBox.rejected.connect(self.shutdownNo)

    # основная функция создания копии базы
    def createBackup(self):
        AppData = os.environ["appdata"]
        ArchivTime = datetime.date.today()
        VBases = open(AppData + "\\1C\\1CEStart\\ibases.v8i", "r", encoding='utf-8')

        # открываем конфигурационный файл и считываем строки
        LineFile = VBases.readline()
        while LineFile:
            i = 0
            while len(LineFile) > i:
                # получаем название базы для имени архива, убираем спецсимволы из имени архива
                if LineFile[i] == '[':
                    pattern = r"[^\w\s]" #регулярка для очистки от спецсимволов
                    BaseName = re.sub(pattern, '', LineFile[i + 1: -2])
                    ArchivName = (".\\Backup\\" + str(BaseName) + "_" + str(ArchivTime))
                    break
                else:
                    i += 1
            #  находим строку с путем к базе, проверяем оканчивается ли путь на слэш,
            #  архивируем базу и закрываем конфигурационный файл
            if LineFile[0:12] == "Connect=File":
                if LineFile[-3:-2] == "\\":
                    PathBase = LineFile[14:-4].replace('\\', '/')
                else:
                    PathBase = LineFile[14:-3].replace('\\', '/')
                subprocess.call(["C:/Program Files/7-Zip/7z.exe", "a", "-tzip", "-ssw", "-mx7", ArchivName, PathBase])
            LineFile = VBases.readline()
        VBases.close()

    def shutdownNo(self):
        self.hide()
        self.createBackup()
        sys.exit()

    def shutdownYes(self):
        self.hide()
        self.createBackup()
        subprocess.call(["shutdown.exe", "/s"])
        sys.exit()


#функция установки архиватора
def setupZip():
    if os.environ["programfiles(x86)"] == "c:\\Program Files (x86)":
        subprocess.call(["7zip/7z-x32.exe", "/S"])
    else:
        subprocess.call(["7zip/7z-x64.exe", "/S"])


# установлен ли архиватор у пользователя, если нет то устанавливаем
directories = os.listdir(path="C:\\Program Files")
for i in directories:
    if i == "7-Zip":
        break
else:
    setupZip()

"""
import ctypes, sys

#повышаем права до администраторских (не работает)
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # установлен ли архиватор у пользователя, если нет то устанавливаем
    directories = os.listdir(path="C:\\Program Files")
    for i in directories:
        if i == "7-Zip":
            break
    else:
        setupZip()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
"""

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == "__main__":  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
