@echo off
cd /d "d:\Python-Dev\Git\21_Point_BJ"
echo 正在安装所需的包...
D:/Python-Dev/Git/21_Point_BJ/.venv/Scripts/pip.exe install pyinstaller

echo.
echo 正在打包程序为exe文件...
D:/Python-Dev/Git/21_Point_BJ/.venv/Scripts/pyinstaller.exe --onefile --windowed --name "21点牌计数器" blackjack_counter.py

echo.
echo 打包完成！
echo exe文件位置: dist\21点牌计数器.exe
echo.
pause
