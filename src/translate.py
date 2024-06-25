def traduzir_comando(comando):
    if "DECLARAÇÃO" in comando:
        return traduzir_declaracao(comando["DECLARAÇÃO"])
    elif "printf" in comando:
        return traduzir_printf(comando["printf"])
    elif "scanf" in comando:
        return traduzir_scanf(comando["scanf"])
    elif "if" in comando:
        return traduzir_if(comando["if"])
    elif "while" in comando:
        return traduzir_while(comando["while"])
    elif "for" in comando:
        return traduzir_for(comando["for"])
    elif "return" in comando:
        return traduzir_return(comando["return"])
    return ""


def traduzir_declaracao(declaracao):
    comandos = []
    for dec in declaracao[0]:
        val = dec["valor"]
        if type(val) == dict:
            val = traduzir_operacao(val)
        comandos.append(f"{dec['nome']}: {dec['type']}" + f" = {val}")
    return "\n    ".join(comandos)


def traduzir_printf(printf):
    return f'print({printf["valor"]})'


def traduzir_scanf(scanf):
    return f'{scanf["nome"]} = input()'


def traduzir_if(if_comando):
    condicao = traduzir_operacao(if_comando["valor"])
    bloco = traduzir_bloco(if_comando["bloco"]["BLOCO"], 2)
    return f"if {condicao}:\n{bloco}"


def traduzir_while(while_comando):
    condicao = traduzir_operacao(while_comando["valor"])
    bloco = traduzir_bloco(while_comando["bloco"]["BLOCO"])
    return f"while {condicao}:\n{bloco}"


def traduzir_for(for_comando):
    init = traduzir_comando(for_comando["init"])
    condition = traduzir_operacao(for_comando["condition"])
    update = traduzir_comando(for_comando["update"])
    comando = traduzir_comando(for_comando["comando"])
    return f"{init}\nwhile {condition}:\n{comando}\n{update}"


def traduzir_return(return_comando):
    return f"return {return_comando['valor']}"


def traduzir_operacao(operacao):
    if "OPERAÇÃO" in operacao:
        val1 = operacao["OPERAÇÃO"]["valor1"]
        if type(val1) == dict:
            val1 = traduzir_operacao(operacao["OPERAÇÃO"]["valor1"])

        op = operacao["OPERAÇÃO"]["op"]

        val2 = operacao["OPERAÇÃO"]["valor2"]
        if type(val2) == dict:
            val2 = traduzir_operacao(operacao["OPERAÇÃO"]["valor2"])
        return f"{val1} {op} {val2}"
    return str(operacao)


def traduzir_bloco(bloco, indent_level=0):
    comandos = [traduzir_comando(comando["COMANDO"]) for comando in bloco]
    indent = "    " * indent_level  # 4 espaços por nível de indentação
    return "\n".join([indent + comando for comando in comandos])


def traduzir_estrutura(estrutura):
    if "MAIN" in estrutura:
        bloco = estrutura["MAIN"]["BLOCO"]
        bloco_traduzido = traduzir_bloco(bloco, indent_level=1)
        return (
            f"def main():\n{bloco_traduzido}\n\nif __name__ == '__main__':\n    main()"
        )
    return ""
