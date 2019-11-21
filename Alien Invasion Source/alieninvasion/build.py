from cx_Freeze import setup, Executable

setup(
        name = "Alien Invasion",
        options = {"build_exe":{"packages":["pygame"],"include_files":["images", "sounds"]}},
        version = "0.255",
        description = "Aliens RUN",
        executables = [Executable("main.pyw"), Executable("alien.py"), Executable("game_functions.py"), Executable("settings.py"), Executable("ship.py"), Executable("bullet.py"), Executable("game_stats.py"), Executable("meteor.py"), Executable("button.py")]
)
