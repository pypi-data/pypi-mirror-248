from os import path, listdir

path_nuklear_libs = path.abspath(path.dirname(__file__))

libs = {
    "Nuklear2.dll": path.join(path_nuklear_libs, "Nuklear2.dll"),
    "NuklearDotNet.dll": path.join(path_nuklear_libs, "NuklearDotNet.dll")
}

