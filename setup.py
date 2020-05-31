import cx_Freeze

executables = [cx_Freeze.Executable("CarGame.py")]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["racecar.png", "crash.mp3", "jazz.mp3"]}},
    executables = executables

    )
