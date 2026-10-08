Manual do Usuário — Gerador SPED ECD (Executável)
Versão: 3.3.1
Leiaute: 9.00 — Lucro Presumido
Plataforma: Windows 10 / 11 (64 bits)

📑 Índice
Apresentação

Instalação

Tela Inicial

Aba 1 — Cadastro

Aba 2 — Notas PDF

Aba 3 — Despesas

Aba 4 — Retiradas de Sócios

Aba 5 — Notas Explicativas

Aba 6 — ECD Anterior

Aba 7 — Gerar & Validar

Aba 8 — Log

Fluxo de trabalho recomendado

Importação no PVA

Solução de problemas

Perguntas frequentes

1. Apresentação
O Gerador SPED ECD é um programa que automatiza a geração do arquivo de transmissão da Escrituração Contábil Digital (ECD) no leiaute 9.00, com suporte a Lucro Presumido.

O que o programa faz
Função	Descrição
Importação de PDFs	Extrai dados de notas fiscais (DANFSe, NFS-e, DANFE)
Cálculo automático	Balanço, DRE e Lucros Acumulados calculados
Lançamentos contábeis	Gerados automaticamente a partir das movimentações
Notas Explicativas	Gera arquivo RTF e anexa ao registro J800
Validação integrada	Confere CNPJ, CPF, datas, partidas dobradas e balanço
Exportação	Arquivo em ISO-8859-1 pronto para o PVA
O que o programa NÃO faz
Não substitui a revisão do contador

Não assina digitalmente o arquivo (feito no PVA)

Não transmite o arquivo à Receita Federal (feito no PVA)

2. Instalação
2.1. Requisitos
Windows 10 ou 11 (64 bits)

100 MB de espaço em disco

Nenhum programa adicional necessário

2.2. Instalação do executável
Copie o arquivo GeradorECD.exe para uma pasta de sua preferência

Sugestão: C:\GeradorECD\

Evite pastas com acentos, espaços ou caracteres especiais

Dê duplo-clique no GeradorECD.exe

Na primeira execução, o Windows pode exibir o aviso do SmartScreen:

text
┌────────────────────────────────────────────┐
│  ⚠  O Windows protegeu o computador        │
│                                            │
│  O Windows Defender SmartScreen impediu    │
│  o início de um aplicativo não reconhecido │
└────────────────────────────────────────────┘
Clique em:

"Mais informações"

Depois em "Executar mesmo assim"

Este aviso é normal para executáveis sem assinatura digital paga. O programa é seguro.

2.3. Criando um atalho
Clique com o botão direito sobre GeradorECD.exe

Escolha "Enviar para" → "Área de trabalho (criar atalho)"

Um ícone será criado na sua área de trabalho

2.4. Recomendações
Não coloque o .exe em pendrive ou pasta de rede (a inicialização fica lenta)

Não mova o .exe enquanto estiver aberto

Faça backup da pasta do programa periodicamente

3. Tela Inicial
Ao abrir o programa, a primeira tela é a Tela Inicial:

text
┌──────────────────────────────────────────────────────────────┐
│  📊  Gerador SPED ECD                                        │
│  Escrituração Contábil Digital — Leiaute 9.00                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│          ▶  INICIAR          [ Sair ]                        │
│                                                              │
│  O que este programa faz?                                    │
│                                                              │
│  1. Notas Explicativas (Registro J800)                       │
│  2. Começa VAZIO — sem lançamentos pré-cadastrados           │
│  3. Importação de notas fiscais (PDF)                        │
│  4. Despesas manuais e Retiradas de sócios                   │
│  5. Capital Social dinâmico                                  │
│  6. Balanço e Lucros calculados automaticamente              │
│                                                              │
│  ⚠ Para importar PDFs é necessário ter a biblioteca 'pypdf'  │
└──────────────────────────────────────────────────────────────┘
Botões
Botão	Ação
▶ INICIAR	Abre a tela principal com as 8 abas
Sair	Fecha o programa
4. Aba 1 — Cadastro
A aba mais importante. Aqui você informa os dados do contribuinte, contador e representante legal.

text
┌──────────────────────────────────────────────────────────────┐
│  1. Cadastro  │  2. Notas PDF  │  3. Despesas  │ ...         │
├──────────────────────────────────────────────────────────────┤
│  Cadastro do Contribuinte                                    │
│                                                              │
│  Razão Social:            [_____________________________]    │
│  CNPJ (só números):       [______________]                   │
│  Capital Social (R$):     [_____________]                    │
│  UF:                      [__]                               │
│  Inscrição Estadual:      [______________]                   │
│  Código IBGE Município:   [__________]                       │
│  Município:               [__________________]               │
│  NIRE:                    [______________]                   │
│  Inscrição Municipal:     [______________]                   │
│  Data Inicial:            [__________]                       │
│  Data Final:              [__________]                       │
│  ...                                                         │
└──────────────────────────────────────────────────────────────┘
Campos do Contribuinte
Campo	Obrigatório	Formato	Exemplo
Razão Social	✅	Texto	EMPRESA XYZ LTDA
CNPJ	✅	14 dígitos	12345678000199
Capital Social		R$	2000.00 ou 2.000,00
UF	✅	2 letras	MG
Inscrição Estadual		Números	1234567890
Código IBGE Município		7 dígitos	3106200
Município	✅	Texto	BELO HORIZONTE
NIRE		Números	31200000000
Inscrição Municipal		Números	12345678
Data Inicial	✅	DDMMAAAA	01012025
Data Final	✅	DDMMAAAA	31122025
Data do Arquivo		DDMMAAAA	31122025
Data Ex. Social		DDMMAAAA	31122025
💡 Dica: se você deixar Data do Arquivo e Data Ex. Social vazios, o programa usa a Data Final automaticamente.

Campos do Contador (obrigatórios)
Campo	Formato	Exemplo
Nome	Texto	BRUNO LABANCA
CPF	11 dígitos	22068862867
CRC	Números	1MG67560
E-mail	Texto	contador@email.com
Telefone	Texto	31999999999
UF CRC	2 letras	MG
Nº Sequencial CRC	Texto	MG/2025/67560
Data CRC	DDMMAAAA	31122025
Campos do Representante Legal
Todos opcionais, mas se preenchidos, geram um registro J930 adicional.

Botões de ação
Botão	Ação
Carregar cadastro (JSON)...	Carrega dados salvos anteriormente
Salvar cadastro (JSON)...	Salva os dados para reutilizar
Confirmar cadastro	Valida tudo e confirma
Limpar cadastro	Apaga todos os campos
Fluxo recomendado
text
1. Importe um PDF (aba 2) → preenche automaticamente
   ↓
2. Volte à aba Cadastro
   ↓
3. Complete: Capital Social, NIRE, dados do Contador
   ↓
4. Clique em "Confirmar cadastro"
5. Aba 2 — Notas PDF
Importa notas fiscais em PDF e extrai os dados automaticamente.

Como usar
Clique em "Adicionar PDFs..."

Selecione um ou mais arquivos .pdf

O programa extrai: CNPJ, razão social, endereço, município, UF, IE, IM, data e valor

Tabela de notas
Coluna	O que mostra
Arquivo	Nome do PDF
CNPJ	CNPJ do emitente
Razão Social	Nome da empresa emissora
Data	Data da competência
Valor	Valor total da nota
Período	OK ou ⚠ FORA
Alerta de nota fora do período
Se a data da nota estiver fora do período da ECD (data inicial a data final do cadastro), o programa exibe:

text
┌────────────────────────────────────────────┐
│  ⚠  Nota fora do período                   │
├────────────────────────────────────────────┤
│  O arquivo: nota_123.pdf                   │
│  tem data 11/11/2025, que está FORA do     │
│  período da ECD.                           │
│                                            │
│  Período: 01/01/2024 a 31/12/2024          │
│                                            │
│  Deseja INCLUIR esta nota mesmo assim?     │
│                                            │
│              [ Sim ]   [ Não ]             │
└────────────────────────────────────────────┘
💡 Recomendação: clique em "Não" para evitar rejeição no PVA.

Botões
Botão	Ação
Adicionar PDFs...	Seleciona novos arquivos
Remover selecionado	Remove a nota da lista
Limpar lista	Remove todas as notas
Ver dados extraídos	Mostra detalhes do PDF
O que acontece ao importar
Cada nota gera automaticamente um lançamento contábil:

text
|I200|001|11112025|8884,00|N||
|I250|1.1.1.01||8884,00|D|1||Recebimento por servicos prestados|
|I250|3.1.1.01||8884,00|C|1||Recebimento NF - TOMADOR XYZ|
6. Aba 3 — Despesas
Cadastra despesas que não vieram de notas PDF.

Como usar
Preencha o formulário:

Data (DDMMAAAA)

Valor (R$)

Histórico (descrição)

Conta Referencial (lista do P150A)

Clique em "Adicionar Despesa"

Contas referenciais disponíveis
O programa oferece 30 contas do plano P150A, incluindo:

Código	Descrição
3.01.01.07.01.02.00	Ordenados, Salários, Gratificações
3.01.01.07.01.04.00	Encargos Sociais
3.01.01.07.01.07.00	Serviços Prestados por Pessoa Jurídica
3.01.01.07.01.11.00	Despesas com Aluguéis
3.01.01.07.01.13.00	Despesas com Energia Elétrica
3.01.01.07.01.19.00	Despesas com Impostos e Taxas
3.01.01.07.01.30.00	Outras Despesas Operacionais
Lançamento gerado
text
|I200|002|12122025|300,00|N||
|I250|4.1.1.01||300,00|D|1||Aluguel do escritório|
|I250|1.1.1.01||300,00|C|1||Aluguel do escritório|
7. Aba 4 — Retiradas de Sócios
Cadastra retiradas de lucro isento de IRPF.

Como usar
Preencha:

CPF do Sócio (11 dígitos — validado)

Nome do Sócio

Valor (R$)

Data (DDMMAAAA)

Clique em "Adicionar Retirada"

Lançamento gerado
text
|I200|003|31122025|30000,00|N||
|I250|2.1.2.01||30000,00|D|1||Retirada lucro isento IRPF - BRUNO (05235563654)|
|I250|1.1.1.01||30000,00|C|1||Retirada lucro isento IRPF - BRUNO (05235563654)|
E o seguinte fato contábil no registro J215:

text
|J215|DISTRIB_LUCRO|Distribuicao de lucros - BRUNO (05235563654)|30000,00|D|
⚠️ Atenção: o CPF é validado pelo dígito verificador. CPFs inválidos são rejeitados.

8. Aba 5 — Notas Explicativas
Digite o conteúdo das notas explicativas. O programa converte automaticamente para RTF e anexa ao registro J800.

Botões disponíveis
Botão	Ação
Inserir modelo padrão	Insere um texto pré-formatado (6 seções)
Limpar	Apaga o campo
Pré-visualizar RTF	Mostra o código RTF e o hash SHA-1
Salvar RTF...	Salva o arquivo .rtf separadamente
Estrutura sugerida (modelo padrão)
text
1. CONTEXTO OPERACIONAL
2. BASE DE PREPARAÇÃO DAS DEMONSTRAÇÕES CONTÁBEIS
3. PRINCIPAIS PRÁTICAS CONTÁBEIS
   3.1. Apuração do Resultado
   3.2. Caixa e Equivalentes de Caixa
   3.3. Ativo Não Circulante
4. CAPITAL SOCIAL
5. DISTRIBUIÇÃO DE LUCROS
6. EVENTOS SUBSEQUENTES
Como funciona por dentro
Você digita o texto

O programa:

Escapa caracteres especiais do RTF

Converte acentos para sequências \uXXX?

Gera o cabeçalho RTF com fonte Arial

Calcula o hash SHA-1

O registro J800 é montado:

text
|J800|010|Notas Explicativas|<HASH_SHA1>|{\rtf1\ansi...|J800FIM|
Referência cruzada
Se as notas estão preenchidas, o campo NOTA_EXP_REF do registro J210 recebe 1:

text
|J210|0|LUCRO_ACUM|LUCROS ACUMULADOS|0,00|C|8584,00|C|1|
9. Aba 6 — ECD Anterior
Se esta NÃO for a primeira entrega, importe o arquivo .txt da ECD do ano anterior.

Como usar
Marque o checkbox "Usar backup da ECD do ano anterior"

Clique em "Selecionar arquivo .txt..."

Selecione o arquivo transmitido no ano anterior

O programa exibe o resumo dos saldos finais encontrados

Informações exibidas
text
Arquivo: sped_ecd_2024.txt
CNPJ: 36303795000154
Empresa: SILVINO FERREIRA DA ROCHA JUNIOR
Período: 01/01/2024 a 31/12/2024

Saldos finais (5 contas):
  1.1.1.01  →  8.884,00 D
  2.1.1.01  →  2.000,00 C
  2.1.2.01  →  6.884,00 C
  3.1.1.01  →  88.884,00 C
  4.1.1.01  →  3.000,00 D
⚠️ Atenção: este recurso apenas informa os saldos encontrados. Para usá-los como saldo inicial do ano atual, é necessário adaptar o programa manualmente.

10. Aba 7 — Gerar & Validar
Aqui você gera e valida o arquivo final.

Botões
Botão	Ação
Gerar Arquivo SPED ECD	Monta o arquivo na memória
Validar	Executa as verificações internas
Salvar Como...	Salva o arquivo .txt no disco
Fluxo
text
1. Gerar Arquivo SPED ECD
   → mostra o conteúdo na pré-visualização

2. Validar
   → se aprovado: mostra as notas explicativas geradas
   → se reprovado: lista os erros

3. Salvar Como...
   → abre o diálogo para escolher onde salvar
Verificações da validação
Verificação	O que confere
Contagem de campos	Cada registro tem o número exato de campos
CNPJ do contribuinte	Dígito verificador válido
CPF do contador	Dígito verificador válido
CNPJ do representante	Dígito verificador válido
Datas	Formato DDMMAAAA e validade
Duplicidade I050	Nenhuma conta duplicada
Consistência I155	SI + Débito - Crédito = SF
Partidas dobradas	Σ Débitos = Σ Créditos
Balanço	Ativo = Passivo
Contadores	I990, J990, 9990, 9999 corretos
Se aprovado — janela de notas explicativas
text
┌──────────────────────────────────────────────┐
│  ✅  Arquivo aprovado na validação           │
├──────────────────────────────────────────────┤
│  ✅ 0 erros — arquivo APTO para o PVA.       │
│                                              │
│  RESUMO DA VALIDAÇÃO                         │
│  ─────────────────────────────────────────   │
│  Balanço equilibrado: R$ 10.884,00           │
│                                              │
│  NOTAS EXPLICATIVAS / FATOS CONTÁBEIS        │
│  ─────────────────────────────────────────   │
│  ── J210 — Lucros Acumulados ──              │
│    • LUCROS ACUMULADOS                       │
│        Saldo inicial : R$      0,00 (C)      │
│        Saldo final   : R$  8.884,00 (C)      │
│        Nota explicativa ref.: 1              │
│                                              │
│  ── J215 — Fatos Contábeis Relevantes ──     │
│    • Encerramento do exercicio...            │
│        Valor: R$ 8884,00 (C)                 │
│                                              │
│  ── J800 — Notas Explicativas ──             │
│    • Notas Explicativas                      │
│        TIPO_DOC : 010                        │
│        HASH_RTF : A1B2C3D4E5F6...            │
│        RTF anexado: Sim                      │
│                                              │
│                  [ OK ]                      │
└──────────────────────────────────────────────┘
Se reprovado
text
┌──────────────────────────────────────────────┐
│  ❌ Validação                                │
├──────────────────────────────────────────────┤
│  3 erro(s):                                  │
│                                              │
│  L102: J100 tem 13 campos (esperado 12)      │
│  L103: J100 tem 13 campos (esperado 12)      │
│  L104: J100 tem 13 campos (esperado 12)      │
│                                              │
│                  [ OK ]                      │
└──────────────────────────────────────────────┘
Corrija os erros e gere novamente.

Arquivo gerado
O arquivo sped_ecd_AAAA.txt é salvo com:

Propriedade	Valor
Codificação	ISO-8859-1 (Latin-1)
Quebra de linha	CRLF (\r\n)
BOM	Sem BOM
Tamanho típico	5-50 KB
11. Aba 8 — Log
Mostra todas as operações realizadas com timestamp.

Formato das mensagens
text
[HH:MM:SS] [CATEGORIA] Mensagem
Categorias
Categoria	Descrição
[CADASTRO]	Operações do cadastro
[PDF]	Importação de notas
[DESPESA]	Cadastro de despesas
[RETIRADA]	Cadastro de retiradas
[NOTAS EXP]	Notas explicativas
[ECD ANTERIOR]	Backup do ano anterior
[GERAR]	Geração do arquivo
[VALIDAR]	Resultado da validação
[SALVAR]	Arquivo salvo
[ERRO ...]	Erros ocorridos
Exemplo de log
text
[19:08:23] [PDF] 31062001236303795000154250000000001425111671185666.pdf → 
                  CNPJ=36303795000154 Razão=SILVINO FERREIRA DA ROCHA JUNIOR 
                  Data=11112025 Valor=8.884,00
[19:08:23] [CADASTRO] Preenchido automaticamente a partir da nota fiscal.
[19:08:57] [CADASTRO] Confirmado: SILVINO FERREIRA DA ROCHA JUNIOR | 
                      CNPJ 36303795000154 | Capital Social: R$ 2000 | 
                      Período 01/01/2025 a 31/12/2025 (ano 2025)
[19:09:17] [GERAR] Iniciando geração para o ano-calendário 2025...
[19:09:17] [GERAR] 1 nota(s), 0 despesa(s), 0 retirada(s), 
                   notas explicativas: sim.
[19:09:17] [GERAR] 157 linhas | I200 = 1 | J800 = 1
[19:09:19] [VALIDAR] 0 erro(s), 0 aviso(s).
[19:09:19] [INFO] Balanço equilibrado: R$ 8.884,00
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
