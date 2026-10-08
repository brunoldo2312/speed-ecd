# 📊 Gerador SPED ECD

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Estável-brightgreen.svg)]()

Aplicação desktop para geração do arquivo de transmissão da **Escrituração Contábil Digital (ECD)** no leiaute **9.00** da Receita Federal, com suporte a **Lucro Presumido**, **importação de notas fiscais em PDF** e **validação integrada**.

---

## 📑 Índice

- [Sobre o projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Como usar](#-como-usar)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Registros gerados no SPED ECD](#-registros-gerados-no-sped-ecd)
- [Compilando para .exe](#-compilando-para-exe)
- [Solução de problemas](#-solução-de-problemas)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🎯 Sobre o projeto

Este programa automatiza a geração do arquivo `.txt` da ECD a partir de:

- **Importação de notas fiscais em PDF** (DANFSe v2.0, NFS-e, DANFE) — extração automática de CNPJ, razão social, endereço, município, UF, IE, IM, data e valor.
- **Lançamentos manuais de despesas** — cadastro de gastos por formulário, com escolha da conta referencial do plano P150A.
- **Backup da ECD do ano anterior** — reaproveitamento de saldos finais.

O arquivo final é gerado em **ISO-8859-1, com quebras CRLF, sem BOM** — formato aceito pelo **PVA (Programa Validador e Assinador)** da Receita Federal.

> ⚠️ Ferramenta destinada a contadores e profissionais de contabilidade. Não substitui a revisão técnica das informações.

---

## ✨ Funcionalidades

| # | Recurso | Descrição |
|---|---------|-----------|
| 1 | **Importação de PDF** | Leitura automática de notas fiscais (DANFSe v2.0, NFS-e, DANFE) |
| 2 | **Validação de período** | Alerta quando a nota está fora do ano-calendário da ECD |
| 3 | **Auto-preenchimento** | Cadastro do contribuinte preenchido a partir do primeiro PDF |
| 4 | **Despesas manuais** | Formulário para lançar gastos com conta referencial P150A |
| 5 | **Ano-calendário dinâmico** | Gera ECD para qualquer ano, inclusive em atraso |
| 6 | **Backup da ECD anterior** | Importa `.txt` do ano anterior para reaproveitar saldos |
| 7 | **Validação integrada** | Confere CNPJ, CPF, datas, partidas dobradas, balanço e contadores |
| 8 | **Exportação pronta para o PVA** | ISO-8859-1 / CRLF / sem BOM |
| 9 | **Log completo** | Registro de todas as operações com timestamp |
| 10 | **Interface gráfica Tkinter** | 6 abas com scroll, roda do mouse e atalhos |

---

## 💻 Requisitos

### Ambiente de desenvolvimento

- **Python 3.8+** (recomendado 3.10 ou superior)
- **Tkinter** (já incluído no instalador oficial do Python para Windows)
- **pypdf** (para leitura de PDFs)

### Sistema operacional

- Windows 10 / 11
- Linux / macOS (funciona, mas focado em Windows)

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/gerador-sped-ecd.git
cd gerador-sped-ecd
```

### 2. Instale as dependências

```bash
pip install pypdf
```

### 3. Execute

```bash
python ecd_automatico.py
```

---

## 📖 Como usar

### Passo a passo resumido

```
┌────────────────────────────────────┐
│  1. TELA INICIAL → Iniciar ▶       │
└────────────────┬───────────────────┘
                 ▼
┌────────────────────────────────────┐
│  2. Aba Cadastro                   │
│     - Importe um PDF (auto-preenche)│
│     - Confira os dados             │
│     - Preencha o CONTADOR          │
│     - Confirmar cadastro           │
└────────────────┬───────────────────┘
                 ▼
┌────────────────────────────────────┐
│  3. Aba Notas PDF                  │
│     - Adicione os PDFs             │
│     - Confira extração             │
└────────────────┬───────────────────┘
                 ▼
┌────────────────────────────────────┐
│  4. Aba Despesas Manuais (opcional)│
│     - Cadastre gastos do CNPJ      │
└────────────────┬───────────────────┘
                 ▼
┌────────────────────────────────────┐
│  5. Aba ECD Anterior (opcional)    │
│     - Importe .txt do ano anterior │
└────────────────┬───────────────────┘
                 ▼
┌────────────────────────────────────┐
│  6. Aba Gerar & Validar            │
│     - Gerar Arquivo                │
│     - Validar                      │
│     - Salvar Como...               │
└────────────────────────────────────┘
```

### Detalhamento de cada aba

#### 🧾 Aba 1 — Cadastro

Preencha os dados do **contribuinte**, **contador** e **representante legal**.

| Campo | Obrigatório | Descrição |
|-------|:-----------:|-----------|
| Razão Social | ✅ | Nome empresarial |
| CNPJ | ✅ | 14 dígitos, sem pontuação |
| UF | ✅ | 2 letras (ex.: `MG`) |
| Inscrição Estadual | | IE estadual |
| Código IBGE Município | | 7 dígitos |
| Município | | Nome do município |
| NIRE | | Número de Identificação do Registro de Empresas |
| Inscrição Municipal | | IM municipal |
| Data Inicial | ✅ | `DDMMAAAA` — define o início do período |
| Data Final | ✅ | `DDMMAAAA` — define o fim do período |
| Data do Arquivo | | Se vazio, usa a data final |
| Data Ex. Social | | Se vazio, usa a data final |

**Contador** — Nome e CPF são **obrigatórios** (registro `J930`).

**Representante Legal** — dados opcionais; se preenchidos, são gravados em outro `J930`.

**Botões:**
- `Carregar cadastro (JSON)...` — carrega de arquivo salvo
- `Salvar cadastro (JSON)...` — salva para reutilizar
- `Confirmar cadastro` — valida e confirma
- `Limpar cadastro` — apaga todos os campos

#### 📄 Aba 2 — Notas PDF

- Clique em **Adicionar PDFs...** e selecione um ou mais arquivos
- O programa extrai automaticamente: **CNPJ, razão social, endereço, município, UF, CEP, IE, IM, data e valor**
- A coluna **Período** mostra:
  - `OK` — dentro do período da ECD
  - `⚠ FORA` — fora do período (linha destacada em vermelho)
- Notas fora do período geram um alerta pedindo confirmação
- Use **Ver dados extraídos** para inspecionar o texto completo do PDF
- Use **Remover selecionado** para retirar itens da lista

#### 💰 Aba 3 — Despesas Manuais

Formulário para lançar gastos que não estão em notas fiscais:

| Campo | Descrição |
|-------|-----------|
| Data | `DDMMAAAA` (validado contra o período da ECD) |
| Valor | Formato `1500,00` ou `1.500,00` |
| Histórico | Descrição do lançamento |
| Conta Referencial | Selecionada da lista P150A (Lucro Presumido) |

Cada despesa gera:
- 1 registro `I200` (cabeçalho do lançamento)
- 1 `I250` de **débito** em `4.1.1.01` (despesa)
- 1 `I250` de **crédito** em `1.1.1.01` (banco)

#### 📂 Aba 4 — ECD Anterior

- Marque o checkbox **Usar backup da ECD do ano anterior**
- Selecione o arquivo `.txt` da ECD transmitida no ano anterior
- O programa mostra os saldos finais encontrados (registros `I155`)

#### ✅ Aba 5 — Gerar & Validar

1. Clique em **Gerar Arquivo SPED ECD** — o programa monta o `.txt` na memória
2. Clique em **Validar** — executa as verificações:
   - Contagem de campos por registro
   - CNPJ do contribuinte
   - CPF/CNPJ do contador/representante
   - Duplicidade de contas `I050`
   - Consistência dos saldos `I155`
   - Partidas dobradas nos `I200`/`I250`
   - Balanço patrimonial (Ativo = Passivo)
   - Contadores dos blocos (`I990`, `J990`, `9990`, `9999`)
3. Clique em **Salvar Como...** — gera o arquivo com codificação ISO-8859-1

#### 📝 Aba 6 — Log

Mostra todas as operações com timestamp. Útil para auditar o que foi feito.

---

## 📁 Estrutura do projeto

```
gerador-sped-ecd/
│
├── ecd_automatico.py      # Programa principal
├── README.md              # Este manual
├── LICENSE                # Licença MIT
├── requirements.txt       # Dependências
├── .gitignore             # Arquivos ignorados
│
├── exemplo/
│   ├── cadastro_ecd.json  # Exemplo de cadastro salvo
│   └── nota_exemplo.pdf   # PDF de exemplo (opcional)
│
└── build/                 # (gerado pelo PyInstaller, não versionar)
```

### Arquivo `requirements.txt`

Crie este arquivo com o conteúdo:

```
pypdf>=3.0.0
pyinstaller>=6.0.0
```

### Arquivo `.gitignore`

Crie este arquivo com o conteúdo:

```
# Byte-compiled
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
venv/
env/
.venv/

# PyInstaller
build/
dist/
*.spec

# Arquivos gerados pelo programa
sped_ecd_*.txt
cadastro_ecd.json
*.log

# IDEs
.vscode/
.idea/
*.swp

# Sistema operacional
.DS_Store
Thumbs.db
```

---

## 📋 Registros gerados no SPED ECD

### Bloco 0 — Abertura e Identificação

| Registro | Descrição |
|----------|-----------|
| `0000` | Cabeçalho do arquivo — dados do contribuinte e período |
| `0001` | Abertura do bloco 0 |
| `0007` | Outros dados da entidade |
| `0990` | Encerramento do bloco 0 |

### Bloco C — Documentos Fiscais

| Registro | Descrição |
|----------|-----------|
| `C001` | Abertura do bloco C |
| `C990` | Encerramento do bloco C |

### Bloco I — Lançamentos Contábeis

| Registro | Descrição | Quantidade |
|----------|-----------|:----------:|
| `I001` | Abertura do bloco I | 1 |
| `I010` | Identificação da escrituração | 1 |
| `I030` | Termo de abertura | 1 |
| `I050` | Plano de contas | 21 |
| `I051` | Mapeamento referencial (P100A) | 7 |
| `I052` | Mapeamento de aglutinação (P150A) | 7 |
| `I100` | Centro de custo | 1 |
| `I150` | Períodos de apuração | 12 |
| `I155` | Saldos periódicos | Variável |
| `I200` | Lançamento contábil | Variável |
| `I250` | Partidas do lançamento | Variável |
| `I350` | Saldos das contas | 1 |
| `I355` | Saldos das contas de resultado | 3 |
| `I990` | Encerramento do bloco I | 1 |

### Bloco J — Demonstrações Contábeis

| Registro | Descrição |
|----------|-----------|
| `J001` | Abertura do bloco J |
| `J005` | Balanço patrimonial |
| `J100` | Balanço patrimonial (Ativo/Passivo) |
| `J150` | Demonstração do Resultado (DRE) |
| `J210` | Notas explicativas — Lucros Acumulados |
| `J215` | Fato contábil relevante |
| `J800` | Notas explicativas |
| `J900` | Termo de encerramento |
| `J930` | Assinantes — contador e representante legal |
| `J990` | Encerramento do bloco J |

### Bloco 9 — Encerramento

| Registro | Descrição |
|----------|-----------|
| `9001` | Abertura do bloco 9 |
| `9900` | Contagem de registros por tipo |
| `9990` | Encerramento do bloco 9 |
| `9999` | Encerramento do arquivo |

---

## 🔨 Compilando para `.exe`

Para distribuir o programa sem exigir Python instalado:

### 1. Instale o PyInstaller

```bash
pip install --upgrade pyinstaller
```

### 2. Compile

```bash
python -m PyInstaller --onefile --windowed --name "GeradorECD" ^
  --hidden-import pypdf ^
  --hidden-import pypdf._crypt_providers ^
  --clean ecd_automatico.py
```

**No Linux/macOS (sem `^`):**

```bash
python -m PyInstaller --onefile --windowed --name "GeradorECD" \
  --hidden-import pypdf \
  --hidden-import pypdf._crypt_providers \
  --clean ecd_automatico.py
```

### 3. Localize o executável

O arquivo final estará em:

```
dist/GeradorECD.exe
```

### Parâmetros explicados

| Parâmetro | Efeito |
|-----------|--------|
| `--onefile` | Gera um único `.exe` |
| `--windowed` | Sem janela de console |
| `--name "GeradorECD"` | Nome do executável |
| `--hidden-import pypdf` | Inclui a biblioteca de PDF |
| `--clean` | Limpa cache de builds anteriores |

### ⚠️ Primeira execução

O Windows SmartScreen pode alertar "Editor desconhecido". Clique em **Mais informações** → **Executar mesmo assim**. Isso é normal para executáveis sem assinatura digital.

---

## 🛠 Solução de problemas

### `'python' não é reconhecido como um comando`

O Python não está no PATH. Durante a instalação, marque **"Add Python to PATH"** ou use o launcher:

```bash
py ecd_automatico.py
```

### `ModuleNotFoundError: No module named 'pypdf'`

Instale a biblioteca:

```bash
pip install pypdf
```

### `ModuleNotFoundError: No module named 'tkinter'`

O Tkinter não está instalado. No Windows, reinstale o Python marcando **"tcl/tk and IDLE"**. No Linux:

```bash
sudo apt-get install python3-tk
```

### O executável não abre

Compile com `--console` para ver o erro real:

```bash
python -m PyInstaller --onefile --console --name "GeradorECD_debug" ^
  --hidden-import pypdf --clean ecd_automatico.py
```

Execute `dist/GeradorECD_debug.exe` e leia o traceback.

### Erro de validação `J930: nome do contador vazio`

Preencha o **nome** e o **CPF do contador** na aba Cadastro antes de gerar.

### `0000: CNPJ inválido`

O CNPJ informado no cadastro não passou na validação de dígito verificador. Confira e digite apenas os 14 números.

### Erro `J150 totalizador diferente dos filhos`

O valor final do totalizador do DRE deve ter o **indicador D/C** igual à soma com sinal dos filhos. Verifique se as receitas estão como `C` (Credor) e despesas como `D` (Devedor).

---

## 🤝 Contribuindo

Contribuições são bem-vindas. Para colaborar:

1. Faça um **fork** do projeto
2. Crie uma branch: `git checkout -b minha-feature`
3. Faça commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Faça push: `git push origin minha-feature`
5. Abra um **Pull Request**

### Padrões de código

- Python **PEP 8**
- Docstrings em todas as funções públicas
- Comentários em português (idioma do projeto)
- Sem dependências externas além de `pypdf`

### Reportando bugs

Abra uma **Issue** com:
- Descrição do problema
- Passos para reproduzir
- Saída da aba **Log** (se aplicável)
- Versão do Python e do sistema operacional

---

## 📄 Licença

Este projeto é distribuído sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📚 Referências

- [Manual de Orientação do Leiaute 9 da ECD](http://sped.rfb.gov.br/) — Receita Federal
- [Programa Validador e Assinador (PVA)](http://sped.rfb.gov.br/pasta/show/1644) — Receita Federal
- [Tabelas Dinâmicas do SPED](http://sped.rfb.gov.br/pagina/show/2481) — Planos referenciais
- [pypdf — Documentação](https://pypdf.readthedocs.io/)

---

## 📞 Contato

**Bruno Labanca**
- 📧 brunolabanca@yahoo.com.br
- 🔗 [GitHub](https://github.com/SEU-USUARIO)

---

<p align="center">
  Desenvolvido para simplificar a vida do contador brasileiro 🇧🇷
</p>
