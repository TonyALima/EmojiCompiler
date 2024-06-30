import subprocess
import sys

dicionario = {
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
    "🙌" : ">",
    "🤏" : "<",
    "🤝" : "&&",
    "🖖" : "||",
    "❗" : "!",
    "➕" : "+",
    "➖" : "-",
    "✖" : "*",
    "➗" : "/",
    "💩" : "%",
    "👉" : "{",
    "👈" : "}",
    "🤜" : "(",
    "🤛" : ")",
    "👇" : "[",
    "👆" : "]",
    "❤" : ",",
    "❣" : ";",
    "💥" : ".",
    "🙏" : "\"",
    "👍" : "true ",
    "👎" : "false ",
    "❌" : "break ",
    "✅" : "continue ",
    "🔄" : "return ",
    "👨" : "main"
}
if __name__ == "__main__":
    with open(sys.argv[1], "r") as txt_file:
        txt = txt_file.readlines()
        for i, line  in enumerate(txt):
            for key in dicionario.keys():
                line = line.replace(key, dicionario[key])
            txt[i] = line
    
    name = sys.argv[1].split(".")[0]
    nameC = name + ".c"
    with open(nameC, "w") as txt_file:
        txt.insert(0, "#include <stdio.h>\n")
        txt_file.writelines(txt)

    out = subprocess.getoutput(f"gcc {nameC} -o {name}")
    for key in dicionario.keys():
        out = out.replace(dicionario[key], key)
    print(out)