A Linguagem de Emojis (LE) é uma linguagem de programação baseada em
emojis, inspirada na estrutura e sintaxe da linguagem C. O objetivo principal foi
substituir os símbolos convencionais de C por emojis, criando assim uma nova forma
de expressar lógica de programação.


## Símbolos
A Linguagem utiliza uma combinação de emojis para representar diversos
elementos da linguagem C, como:

-  Tipos de dados :
    - Caracteres ASCII (char): 🔤
    - Inteiro (int): ℹ️
    - Real (float):☁
    - Vazio (void): 🥚
    - Bool (bool): 🐃

- Comandos:
    - Atribuição (=): 🟰
    - Entrada (scanf): 🔍
    - Saída (printf): 🖨
    - Condicional
        - if: 🤔
        - else: 🙄
    - Repetição
        - while: 🧄
        - for: 🍀

- Operadores
    - Relacionais
        - Igualdade (==) : 🟰🟰
        - Diferença (!=): ❗🟰
        - Maior (>): 🙌
        - Menor (<): 🤏
        - Maior igual (>=): 🙌🟰
        - Menor igual (<=): 🤏🟰
    - Lógicos
        - Conjunção (&&): 🤝
        - Disjunção (||): 🖖
        - Negação (!): ❗
    - Aritméticos
        - Adição (+): ➕
        - Subtração (-): ➖
        - Multiplicação (*): ✖
        - Divisão (/): ➗
        - Resto (mod)(%): 💩

- Símbolos especiais
    - Chaves {} : 👉👈
    - Parênteses (): 🤜🤛
    - Colchetes []: 👇👆
    - Virgula “,”: ❤
    - Ponto e vírgula “;”: ❣
    - Ponto final “.”: 💥
    - Aspas simples (’): 🙏
    - Aspas duplas  ("): 🙏

- Blocos de comandos
    - begin/end ({}): 👉👈

- Palavras reservadas
    - true: 👍
    - false: 👎
    - break: ❌
    - continue: ✅
    - return: 🔄
    - main: 👨


## Regras:

Para utilizar a linguagem basta substituir os termos pelos emojis respectivos.
Exemplo:


```c
int main (){
    return 0;
}
```
```c
ℹ️ 👨 🤜🤛 👉
    🔄0❣
👈
```
### Declaração e Atribuição:
A interação da LE com valores e nomes de variáveis também é a mesma da Linguagem C
```c
int a = 5;
ℹ️ a 🟰 5 ❣
```
```c
char b = 'b';
🔤 b  🙏b🙏❣
```
```c
bool c = true;
🐃 c 🟰 👍❣
```
```c
float d = 5.0;
☁ d 🟰 5💥0❣
```

A linguagem também aceita declarações com atribuições ou sem e sequencias de declarações de um tipo especificado, por exemplo:
```c
float  r=5.1 , p=3.141592654 , v;
☁ r🟰5💥1 ❤ p🟰3💥141592654 ❤ v❣
```

O nome das variaveis seguem o automato NOME, o qual irá aceitar qualquer sequencia que comece com uma letra minuscula seguida de números e/ou letras minúsculas.


### Leitura e Escrita
- A função printf funciona da mesma maneira, note que as aspas simples e duplas possuem o mesmo emoji.

    ```c
    printf("digite um numero = ");
    🖨🤜🙏digite um numero = 🙏🤛❣
    ```

    A regra também aceitará o anexo de valores 
    ```c
    printf("Volume da esfera de raio %f: %f\n",r,v);
    🖨🤜🙏Volume da esfera de raio %f: %f\n🙏❤r❤v🤛❣
    ```

- A função scanf mantém sua estrutura, porém sem a necessidade do operador de referência & que é inserido pelo tradutor.
    ```c
    scanf("%d",&a);
    🔍🤜🙏%d🙏❤a🤛❣ 
    ```
### Estruturas Condicionais
- Para condicionais, implementamos somente expressão if.
    ```c
    if(a==0){}
    🤔🤜a🟰🟰0🤛👉👈
    ```

### Estruturas de Repetição
Loopings também são similares, implementamos a estrutura `for` e `while`.
- `for` : Mantemos a estrutura de 3 segmentos inicialização, condição e incremento/decremento. 
    ```c
    for(i=0;i<5;i=i+1){}

    🍀🤜i 🟰 0❣i🤏5❣i 🟰 i➕1🤛👉👈
    ```
- `while` : 
    ```c
    while (true) {}

    🧄 🤜 👍 🤛 👉👈
    ```

### Observações

Em relação aos automatos declarados no planejamento da linguagem não foram implementadas o reconhecimento de declaraçõs e chamadas de funções.

## Uso

Para uso da linguagem utilize arquivo [main.py](main.py), utilizando como argumento o arquivo de extensão `.emo` e opcionalmente um nome para o arquivo `.c` e `.exe` de saída. Através do direotorio principal execute:

```bash
python main.py <file.emo> [<output_name>]
```

- `<file.emo>`: Arquivo de entrada com o código a ser interpretado 
- `<output_name>`: Nome para o arquivo de saída. 
    - Opcional, valor padrão: `"output"`

Também é possivel colocar manualmente o código a ser intepretado na variavel codigo neste arquivo principal.

A execução do arquivo demonstrará a Analise lexica, sintática e a tradução do código para o código em linguagem C, a compilação do mesmo assim como a execução em um terminal separado de forma automatica, caso não haja erros. O executavel e o arquivo C serão gerados no diretorio [out](out)

Para a implementação da Analise léxica e sintatica utilizamos a biblioteca [ply](https://ply.readthedocs.io/en/latest/ply.html#) em python.

Essa é a unica biblioteca externa a ser instalada e pode ser obtida pela ferramenta pip
```bash
pip install -r requirements.txt
```
ou de forma mais direta
```bash
pip install ply==3.11
```

- [Analise Léxica](src/emoji_lex.py): Fará o reconhecimento de todos simbolos definidos, utilizando o modulo [ply.lex](https://ply.readthedocs.io/en/latest/ply.html#lex)
- [Analise Sintatica](src/emoji_parser.py): Fará o uso das regras, automatos definidos para reconhecer e aceitar a sintaxe da linguagem. Demonstrará de forma hierarquica todas as estuturas reconhecidas, caso não haja erros de sintaxe. Foi utilizado o modulo [ply.yacc](https://ply.readthedocs.io/en/latest/ply.html#yacc), este que gera os arquivos [parser.out](out/parser.out) e [parsertab.py](out/parsetab.py), que configuram os estados das regras e configurações da biblioteca para interpretar nossa solução.
- [Tradutor](src/gcc_translate.py): Irá criar e compilar o arquivo `.c` realizando a substituiçaõ de cada emoji pelo seu simbolo na linguagem C correspondente.

## Exemplos

Para demonstrar o uso da linguagem foram criados alguns exemplos de códigos. Todos os código de exemplo estão no diretorio [data](data/):

- [HelloWorld.emo](data/HelloWorld.emo)
    Este exemplo utiliza da estrutura de repetição `for` e de impressão `printf`, realizando o print de uma mensagem personalizada de "Hello World" 5 vezes seguidas.
    ```bash
    python main.py data/HelloWorld.emo hello
    ```
- [Paridade.emo](data/Paridade.emo)
    Este exemplo utiliza da estrutura condicional `if` verificando se o número inteiro declarado é par utilizando o operador de resto de divisão.
    ```bash
    python main.py data/Paridade.emo par
    ```
- [VolumeEsfera.emo](data/VolumeEsfera.emo)
    Este exemplo explora operações e declarações de variaveis em cascata, usando a formula de volume de uma esfera de determinado raio.
    ```bash
    python main.py data/VolumeEsfera.emo volume
    ```
- [InOut.emo](data/InOut.emo)
    Este exemplo explora o uso de leitura com `scanf` para armazenar um valor e imprimir uma operação com esse valor.
    ```bash
    python main.py data/InOut.emo input
    ```

  






