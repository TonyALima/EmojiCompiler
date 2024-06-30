import subprocess
import sys
import shlex


class Translator:
    def __init__(self):
        self.dicionario = {
            "🔤": "char ",
            "ℹ️": "int ",
            "☁": "float ",
            "🥚": "void ",
            "🐃": "boolean ",
            "🟰": "=",
            "🔍": "scanf",
            "🖨": "printf",
            "🤔": "if ",
            "🙄": "else ",
            "🧄": "while ",
            "🍀": "for ",
            "🙌": ">",
            "🤏": "<",
            "🤝": "&&",
            "🖖": "||",
            "❗": "!",
            "➕": "+",
            "➖": "-",
            "✖": "*",
            "➗": "/",
            "💩": "%",
            "👉": "{",
            "👈": "}",
            "🤜": "(",
            "🤛": ")",
            "👇": "[",
            "👆": "]",
            "❤": ",",
            "❣": ";",
            "💥": ".",
            "🙏": '"',
            "👍": "true ",
            "👎": "false ",
            "❌": "break ",
            "✅": "continue ",
            "🔄": "return ",
            "👨": "main",
        }

    def translate(self, data: str, name: str = "output", execute: bool = False):
        if data.endswith(".emo"):
            with open(data, "r") as txt_file:
                txt = txt_file.readlines()
        else:
            txt = data.splitlines()

        for i, line in enumerate(txt):
            for key in self.dicionario.keys():
                line = line.replace(key, self.dicionario[key])
            if "scanf" in line:
                start = line.find(",") + 1
                end = line.find(")", start)
                var_name = line[start:end].strip()
                line = line[:start] + "&" + var_name + line[end:]
            txt[i] = line

        nameC = "out/" + name + ".c"
        with open(nameC, "w") as txt_file:
            txt.insert(0, "#include <stdio.h>\n")
            txt_file.writelines([line + "\n" for line in txt])

        print("\n".join(txt))

        out_compile = subprocess.getoutput(f"gcc {nameC} -o out/{name}")
        for key in self.dicionario.keys():
            out_compile = out_compile.replace(self.dicionario[key], key)
        print(out_compile)

        if execute:
            print("A executar...")
            command = f'gnome-terminal -- bash -c "./out/{name}; exec bash"'
            subprocess.Popen(shlex.split(command))
