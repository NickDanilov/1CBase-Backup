from cx_Freeze import setup, Executable

build_options = {"build_exe": "build_0.2", 
				 #"zip_include_packages": []
				 }

setup(
    name = "Backup 1C",
    version = "0.2",
    description = "Архивация 1С",
    executables = [Executable("1cbackup.py", 
    	           targetName = "backup_1C.exe", 
    	           base ="Win32GUI",
    	           #icon = "1c.ico"
    	           )],
    options = {"build_exe": build_options}
)