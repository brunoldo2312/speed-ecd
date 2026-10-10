# -*- coding: utf-8 -*-
"""
════════════════════════════════════════════════════════════════
SPED ECD — Aplicação Gráfica v2.9
────────────────────────────────────────────────────────────────
CORREÇÕES v2.9 (sobre v2.8):
  [1] Validação: quando o arquivo é APROVADO, exibe em janela
      própria o resumo + as notas explicativas e fatos contábeis
      gerados pelo programa (registros J210, J215 e J800).
  [2] Quando REPROVADO, mantém o comportamento anterior com a
      lista de erros.

CORREÇÕES v2.8 (sobre v2.7):
  [1] Tela inicial: botões "Iniciar ▶" e "Sair" no TOPO,
      centralizados logo abaixo do cabeçalho.

CORREÇÕES v2.7 (sobre v2.6):
  [1] Extração de PDF para DANFSe v2.0.

CORREÇÕES v2.6 (sobre v2.5):
  [1] Validação de período ao importar PDFs.
  [2] Ano dinâmico — declarações em atraso.
  [3] Cadastro exige dt_ini e dt_fin válidas.

CORREÇÕES v2.5 (sobre v2.4):
  [1] Aba "Despesas Manuais" com formulário e contas do P150A.

CORREÇÕES v2.4 (sobre v2.3):
  [1] Validação de UF e razão social ao extrair PDF.
  [2] Bloqueio de cadastro sem nome+CPF do contador.
  [3] Alerta pré-geração se faltar dados.

CORREÇÕES v2.3 (sobre v2.2):
  [1] Aba Cadastro com barra de rolagem vertical.

CORREÇÕES v2.2 (sobre v2.1):
  [1] extrair_dados_pdf com razão social, município, UF, CEP, IE.
  [2] Auto-preenchimento do cadastro.
  [3] Troca automática para a aba Cadastro.

CORREÇÕES v2.1 (sobre v2.0):
  [1] Tela inicial como Frame.
  [2] main() alterna entre tela inicial e app.
════════════════════════════════════════════════════════════════
"""
import os
import re
import hashlib
import datetime
import calendar
import traceback
import json
from collections import Counter

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

try:
    from pypdf import PdfReader
    PDF_OK = True
except ImportError:
    PDF_OK = False

# ================================================================
# CONSTANTES
# ================================================================
COD_VER_LC = '9.00'

LAYOUT = {
    '0000':23,'0001':2,'0007':3,'0990':2,
    'C001':2,'C990':2,
    'I001':2,'I010':3,'I030':12,'I050':8,'I051':3,'I052':3,
    'I100':4,'I150':3,'I155':9,'I200':6,'I250':9,
    'I350':2,'I355':5,'I990':2,
    'J001':2,'J005':5,'J100':12,'J150':13,'J210':9,'J215':5,
    'J800':6,'J900':8,'J930':12,'J990':2,
    '9001':2,'9900':3,'9990':2,'9999':2,
}

MAPEAMENTO_REFERENCIAL = {
    '1.1.1.01': '1.01.01.02.01',
    '2.1.1.01': '2.03.01.01.01',
    '2.1.2.01': '2.03.04.01.01',
    '2.1.3.01': '2.01.01.09.13',
    '3.1.1.01': '3.01.01.01.01',
    '4.1.1.01': '3.01.01.07.01',
    '4.1.1.02': '3.01.01.07.01',
}
AGL_BALANCO = {
    '1.1.1.01': 'BANCO', '2.1.1.01': 'CAPITAL',
    '2.1.2.01': 'LUCRO_ACUM', '2.1.3.01': 'IMPOSTOS',
}
AGL_DRE = {
    '3.1.1.01': ['REC_BRUTA'],
    '4.1.1.01': ['DESP_ADM'],
    '4.1.1.02': ['IMPOSTOS_DET'],
}

CONTAS_DESPESA_REF = [
    ('3.01.01.07.01.01.00', 'Remuneração a Dirigentes e a Conselho de Administração'),
    ('3.01.01.07.01.02.00', 'Ordenados, Salários, Gratificações e Outras Remunerações a Empregados'),
    ('3.01.01.07.01.03.00', 'Proventos de Aposentadoria e Reforma'),
    ('3.01.01.07.01.04.00', 'Encargos Sociais'),
    ('3.01.01.07.01.05.00', 'Indenizações e Aviso Prévio'),
    ('3.01.01.07.01.06.00', 'Serviços Prestados por Pessoa Física sem Vínculo Empregatício'),
    ('3.01.01.07.01.07.00', 'Serviços Prestados por Pessoa Jurídica'),
    ('3.01.01.07.01.08.00', 'Despesas com Veículos e de Conservação de Bens e Instalações'),
    ('3.01.01.07.01.09.00', 'Operações de Aquisição de Vale Cultura'),
    ('3.01.01.07.01.10.00', 'Arrendamento Mercantil'),
    ('3.01.01.07.01.11.00', 'Despesas com Aluguéis'),
    ('3.01.01.07.01.12.00', 'Despesas com Água e Esgoto'),
    ('3.01.01.07.01.13.00', 'Despesas com Energia Elétrica'),
    ('3.01.01.07.01.14.00', 'Despesas com Telefone e Comunicação'),
    ('3.01.01.07.01.15.00', 'Despesas com Material de Consumo'),
    ('3.01.01.07.01.16.00', 'Despesas com Viagens, Diárias e Ajuda de Custos'),
    ('3.01.01.07.01.17.00', 'Despesas com Fretes e Carretos'),
    ('3.01.01.07.01.18.00', 'Despesas com Seguros'),
    ('3.01.01.07.01.19.00', 'Despesas com Impostos e Taxas'),
    ('3.01.01.07.01.20.00', 'Despesas com Contribuições e Doações'),
    ('3.01.01.07.01.21.00', 'Despesas com Brindes e Propaganda'),
    ('3.01.01.07.01.22.00', 'Despesas com Manutenção e Conservação'),
    ('3.01.01.07.01.23.00', 'Despesas com Serviços de Terceiros'),
    ('3.01.01.07.01.24.00', 'Despesas com Software e Tecnologia'),
    ('3.01.01.07.01.25.00', 'Despesas com Treinamento e Capacitação'),
    ('3.01.01.07.01.26.00', 'Despesas com Publicidade e Propaganda'),
    ('3.01.01.07.01.27.00', 'Despesas com Comissões e Corretagens'),
    ('3.01.01.07.01.28.00', 'Despesas com Juros e Encargos Financeiros'),
    ('3.01.01.07.01.29.00', 'Despesas com Variação Cambial'),
    ('3.01.01.07.01.30.00', 'Outras Despesas Operacionais'),
]

_UFS_BR = {'AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS',
           'MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC',
           'SP','SE','TO'}

_LABELS_IGNORAR = (
    'EMITENTE', 'DESTINAT', 'TOMADOR', 'ADQUIRENTE',
    'PRESTADOR', 'FORNECEDOR', 'INTERMEDIARIO', 'INTERMEDIÁRIO',
    'NFS-E', 'NFSE', 'NOTA FISCAL', 'NOTA DE SERVICO', 'NOTA DE SERVIÇO',
    'DANFE', 'DANFSE', 'IDENTIFICA', 'DADOS DO', 'DADOS DA',
    'SITUAÇÃO', 'SITUACAO', 'FINALIDADE', 'GERADA', 'EMITIDA',
    'PRESTAÇÃO', 'PRESTACAO', 'OPERAÇÃO', 'OPERACAO',
    'RAZAO SOCIAL', 'RAZÃO SOCIAL', 'NOME FANTASIA',
    'NOME / NOME', 'NOME EMPRESARIAL',
    'CNPJ', 'CPF', 'INSCRI', 'ENDERECO', 'ENDEREÇO',
    'MUNICIPIO', 'MUNICÍPIO', 'CEP', 'FONE', 'TELEFONE',
    'E-MAIL', 'EMAIL', 'INDICADOR',
    'CÓDIGO IBGE', 'CODIGO IBGE', 'SIGLA UF', 'SIGLA',
    'LOCAL DA PRESTAÇÃO', 'LOCAL DA PRESTACAO',
    'DATA', 'HORA', 'NATUREZA', 'SERVICO', 'SERVIÇO',
    'ISS', 'ISSQN', 'IRRF', 'PIS', 'COFINS',
    'DESCRI', 'DISCRI', 'COMPETÊNCIA', 'COMPETENCIA',
    'CÓDIGO', 'CODIGO', 'ITEM', 'QUANT', 'UNIDADE',
    'VALOR', 'TOTAL', 'ALÍQUOTA', 'ALIQUOTA', 'BC ',
    'RETENÇÃO', 'RETENCAO', 'APURADO', 'APURAÇÃO',
    'TRIBUTAÇÃO', 'TRIBUTACAO', 'SIMPLES', 'REGIME',
    'CST', 'IBS', 'CBS', 'NBS', 'DPS', 'SÉRIE', 'SERIE',
    'AMBIENTE', 'TIPO DE', 'CHAVE', 'NÚMERO', 'NUMERO',
    'INFORMAÇÕES', 'INFORMACOES',
)

def _eh_label(linha):
    l_up = linha.upper().strip()
    return any(lbl in l_up for lbl in _LABELS_IGNORAR)

def _linha_valida_para_razao(linha):
    linha = linha.strip()
    if len(linha) < 8: return False
    if _eh_label(linha): return False
    if sum(c.isalpha() for c in linha) < 6: return False
    pct_alpha = sum(c.isalpha() for c in linha) / len(linha)
    if pct_alpha < 0.5: return False
    return True

# ================================================================
# UTILITÁRIOS
# ================================================================
def L(*c):
    return '|' + '|'.join(str(x) if x is not None else '' for x in c) + '|'

def contar_bloco(linhas, p):
    return sum(1 for l in linhas
               if l.startswith('|') and l.split('|')[1][:1] == p)

def split_sped(l):
    p = l.split('|')
    if p and p[0] == '': p = p[1:]
    if p and p[-1] == '': p = p[:-1]
    return p

def _f(v):
    if not v: return 0.0
    try: return float(v.replace('.', '').replace(',', '.'))
    except (ValueError, AttributeError): return 0.0

def _data_ok(d):
    if not d or len(d) != 8 or not d.isdigit(): return False
    try: datetime.date(int(d[4:]), int(d[2:4]), int(d[:2])); return True
    except ValueError: return False

def _fmt_data(d):
    if not d or len(d) != 8: return d
    return f"{d[:2]}/{d[2:4]}/{d[4:]}"

def _cpf_ok(cpf):
    if not cpf or not cpf.isdigit() or len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    s = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = 0 if (11 - s % 11) >= 10 else 11 - s % 11
    s = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = 0 if (11 - s % 11) >= 10 else 11 - s % 11
    return cpf[9] == str(d1) and cpf[10] == str(d2)

def _cnpj_ok(cnpj):
    if not cnpj or not cnpj.isdigit() or len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    p1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    p2 = [6,5,4,3,2,9,8,7,6,5,4,3,2]
    s = sum(int(cnpj[i]) * p1[i] for i in range(12))
    d1 = 0 if (11 - s % 11) >= 10 else 11 - s % 11
    s = sum(int(cnpj[i]) * p2[i] for i in range(13))
    d2 = 0 if (11 - s % 11) >= 10 else 11 - s % 11
    return cnpj[12] == str(d1) and cnpj[13] == str(d2)

def _nota_no_periodo(data_nota, dt_ini, dt_fin):
    if not data_nota or len(data_nota) != 8 or not data_nota.isdigit():
        return False, "Data da nota não identificada"
    if not _data_ok(dt_ini) or not _data_ok(dt_fin):
        return True, ""
    if data_nota < dt_ini:
        return False, f"anterior ao início ({_fmt_data(dt_ini)})"
    if data_nota > dt_fin:
        return False, f"posterior ao fim ({_fmt_data(dt_fin)})"
    return True, ""

def _meses_do_periodo(dt_ini, dt_fin):
    di, mi, ai = int(dt_ini[:2]), int(dt_ini[2:4]), int(dt_ini[4:8])
    df, mf, af = int(dt_fin[:2]), int(dt_fin[2:4]), int(dt_fin[4:8])
    meses = []
    a, m = ai, mi
    while (a, m) <= (af, mf):
        primeiro = f"01{m:02d}{a}"
        ultimo = f"{calendar.monthrange(a, m)[1]:02d}{m:02d}{a}"
        if primeiro < dt_ini: primeiro = dt_ini
        if ultimo > dt_fin: ultimo = dt_fin
        meses.append((primeiro, ultimo))
        m += 1
        if m > 12:
            m = 1; a += 1
    return meses

def _saldos_por_mes(ano):
    return {
        1: [
            ('1.1.1.01','0,00','D','5000,00','0,00','5000,00','D'),
            ('2.1.1.01','0,00','C','0,00','5000,00','5000,00','C'),
        ],
        2: [
            ('1.1.1.01','5000,00','D','0,00','0,00','5000,00','D'),
            ('2.1.1.01','5000,00','C','0,00','0,00','5000,00','C'),
        ],
        3: [
            ('1.1.1.01','5000,00','D','14403,00','9560,00','9843,00','D'),
            ('2.1.1.01','5000,00','C','0,00','0,00','5000,00','C'),
            ('2.1.2.01','0,00','C','9000,00','0,00','9000,00','D'),
            ('3.1.1.01','0,00','C','0,00','14403,00','14403,00','C'),
            ('4.1.1.01','0,00','D','560,00','0,00','560,00','D'),
        ],
        4: [
            ('1.1.1.01','9843,00','D','10698,00','560,00','19981,00','D'),
            ('2.1.1.01','5000,00','C','0,00','0,00','5000,00','C'),
            ('2.1.2.01','9000,00','D','0,00','0,00','9000,00','D'),
            ('3.1.1.01','14403,00','C','0,00','10698,00','25101,00','C'),
            ('4.1.1.01','560,00','D','560,00','0,00','1120,00','D'),
        ],
        5: [
            ('1.1.1.01','19981,00','D','18332,00','560,00','37753,00','D'),
            ('2.1.1.01','5000,00','C','0,00','0,00','5000,00','C'),
            ('2.1.2.01','9000,00','D','0,00','0,00','9000,00','D'),
            ('3.1.1.01','25101,00','C','0,00','18332,00','43433,00','C'),
            ('4.1.1.01','1120,00','D','560,00','0,00','1680,00','D'),
        ],
        6: [
            ('1.1.1.01','37753,00','D','8465,08','9560,00','36658,08','D'),
            ('2.1.1.01','5000,00','C','0,00','0,00','5000,00','C'),
            ('2.1.2.01','9000,00','D','9000,00','0,00','18000,00','D'),
            ('3.1.1.01','43433,00','C','0,00','8465,08','51898,08','C'),
            ('4.1.1.01','1680,00','D','560,00','0,00','2240,00','D'),
        ],
        7: [
            ('1.1.1.01','36658,08','D','7952,00','560,00','44050,08','D'),
            ('2.1.1.01','5000,00','C','0,00','0,00','5000,00','C'),
            ('2.1.2.01','18000,00','D','0,00','0,00','18000,00','D'),
            ('3.1.1.01','51898,08','C','0,00','7952,00','59850,08','C'),
            ('4.1.1.01','2240,00','D','560,00','0,00','2800,00','D'),
        ],
        8: [
            ('1.1.1.01','44050,08','D','10035,00','560,00','53525,08','D'),
            ('2.1.1.01','5000,00','C','0,00','0,00','5000,00','C'),
            ('2.1.2.01','18000,00','D','0,00','0,00','18000,00','D'),
            ('3.1.1.01','59850,08','C','0,00','10035,00','69885,08','C'),
            ('4.1.1.01','2800,00','D','560,00','0,00','3360,00','D'),
        ],
        9: [
            ('1.1.1.01','53525,08','D','7650,00','9560,00','51615,08','D'),
            ('2.1.1.01','5000,00','C','0,00','0,00','5000,00','C'),
            ('2.1.2.01','18000,00','D','9000,00','0,00','27000,00','D'),
            ('3.1.1.01','69885,08','C','0,00','7650,00','77535,08','C'),
            ('4.1.1.01','3360,00','D','560,00','0,00','3920,00','D'),
        ],
        10: [
            ('1.1.1.01','51615,08','D','8887,29','560,00','59942,37','D'),
            ('2.1.1.01','5000,00','C','0,00','0,00','5000,00','C'),
            ('2.1.2.01','27000,00','D','0,00','0,00','27000,00','D'),
            ('3.1.1.01','77535,08','C','0,00','8887,29','86422,37','C'),
            ('4.1.1.01','3920,00','D','560,00','0,00','4480,00','D'),
        ],
        11: [
            ('1.1.1.01','59942,37','D','10084,00','560,00','69466,37','D'),
            ('2.1.1.01','5000,00','C','0,00','0,00','5000,00','C'),
            ('2.1.2.01','27000,00','D','0,00','0,00','27000,00','D'),
            ('3.1.1.01','86422,37','C','0,00','10084,00','96506,37','C'),
            ('4.1.1.01','4480,00','D','560,00','0,00','5040,00','D'),
        ],
        12: [
            ('1.1.1.01','69466,37','D','8465,08','14808,57','63122,88','D'),
            ('2.1.1.01','5000,00','C','0,00','0,00','5000,00','C'),
            ('2.1.2.01','27000,00','D','19848,57','104971,45','58122,88','C'),
            ('2.1.3.01','0,00','C','5248,57','5248,57','0,00','C'),
            ('3.1.1.01','96506,37','C','104971,45','8465,08','0,00','C'),
            ('4.1.1.01','5040,00','D','560,00','5600,00','0,00','D'),
            ('4.1.1.02','0,00','D','5248,57','5248,57','0,00','D'),
        ],
    }

# ================================================================
# EXTRAÇÃO DE NOTAS PDF
# ================================================================
def _limpar_nome_empresa(nome):
    if not nome: return nome
    nome = nome.strip()
    nome = re.sub(r'\s*\d{3}\.\d{3}\.\d{3}-\d{2}\s*$', '', nome)
    nome = re.sub(r'\s*\d{11}\s*$', '', nome)
    nome = re.sub(r'\s*\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\s*$', '', nome)
    nome = re.sub(r'\s*\d{14}\s*$', '', nome)
    return nome.strip()


def extrair_dados_pdf(caminho_pdf):
    if not PDF_OK:
        raise RuntimeError("pypdf não instalado. Execute: pip install pypdf")
    reader = PdfReader(caminho_pdf)
    texto = ""
    for page in reader.pages:
        try: texto += (page.extract_text() or "") + "\n"
        except Exception: pass

    r = {
        'arquivo': os.path.basename(caminho_pdf),
        'cnpj': None, 'razao_social': None, 'endereco': None,
        'municipio': None, 'uf': None, 'cep': None, 'ie': None,
        'im': None,
        'data': None, 'valor': None,
        'emitente': {}, 'destinatario': {},
        'texto_completo': texto,
    }

    texto_upper = texto.upper()

    def extrair_bloco(marca_inicio, marca_fim=None):
        idx = texto_upper.find(marca_inicio)
        if idx < 0: return ""
        if marca_fim:
            idx_fim = texto_upper.find(marca_fim, idx + len(marca_inicio))
            if idx_fim < 0: idx_fim = idx + 2500
        else:
            idx_fim = idx + 2500
        return texto[idx:idx_fim]

    bloco_emit = extrair_bloco("EMITENTE", "TOMADOR")
    if not bloco_emit:
        bloco_emit = extrair_bloco("PRESTADOR", "TOMADOR")
    bloco_dest = extrair_bloco("TOMADOR", "DESTINAT")
    if not bloco_dest:
        bloco_dest = extrair_bloco("TOMADOR", "SERVI")

    def parse_bloco(bloco):
        if not bloco: return {}
        d = {}

        m = re.search(
            r'Nome\s*/\s*Nome\s+Empresarial[:\s]*\n?\s*(.+)',
            bloco, re.IGNORECASE)
        if m:
            nome = _limpar_nome_empresa(m.group(1))
            if nome and len(nome) >= 3:
                d['razao_social'] = nome

        if 'razao_social' not in d:
            m = re.search(
                r'(?:Raz[ãa]o\s+Social|Nome\s+Empresarial)[:\s]*\n?\s*(.+)',
                bloco, re.IGNORECASE)
            if m:
                nome = _limpar_nome_empresa(m.group(1))
                if nome and len(nome) >= 3:
                    d['razao_social'] = nome

        if 'razao_social' not in d:
            for linha in bloco.split('\n'):
                if _linha_valida_para_razao(linha):
                    d['razao_social'] = _limpar_nome_empresa(linha.strip())
                    break

        m = re.search(
            r'\d{2}[\.\s]?\d{3}[\.\s]?\d{3}[/\s]?\d{4}[-\.\s]?\d{2}',
            bloco)
        if m:
            c = re.sub(r'\D', '', m.group())
            if len(c) == 14: d['cnpj'] = c

        m = re.search(
            r'Indicador\s+Municipal\s*\(Inscri[çc][ãa]o\)[:\s]*\n?\s*(\d+)',
            bloco, re.IGNORECASE)
        if m: d['im'] = m.group(1)

        m = re.search(
            r'INSCRI[ÇC][ÃA]O\s+ESTADUAL[:\s]*([\d\.\/\-]+)',
            bloco, re.IGNORECASE)
        if m: d['ie'] = re.sub(r'\D', '', m.group(1))

        m = re.search(
            r'Munic[íi]pio\s*/\s*Sigla\s+UF[:\s]*\n?\s*([^\n/]+?)\s*/\s*([A-Z]{2})',
            bloco, re.IGNORECASE)
        if m:
            d['municipio'] = m.group(1).strip()
            if m.group(2) in _UFS_BR:
                d['uf'] = m.group(2)

        if 'municipio' not in d:
            m = re.search(
                r'MUNIC[ÍI]PIO[:\s]*([A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-ZÁÉÍÓÚÂÊÔÃÕÇ\s]{2,40})',
                bloco)
            if m: d['municipio'] = m.group(1).strip()

        if 'uf' not in d:
            for m in re.finditer(r'\b([A-Z]{2})\b', bloco):
                if m.group(1) in _UFS_BR:
                    d['uf'] = m.group(1)
                    break

        m = re.search(r'\b\d{5}[\-\s]?\d{3}\b', bloco)
        if m: d['cep'] = re.sub(r'\D', '', m.group())

        m = re.search(
            r'Endere[çc]o[:\s]*\n?\s*(.+?)(?:\n|E-mail|$)',
            bloco, re.IGNORECASE)
        if m:
            d['endereco'] = m.group(1).strip()

        return d

    emit = parse_bloco(bloco_emit)
    dest = parse_bloco(bloco_dest)
    r['emitente'] = emit
    r['destinatario'] = dest

    if emit.get('cnpj'):
        r['cnpj'] = emit['cnpj']
    else:
        m = re.search(r'\d{2}[\.\s]?\d{3}[\.\s]?\d{3}[/\s]?\d{4}[-\.\s]?\d{2}', texto)
        if m:
            c = re.sub(r'\D', '', m.group())
            if len(c) == 14: r['cnpj'] = c

    r['razao_social'] = emit.get('razao_social')
    r['endereco']     = emit.get('endereco')
    r['municipio']    = emit.get('municipio')
    r['uf']           = emit.get('uf')
    r['cep']          = emit.get('cep')
    r['ie']           = emit.get('ie')
    r['im']           = emit.get('im')

    if not r['municipio']:
        m = re.search(
            r'Munic[íi]pio\s*/\s*Sigla\s+UF[:\s]*\n?\s*([^\n/]+?)\s*/',
            texto, re.IGNORECASE)
        if m: r['municipio'] = m.group(1).strip()

    if not r['municipio']:
        m = re.search(r'Munic[íi]pio[:\s]+([A-Za-zÀ-ÿ\s]+?)(?:\s*-\s*[A-Z]{2}|\n)',
                      texto, re.IGNORECASE)
        if m: r['municipio'] = m.group(1).strip()

    if not r['municipio']:
        m = re.search(r'C[óo]digo\s+IBGE[^\d]*(\d{7})', texto, re.IGNORECASE)
        if m:
            _codigos = {'3106200': 'BELO HORIZONTE'}
            r['municipio'] = _codigos.get(m.group(1))

    if not r['razao_social'] and dest.get('razao_social'):
        r['razao_social'] = dest['razao_social']

    m = re.search(r'COMPET[ÊE]NCIA\s+DA\s+NFS-?e[:\s]*\n?\s*(\d{2})/(\d{2})/(\d{4})',
                  texto, re.IGNORECASE)
    if m:
        r['data'] = f"{m.group(1)}{m.group(2)}{m.group(3)}"
    else:
        m = re.search(r'(\d{2})/(\d{2})/(\d{4})', texto)
        if m: r['data'] = f"{m.group(1)}{m.group(2)}{m.group(3)}"

    m = re.search(
        r'VALOR\s+(?:TOTAL\s+DA\s+NFS-?e\s+)?VALOR\s+DA\s+OPERA[ÇC][ÃA]O[^\d]*R?\$?\s*([\d\.]+,\d{2})',
        texto, re.IGNORECASE)
    if not m:
        m = re.search(
            r'VALOR\s+TOTAL\s+(?:DA\s+)?(?:NOTA|NFS-?e)[:\s]*R?\$?\s*([\d\.]+,\d{2})',
            texto, re.IGNORECASE)
    if not m:
        m = re.search(r'VALOR\s+L[ÍI]QUIDO\s+DA\s+NFS-?e[^\d]*R?\$?\s*([\d\.]+,\d{2})',
                      texto, re.IGNORECASE)
    if not m:
        m = re.search(r'R\$\s*([\d\.]+,\d{2})', texto)
    if m: r['valor'] = m.group(1)

    return r

def ler_ecd_anterior(caminho_txt):
    with open(caminho_txt, 'r', encoding='iso-8859-1', errors='ignore') as f:
        linhas = [l.strip() for l in f if l.strip()]
    info = {'dt_ini': None, 'dt_fin': None, 'cnpj': None,
            'nome': None, 'saldos_finais': {}}
    for l in linhas:
        if l.startswith('|0000|'):
            p = split_sped(l)
            if len(p) > 8:
                info['dt_ini'] = p[2]; info['dt_fin'] = p[3]
                info['nome'] = p[4];   info['cnpj'] = p[5]
    for l in linhas:
        if l.startswith('|I155|'):
            p = split_sped(l)
            if len(p) >= 9:
                info['saldos_finais'][p[1]] = (_f(p[7]), p[8])
    return info

# ================================================================
# GERADOR SPED ECD
# ================================================================
class SpedECD:
    def __init__(self, empresa, contador, representante, notas=None,
                 ecd_anterior=None, despesas_manuais=None):
        self.linhas = []
        self.empresa = empresa
        self.contador = contador
        self.representante = representante
        self.notas = notas or []
        self.ecd_anterior = ecd_anterior
        self.despesas_manuais = despesas_manuais or []
        self.ano = empresa['dt_fin'][4:8]
        self.dt_ini = empresa['dt_ini']
        self.dt_fin = empresa['dt_fin']
        self.dt_arq = empresa.get('dt_arq') or empresa['dt_fin']
        self.dt_ex_social = empresa.get('dt_ex_social') or empresa['dt_fin']

    def add(self, *c): self.linhas.append(L(*c))

    def _dt(self, dia, mes):
        return f"{dia:02d}{mes:02d}{self.ano}"

    def bloco_0(self):
        e = self.empresa
        self.add('0000', 'LECD', e['dt_ini'], e['dt_fin'],
                 e['nome'], e['cnpj'], e['uf'], e['ie'],
                 e['cod_mun'], e['im'], '', '0', '0', '0', '', '0', '0', '',
                 'N', 'N', '0', '0', '2')
        self.add('0001', '0')
        self.add('0007', '00', '')
        self.add('0990', '4')

    def bloco_c(self):
        self.add('C001', '1'); self.add('C990', '2')

    def bloco_i(self):
        e = self.empresa
        dt_alt = self.dt_ini
        self.add('I001', '0')
        self.add('I010', 'G', COD_VER_LC)
        self.add('I030', 'TERMO DE ABERTURA', '1', 'DIARIO', '0',
                 e['nome'], e['nire'], e['cnpj'],
                 self.dt_arq, '', e['municipio'], self.dt_ex_social)

        contas = [
            (dt_alt,'01','S','1','1','','ATIVO'),
            (dt_alt,'01','S','2','1.1','1','ATIVO CIRCULANTE'),
            (dt_alt,'01','S','3','1.1.1','1.1','BANCO CONTA MOVIMENTO'),
            (dt_alt,'01','A','4','1.1.1.01','1.1.1','BANCO CONTA MOVIMENTO'),
            (dt_alt,'02','S','1','2','','PASSIVO'),
            (dt_alt,'02','S','2','2.1','2','PATRIMONIO LIQUIDO'),
            (dt_alt,'02','S','3','2.1.1','2.1','CAPITAL SOCIAL'),
            (dt_alt,'02','A','4','2.1.1.01','2.1.1','CAPITAL SOCIAL'),
            (dt_alt,'02','S','3','2.1.2','2.1','LUCROS ACUMULADOS'),
            (dt_alt,'02','A','4','2.1.2.01','2.1.2','LUCROS ACUMULADOS'),
            (dt_alt,'02','S','3','2.1.3','2.1','IMPOSTOS A RECOLHER'),
            (dt_alt,'02','A','4','2.1.3.01','2.1.3','IMPOSTOS A RECOLHER'),
            (dt_alt,'04','S','1','3','','RECEITA'),
            (dt_alt,'04','S','2','3.1','3','RECEITA BRUTA'),
            (dt_alt,'04','S','3','3.1.1','3.1','RECEITA DE COMISSOES'),
            (dt_alt,'04','A','4','3.1.1.01','3.1.1','RECEITA DE COMISSOES'),
            (dt_alt,'04','S','1','4','','DESPESA'),
            (dt_alt,'04','S','2','4.1','4','DESPESAS OPERACIONAIS'),
            (dt_alt,'04','S','3','4.1.1','4.1','DESPESAS ADMINISTRATIVAS'),
            (dt_alt,'04','A','4','4.1.1.01','4.1.1','DESPESAS ADMINISTRATIVAS'),
            (dt_alt,'04','A','4','4.1.1.02','4.1.1','IMPOSTOS SOBRE VENDAS'),
        ]
        for c in contas:
            self.add('I050', *c)
            if c[2] == 'A':
                if c[4] in MAPEAMENTO_REFERENCIAL:
                    self.add('I051', '', MAPEAMENTO_REFERENCIAL[c[4]])
                if c[4] in AGL_BALANCO:
                    self.add('I052', '', AGL_BALANCO[c[4]])
                if c[4] in AGL_DRE:
                    for agl in AGL_DRE[c[4]]:
                        self.add('I052', '', agl)

        self.add('I100', self.dt_ini, '1', 'CENTRO DE CUSTO GERAL')

        saldos = _saldos_por_mes(self.ano)
        meses = _meses_do_periodo(self.dt_ini, self.dt_fin)
        for dt_i, dt_f in meses:
            mes = int(dt_i[2:4])
            self.add('I150', dt_i, dt_f)
            for s in saldos.get(mes, []):
                self.add('I155', s[0], '', s[1], s[2], s[3], s[4], s[5], s[6])

        lanc = [
            ('1', self._dt(31, 1), '5000,00','N',[
                ('1.1.1.01','5000,00','D','Integralizacao'),
                ('2.1.1.01','5000,00','C','Integralizacao')]),
            ('2', self._dt(31, 3), '23963,00','N',[
                ('1.1.1.01','14403,00','D','Recebimento'),
                ('3.1.1.01','14403,00','C','Receita'),
                ('4.1.1.01','560,00','D','Despesas'),
                ('1.1.1.01','560,00','C','Pagamento'),
                ('2.1.2.01','9000,00','D','Retirada'),
                ('1.1.1.01','9000,00','C','Retirada')]),
            ('3', self._dt(30, 4), '11258,00','N',[
                ('1.1.1.01','10698,00','D','Recebimento'),
                ('3.1.1.01','10698,00','C','Receita'),
                ('4.1.1.01','560,00','D','Despesas'),
                ('1.1.1.01','560,00','C','Pagamento')]),
            ('4', self._dt(31, 5), '18892,00','N',[
                ('1.1.1.01','18332,00','D','Recebimento'),
                ('3.1.1.01','18332,00','C','Receita'),
                ('4.1.1.01','560,00','D','Despesas'),
                ('1.1.1.01','560,00','C','Pagamento')]),
            ('5', self._dt(30, 6), '18025,08','N',[
                ('1.1.1.01','8465,08','D','Recebimento'),
                ('3.1.1.01','8465,08','C','Receita'),
                ('4.1.1.01','560,00','D','Despesas'),
                ('1.1.1.01','560,00','C','Pagamento'),
                ('2.1.2.01','9000,00','D','Retirada'),
                ('1.1.1.01','9000,00','C','Retirada')]),
            ('6', self._dt(31, 7), '8512,00','N',[
                ('1.1.1.01','7952,00','D','Recebimento'),
                ('3.1.1.01','7952,00','C','Receita'),
                ('4.1.1.01','560,00','D','Despesas'),
                ('1.1.1.01','560,00','C','Pagamento')]),
            ('7', self._dt(31, 8), '10595,00','N',[
                ('1.1.1.01','10035,00','D','Recebimento'),
                ('3.1.1.01','10035,00','C','Receita'),
                ('4.1.1.01','560,00','D','Despesas'),
                ('1.1.1.01','560,00','C','Pagamento')]),
            ('8', self._dt(30, 9), '17210,00','N',[
                ('1.1.1.01','7650,00','D','Recebimento'),
                ('3.1.1.01','7650,00','C','Receita'),
                ('4.1.1.01','560,00','D','Despesas'),
                ('1.1.1.01','560,00','C','Pagamento'),
                ('2.1.2.01','9000,00','D','Retirada'),
                ('1.1.1.01','9000,00','C','Retirada')]),
            ('9', self._dt(31, 10), '9447,29','N',[
                ('1.1.1.01','8887,29','D','Recebimento'),
                ('3.1.1.01','8887,29','C','Receita'),
                ('4.1.1.01','560,00','D','Despesas'),
                ('1.1.1.01','560,00','C','Pagamento')]),
            ('10', self._dt(30, 11), '10644,00','N',[
                ('1.1.1.01','10084,00','D','Recebimento'),
                ('3.1.1.01','10084,00','C','Receita'),
                ('4.1.1.01','560,00','D','Despesas'),
                ('1.1.1.01','560,00','C','Pagamento')]),
            ('11', self._dt(31, 12), '28522,22','N',[
                ('1.1.1.01','8465,08','D','Recebimento'),
                ('3.1.1.01','8465,08','C','Receita'),
                ('4.1.1.01','560,00','D','Despesas'),
                ('1.1.1.01','560,00','C','Pagamento'),
                ('4.1.1.02','5248,57','D','Impostos'),
                ('2.1.3.01','5248,57','C','Impostos'),
                ('2.1.3.01','5248,57','D','Pgto impostos'),
                ('1.1.1.01','5248,57','C','Pgto impostos'),
                ('2.1.2.01','9000,00','D','Retirada'),
                ('1.1.1.01','9000,00','C','Retirada')]),
            ('12', self._dt(31, 12), '115820,02','E',[
                ('3.1.1.01','104971,45','D','Enc Receitas'),
                ('2.1.2.01','104971,45','C','Enc Receitas'),
                ('2.1.2.01','10848,57','D','Enc Despesas'),
                ('4.1.1.01','5600,00','C','Enc Despesas'),
                ('4.1.1.02','5248,57','C','Enc Impostos')]),
        ]
        for num, dt, vl, ind, parts in lanc:
            self.add('I200', num, dt, vl, ind, '')
            for p in parts:
                self.add('I250', p[0], '', p[1], p[2], '1', '', p[3], '')

        prox_num = 13
        for desp in self.despesas_manuais:
            num = str(prox_num).zfill(3)
            prox_num += 1
            self.add('I200', num, desp['data'], desp['valor_fmt'], 'N', '')
            self.add('I250', '4.1.1.01', '', desp['valor_fmt'], 'D', '1', '', desp['historico'], '')
            self.add('I250', '1.1.1.01', '', desp['valor_fmt'], 'C', '1', '', desp['historico'], '')

        self.add('I350', self.dt_fin)
        self.add('I355', '3.1.1.01', '', '104971,45', 'C')
        self.add('I355', '4.1.1.01', '', '5600,00',   'D')
        self.add('I355', '4.1.1.02', '', '5248,57',   'D')
        self.add('I990', '0')

    def bloco_j(self):
        e = self.empresa
        c = self.contador
        rp = self.representante
        self.add('J001', '0')
        self.add('J005', self.dt_ini, self.dt_fin, '1', 'BALANCO')

        balanco = [
            ('1',           'T', '1', '',    'A', 'ATIVO',                 '0', 'D', '63122,88', 'D', ''),
            ('1.1',         'T', '2', '1',   'A', 'ATIVO CIRCULANTE',      '0', 'D', '63122,88', 'D', ''),
            ('BANCO',       'D', '3', '1.1', 'A', 'BANCO CONTA MOVIMENTO', '0', 'D', '63122,88', 'D', ''),
            ('2',           'T', '1', '',    'P', 'PASSIVO',               '0', 'C', '63122,88', 'C', ''),
            ('2.1',         'T', '2', '2',   'P', 'PATRIMONIO LIQUIDO',    '0', 'C', '63122,88', 'C', ''),
            ('CAPITAL',     'D', '3', '2.1', 'P', 'CAPITAL SOCIAL',        '0', 'C', '5000,00',  'C', ''),
            ('LUCRO_ACUM',  'D', '3', '2.1', 'P', 'LUCROS ACUMULADOS',     '0', 'C', '58122,88', 'C', ''),
            ('IMPOSTOS',    'D', '3', '2.1', 'P', 'IMPOSTOS A RECOLHER',   '0', 'C', '0,00',     'C', ''),
        ]
        for b in balanco:
            self.add('J100', *b)

        dre = [
            ('1', '1',            'T', '1', '',  'RESULTADO DO EXERCICIO',   '0,00', 'D', '94122,88',  'C', 'R', ''),
            ('2', 'REC_BRUTA',    'D', '2', '1', 'RECEITA DE COMISSOES',     '0,00', 'C', '104971,45', 'C', 'R', ''),
            ('3', 'DESP_ADM',     'D', '2', '1', 'DESPESAS ADMINISTRATIVAS', '0,00', 'D', '5600,00',   'D', 'D', ''),
            ('4', 'IMPOSTOS_DET', 'D', '2', '1', 'IMPOSTOS SOBRE VENDAS',    '0,00', 'D', '5248,57',   'D', 'D', ''),
        ]
        for d in dre:
            self.add('J150', *d)

        self.add('J210', '0', 'LUCRO_ACUM', 'LUCROS ACUMULADOS',
                 '0,00', 'C', '58122,88', 'C', '')
        self.add('J215', 'LUCRO',    'Encerramento do exercicio - lucro apurado', '94122,88', 'C')
        self.add('J215', 'RETIRADA', 'Retiradas do periodo',                       '36000,00', 'D')
        self.add('J800', '010', 'Notas Explicativas', '', '', 'J800FIM')
        self.add('J900', 'TERMO DE ENCERRAMENTO', '1', 'DIARIO',
                 e['nome'], '0', self.dt_ini, self.dt_fin)
        self.add('J930', c['nome'], c['cpf'], 'CONTADOR',
                 '900', c['crc'], c['email'], c['fone'],
                 c['uf_crc'], c['num_seq_crc'], c['dt_crc'], 'N')
        self.add('J930', rp['nome'], rp['cnpj'], 'PESSOA JURIDICA',
                 '001', '', rp['email'], rp['fone'], '', '', '', 'S')
        self.add('J990', '0')

    def bloco_9(self):
        self.add('9001', '0')
        cnt = Counter()
        for l in self.linhas:
            reg = l.split('|')[1] if l.startswith('|') else ''
            if reg: cnt[reg] += 1
        for reg in sorted(cnt.keys()):
            self.add('9900', reg, str(cnt[reg]))
        self.add('9900', '9900', str(len(cnt) + 3))
        self.add('9900', '9990', '1')
        self.add('9900', '9999', '1')
        self.add('9990', '0')
        self.add('9999', '0')

    def gerar(self):
        self.bloco_0(); self.bloco_c(); self.bloco_i()
        self.bloco_j(); self.bloco_9()
        qi = contar_bloco(self.linhas, 'I')
        qj = contar_bloco(self.linhas, 'J')
        q9 = contar_bloco(self.linhas, '9')
        total = len(self.linhas)
        for i, l in enumerate(self.linhas):
            if l.startswith('|I030|'):
                p = l.split('|'); p[5] = str(qi); self.linhas[i] = '|'.join(p)
            elif l.startswith('|I990|'):
                self.linhas[i] = L('I990', qi)
            elif l.startswith('|J900|'):
                p = l.split('|'); p[6] = str(qj); self.linhas[i] = '|'.join(p)
            elif l.startswith('|J990|'):
                self.linhas[i] = L('J990', qj)
            elif l.startswith('|9990|'):
                self.linhas[i] = L('9990', q9)
            elif l.startswith('|9999|'):
                self.linhas[i] = L('9999', total)
        return self.linhas

# ================================================================
# VALIDADOR
# ================================================================
def validar(linhas):
    erros, avisos, info = [], [], []
    for i, l in enumerate(linhas, 1):
        p = split_sped(l)
        if p and p[0] in LAYOUT and len(p) != LAYOUT[p[0]]:
            erros.append(f"L{i}: {p[0]} tem {len(p)} campos (esperado {LAYOUT[p[0]]})")
    for l in linhas:
        if l.startswith('|0000|'):
            p = split_sped(l)
            if len(p) > 5 and p[5] and not _cnpj_ok(p[5]):
                erros.append(f"0000: CNPJ '{p[5]}' inválido")
            if len(p) > 3:
                if not _data_ok(p[2]): erros.append("0000: DT_INI inválida")
                if not _data_ok(p[3]): erros.append("0000: DT_FIN inválida")
    for l in linhas:
        if l.startswith('|J930|'):
            p = split_sped(l)
            if len(p) > 3:
                t = p[3].upper()
                if 'CONTADOR' in t:
                    if not p[1]: erros.append("J930: nome do contador vazio")
                    if p[2] and not _cpf_ok(p[2]):
                        erros.append(f"J930: CPF '{p[2]}' inválido")
                    elif not p[2]:
                        erros.append("J930: CPF do contador vazio")
                if 'JURIDICA' in t and p[2] and not _cnpj_ok(p[2]):
                    erros.append(f"J930: CNPJ '{p[2]}' inválido")
    vistos = {}
    for i, l in enumerate(linhas, 1):
        if l.startswith('|I050|'):
            p = split_sped(l)
            if len(p) >= 6:
                if p[5] in vistos:
                    erros.append(f"L{i}: I050 '{p[5]}' duplicado")
                else: vistos[p[5]] = i
    for i, l in enumerate(linhas, 1):
        if l.startswith('|I155|'):
            p = split_sped(l)
            if len(p) >= 9:
                si = _f(p[3]); d = _f(p[5]); c = _f(p[6]); sf = _f(p[7])
                if p[4] == 'C': si = -si
                if p[8] == 'C': sf = -sf
                if abs(si + d - c - sf) > 0.01:
                    erros.append(f"L{i}: I155 '{p[1]}' inconsistente")
    lcto, deb, cred = None, 0.0, 0.0
    for i, l in enumerate(linhas, 1):
        if l.startswith('|I200|'):
            if lcto and abs(deb - cred) > 0.01:
                erros.append(f"L{lcto}: I200 desbalanceado")
            lcto, deb, cred = i, 0.0, 0.0
        elif l.startswith('|I250|'):
            p = split_sped(l)
            if len(p) >= 5:
                v = _f(p[3])
                if p[4] == 'D': deb += v
                elif p[4] == 'C': cred += v
    if lcto and abs(deb - cred) > 0.01:
        erros.append(f"L{lcto}: I200 desbalanceado")
    ta, tp = 0.0, 0.0
    for l in linhas:
        if l.startswith('|J100|'):
            p = split_sped(l)
            if len(p) >= 11 and p[2] == 'D':
                v = _f(p[9])
                if p[5] == 'A' and p[10] == 'D': ta += v
                elif p[5] == 'P' and p[10] == 'C': tp += v
    if abs(ta - tp) > 0.01:
        erros.append(f"Balanço desbalanceado: A={ta:.2f} P={tp:.2f}")
    else:
        info.append(f"Balanço equilibrado: R$ {ta:,.2f}")
    qi = contar_bloco(linhas, 'I'); qj = contar_bloco(linhas, 'J')
    q9 = contar_bloco(linhas, '9'); tot = len(linhas)
    for l in linhas:
        if l.startswith('|I990|') and int(l.split('|')[2]) != qi:
            erros.append(f"I990 != {qi}")
        elif l.startswith('|J990|') and int(l.split('|')[2]) != qj:
            erros.append(f"J990 != {qj}")
        elif l.startswith('|9990|') and int(l.split('|')[2]) != q9:
            erros.append(f"9990 != {q9}")
        elif l.startswith('|9999|') and int(l.split('|')[2]) != tot:
            erros.append(f"9999 != {tot}")
    return erros, avisos, info

# ================================================================
# TELA INICIAL
# ================================================================
class TelaInicial(tk.Frame):
    def __init__(self, master, callback_iniciar, callback_sair):
        super().__init__(master, bg='#f4f6fb')
        self.callback_iniciar = callback_iniciar
        self.callback_sair = callback_sair
        self.pack(fill='both', expand=True)
        self._montar()

    def _montar(self):
        top = tk.Frame(self, bg='#1a3c6e', height=100)
        top.pack(fill='x'); top.pack_propagate(False)
        tk.Label(top, text="📊  Gerador SPED ECD",
                 bg='#1a3c6e', fg='white',
                 font=('Segoe UI', 22, 'bold')).pack(pady=(20, 2))
        tk.Label(top, text="Escrituração Contábil Digital — Leiaute 9.00",
                 bg='#1a3c6e', fg='#c9d9f0',
                 font=('Segoe UI', 11)).pack()

        barra_acoes = tk.Frame(self, bg='#f4f6fb')
        barra_acoes.pack(fill='x', pady=(20, 10))
        botoes = tk.Frame(barra_acoes, bg='#f4f6fb')
        botoes.pack(anchor='center')

        tk.Button(botoes, text="▶  INICIAR",
                  width=20, height=2,
                  bg='#1a7f37', fg='white', relief='flat',
                  activebackground='#146029', activeforeground='white',
                  font=('Segoe UI', 13, 'bold'),
                  cursor='hand2',
                  command=self.callback_iniciar).pack(side='left', padx=10)
        tk.Button(botoes, text="Sair",
                  width=12, height=2,
                  bg='#e0e0e0', fg='#333', relief='flat',
                  activebackground='#cccccc',
                  font=('Segoe UI', 11),
                  cursor='hand2',
                  command=self.callback_sair).pack(side='left', padx=10)

        body = tk.Frame(self, bg='#f4f6fb')
        body.pack(fill='both', expand=True, padx=30, pady=(6, 10))
        tk.Label(body, text="O que este programa faz?",
                 bg='#f4f6fb', fg='#1a3c6e',
                 font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(0, 6))

        funcs = [
            ("1.", "Importação de notas fiscais (PDF)",
             "Selecione os PDFs (DANFSe v2.0 / NFS-e). O programa extrai CNPJ, "
             "razão social, endereço, município, UF, CEP, IM, data e valor.\n"
             "As notas fora do período da ECD são sinalizadas."),
            ("2.", "Despesas manuais",
             "Cadastre gastos do CNPJ com data, valor, histórico e conta "
             "referencial do P150A."),
            ("3.", "Ano dinâmico",
             "Gera ECD para qualquer ano-calendário — inclusive em atraso."),
            ("4.", "Backup da ECD anterior",
             "Importe o .txt da ECD do ano anterior para reaproveitar saldos."),
            ("5.", "Geração e validação com notas explicativas",
             "Ao validar, exibe o resumo do balanço e as notas explicativas, "
             "fatos contábeis e lucros acumulados gerados."),
            ("6.", "Exportação pronta para o PVA",
             "Arquivo em ISO-8859-1, CRLF e sem BOM."),
        ]
        for num, titulo, desc in funcs:
            linha = tk.Frame(body, bg='#f4f6fb')
            linha.pack(fill='x', pady=3)
            tk.Label(linha, text=num, bg='#f4f6fb', fg='#1a3c6e',
                     font=('Segoe UI', 11, 'bold'), width=3,
                     anchor='nw').pack(side='left', anchor='n')
            bloco = tk.Frame(linha, bg='#f4f6fb')
            bloco.pack(side='left', fill='x', expand=True)
            tk.Label(bloco, text=titulo, bg='#f4f6fb', fg='#222',
                     font=('Segoe UI', 10, 'bold'),
                     anchor='w').pack(anchor='w')
            tk.Label(bloco, text=desc, bg='#f4f6fb', fg='#555',
                     font=('Segoe UI', 9), anchor='w',
                     wraplength=680, justify='left').pack(anchor='w')

        aviso = tk.Frame(self, bg='#fff7e0', bd=1, relief='solid')
        aviso.pack(fill='x', padx=30, pady=(0, 15))
        tk.Label(aviso,
                 text="⚠  Para importar PDFs é necessário ter a biblioteca 'pypdf' instalada.\n"
                      "    Se ainda não instalou, execute no terminal:   pip install pypdf",
                 bg='#fff7e0', fg='#7a5a00',
                 font=('Segoe UI', 9), justify='left').pack(padx=12, pady=8, anchor='w')

# ================================================================
# APLICAÇÃO PRINCIPAL
# ================================================================
class AppSpedECD(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg='#f4f6fb')
        self.pack(fill='both', expand=True)
        self.root = root
        self.empresa = None
        self.contador = None
        self.representante = None
        self.notas = []
        self.ecd_anterior = None
        self.linhas_geradas = []
        self.despesas_manuais = []
        self._montar_ui()

    def _montar_ui(self):
        menubar = tk.Menu(self.root)
        m_arq = tk.Menu(menubar, tearoff=0)
        m_arq.add_command(label="Salvar como...", command=self._salvar_como)
        m_arq.add_separator()
        m_arq.add_command(label="Sair", command=self.root.destroy)
        menubar.add_cascade(label="Arquivo", menu=m_arq)
        m_ajuda = tk.Menu(menubar, tearoff=0)
        m_ajuda.add_command(label="Sobre",
            command=lambda: messagebox.showinfo("Sobre",
                "Gerador SPED ECD — v2.9\nLeiaute 9.00 / Lucro Presumido\n\n"
                "Suporta DANFSe v2.0 e qualquer ano-calendário."))
        menubar.add_cascade(label="Ajuda", menu=m_ajuda)
        self.root.config(menu=menubar)

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill='both', expand=True, padx=8, pady=8)

        self.aba_cad = ttk.Frame(self.nb);  self.nb.add(self.aba_cad,  text='  1. Cadastro  ')
        self.aba_notas = ttk.Frame(self.nb);self.nb.add(self.aba_notas,text='  2. Notas PDF  ')
        self.aba_desp = ttk.Frame(self.nb); self.nb.add(self.aba_desp, text='  3. Despesas Manuais  ')
        self.aba_ant = ttk.Frame(self.nb);  self.nb.add(self.aba_ant,  text='  4. ECD Anterior  ')
        self.aba_ger = ttk.Frame(self.nb);  self.nb.add(self.aba_ger,  text='  5. Gerar & Validar  ')
        self.aba_log = ttk.Frame(self.nb);  self.nb.add(self.aba_log,  text='  6. Log  ')

        self._montar_cadastro()
        self._montar_notas()
        self._montar_despesas()
        self._montar_anterior()
        self._montar_gerar()
        self._montar_log()

    def _montar_cadastro(self):
        f = self.aba_cad
        container = ttk.Frame(f); container.pack(fill='both', expand=True)
        canvas = tk.Canvas(container, bg='#f4f6fb', highlightthickness=0)
        vbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)
        vbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        wrap = ttk.Frame(canvas)
        win_id = canvas.create_window((0, 0), window=wrap, anchor='nw')
        wrap.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(win_id, width=e.width))
        def _mw(event): canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        canvas.bind('<Enter>', lambda e: canvas.bind_all('<MouseWheel>', _mw))
        canvas.bind('<Leave>', lambda e: canvas.unbind_all('<MouseWheel>'))

        ttk.Label(wrap, text="Cadastro do Contribuinte",
                  font=('Segoe UI', 12, 'bold')).grid(
                  row=0, column=0, columnspan=4, sticky='w', padx=14, pady=(10, 6))
        self.emp = {}
        campos_emp = [
            ('nome',      'Razão Social',            'w', 60),
            ('cnpj',      'CNPJ (só números)',       'w', 20),
            ('uf',        'UF',                      'w',  4),
            ('ie',        'Inscrição Estadual',      'w', 20),
            ('cod_mun',   'Código IBGE Município',   'w', 12),
            ('municipio', 'Município',               'w', 30),
            ('nire',      'NIRE',                    'w', 20),
            ('im',        'Inscrição Municipal',     'w', 20),
            ('dt_ini',    'Data Inicial (DDMMAAAA)', 'w', 12),
            ('dt_fin',    'Data Final (DDMMAAAA)',   'w', 12),
            ('dt_arq',    'Data do Arquivo',         'w', 12),
            ('dt_ex_social', 'Data Ex. Social',      'w', 12),
        ]
        r = 1
        for k, lbl, _, w in campos_emp:
            ttk.Label(wrap, text=lbl + ':').grid(row=r, column=0, sticky='e', padx=4, pady=2)
            v = tk.StringVar()
            ttk.Entry(wrap, textvariable=v, width=w).grid(
                row=r, column=1, columnspan=3, sticky='w', padx=4, pady=2)
            self.emp[k] = v
            r += 1

        ttk.Label(wrap,
                  text="ℹ  O período (data inicial e final) define o ano-calendário da ECD.\n"
                       "    Ex.: 01/01/2023 a 31/12/2023 gera a ECD de 2023 (declaração em atraso).",
                  foreground='#1a3c6e',
                  font=('Segoe UI', 9, 'italic'),
                  justify='left').grid(row=r, column=0, columnspan=4, sticky='w',
                                       padx=14, pady=(6, 4))
        r += 1

        ttk.Separator(wrap, orient='horizontal').grid(
            row=r, column=0, columnspan=4, sticky='ew', pady=10); r += 1
        ttk.Label(wrap, text="Contador  (nome e CPF são obrigatórios)",
                  font=('Segoe UI', 12, 'bold')).grid(
                  row=r, column=0, columnspan=4, sticky='w', pady=(0, 6)); r += 1
        self.cont = {}
        for k, lbl in [
            ('nome','Nome'),('cpf','CPF (só números)'),('crc','CRC'),
            ('email','E-mail'),('fone','Telefone'),
            ('uf_crc','UF CRC'),('num_seq_crc','Nº Sequencial CRC'),
            ('dt_crc','Data CRC'),
        ]:
            ttk.Label(wrap, text=lbl + ':').grid(row=r, column=0, sticky='e', padx=4, pady=2)
            v = tk.StringVar()
            ttk.Entry(wrap, textvariable=v, width=40).grid(
                row=r, column=1, columnspan=3, sticky='w', padx=4, pady=2)
            self.cont[k] = v
            r += 1

        ttk.Separator(wrap, orient='horizontal').grid(
            row=r, column=0, columnspan=4, sticky='ew', pady=10); r += 1
        ttk.Label(wrap, text="Representante Legal",
                  font=('Segoe UI', 12, 'bold')).grid(
                  row=r, column=0, columnspan=4, sticky='w', pady=(0, 6)); r += 1
        self.rep = {}
        for k, lbl in [('nome','Nome'),('cnpj','CNPJ (só números)'),
                       ('email','E-mail'),('fone','Telefone')]:
            ttk.Label(wrap, text=lbl + ':').grid(row=r, column=0, sticky='e', padx=4, pady=2)
            v = tk.StringVar()
            ttk.Entry(wrap, textvariable=v, width=40).grid(
                row=r, column=1, columnspan=3, sticky='w', padx=4, pady=2)
            self.rep[k] = v
            r += 1

        ttk.Separator(wrap, orient='horizontal').grid(
            row=r, column=0, columnspan=4, sticky='ew', pady=10); r += 1
        bar = ttk.Frame(wrap); bar.grid(row=r, column=0, columnspan=4, sticky='w', pady=4, padx=4)
        ttk.Button(bar, text="Carregar cadastro (JSON)...",
                   command=self._carregar_cadastro).pack(side='left')
        ttk.Button(bar, text="Salvar cadastro (JSON)...",
                   command=self._salvar_cadastro).pack(side='left', padx=6)
        ttk.Button(bar, text="Confirmar cadastro",
                   command=self._confirmar_cadastro).pack(side='left', padx=6)
        ttk.Button(bar, text="Limpar cadastro",
                   command=self._limpar_cadastro).pack(side='left', padx=6)

        self.lbl_cad = ttk.Label(wrap, text="Cadastro ainda não confirmado.",
                                  foreground='#a00')
        self.lbl_cad.grid(row=r+1, column=0, columnspan=4, sticky='w', padx=14, pady=(6, 20))

    def _montar_notas(self):
        f = self.aba_notas
        ttk.Label(f, text="Importação de Notas Fiscais (PDF)",
                  font=('Segoe UI', 12, 'bold')).pack(anchor='w', padx=10, pady=(10, 4))
        ttk.Label(f, text="Selecione um ou mais PDFs (DANFSe v2.0 / NFS-e). O programa extrai "
                          "os dados e VALIDA se a data da nota está dentro do período da ECD.\n"
                          "Notas fora do período serão sinalizadas para sua decisão.",
                  foreground='#555', wraplength=900, justify='left').pack(anchor='w', padx=10, pady=(0, 8))

        bar = ttk.Frame(f); bar.pack(fill='x', padx=10, pady=4)
        ttk.Button(bar, text="Adicionar PDFs...", command=self._add_pdfs).pack(side='left')
        ttk.Button(bar, text="Remover selecionado", command=self._remover_pdf).pack(side='left', padx=6)
        ttk.Button(bar, text="Limpar lista", command=self._limpar_pdfs).pack(side='left')
        ttk.Button(bar, text="Ver dados extraídos", command=self._ver_detalhes_nota).pack(side='left', padx=6)

        cols = ('arquivo','cnpj','razao','data','valor','periodo')
        self.tv_notas = ttk.Treeview(f, columns=cols, show='headings', height=12)
        for c,t,w in [('arquivo','Arquivo',200),('cnpj','CNPJ',150),
                      ('razao','Razão Social',180),
                      ('data','Data',90),('valor','Valor',100),
                      ('periodo','Período',110)]:
            self.tv_notas.heading(c, text=t)
            self.tv_notas.column(c, width=w, anchor='w' if c in ('arquivo','razao') else 'center')
        self.tv_notas.tag_configure('fora', background='#ffe6e6')
        self.tv_notas.pack(fill='both', expand=True, padx=10, pady=6)
        self.lbl_notas_info = ttk.Label(f, text="Nenhuma nota importada.", foreground='#888')
        self.lbl_notas_info.pack(anchor='w', padx=10, pady=(0,10))

    def _montar_despesas(self):
        f = self.aba_desp
        ttk.Label(f, text="Cadastro Manual de Despesas do CNPJ",
                  font=('Segoe UI', 12, 'bold')).pack(anchor='w', padx=10, pady=(10, 4))
        ttk.Label(f, text="Adicione gastos da empresa informando data, valor, histórico e "
                          "conta referencial do P150A.\nAs datas também são validadas contra "
                          "o período da ECD.",
                  foreground='#555', justify='left', wraplength=900).pack(anchor='w', padx=10, pady=(0, 10))

        form = ttk.LabelFrame(f, text="Nova Despesa"); form.pack(fill='x', padx=10, pady=6)
        l1 = ttk.Frame(form); l1.pack(fill='x', padx=10, pady=4)
        ttk.Label(l1, text="Data (DDMMAAAA):").pack(side='left')
        self.desp_data = tk.StringVar()
        ttk.Entry(l1, textvariable=self.desp_data, width=12).pack(side='left', padx=4)
        ttk.Label(l1, text="Valor (R$):").pack(side='left', padx=(16, 0))
        self.desp_valor = tk.StringVar()
        ttk.Entry(l1, textvariable=self.desp_valor, width=14).pack(side='left', padx=4)
        ttk.Label(l1, text="Histórico:").pack(side='left', padx=(16, 0))
        self.desp_hist = tk.StringVar()
        ttk.Entry(l1, textvariable=self.desp_hist, width=40).pack(side='left', padx=4)
        l2 = ttk.Frame(form); l2.pack(fill='x', padx=10, pady=4)
        ttk.Label(l2, text="Conta Referencial (P150A):").pack(side='left')
        self.desp_conta = tk.StringVar()
        combo = ttk.Combobox(l2, textvariable=self.desp_conta, width=95, state='readonly')
        combo['values'] = [f"{cod}  —  {desc}" for cod, desc in CONTAS_DESPESA_REF]
        combo.pack(side='left', padx=4)
        l3 = ttk.Frame(form); l3.pack(fill='x', padx=10, pady=6)
        ttk.Button(l3, text="Adicionar Despesa", command=self._add_despesa).pack(side='left')
        ttk.Button(l3, text="Limpar Formulário", command=self._limpar_form_despesa).pack(side='left', padx=6)

        ttk.Label(f, text="Despesas cadastradas:").pack(anchor='w', padx=10, pady=(10,0))
        cols = ('data','valor','historico','conta')
        self.tv_desp = ttk.Treeview(f, columns=cols, show='headings', height=12)
        for c,t,w in [('data','Data',100),('valor','Valor',110),
                      ('historico','Histórico',300),('conta','Conta Referencial',260)]:
            self.tv_desp.heading(c, text=t)
            self.tv_desp.column(c, width=w, anchor='w' if c in ('historico','conta') else 'center')
        self.tv_desp.pack(fill='both', expand=True, padx=10, pady=6)
        bar2 = ttk.Frame(f); bar2.pack(fill='x', padx=10, pady=4)
        ttk.Button(bar2, text="Remover selecionada", command=self._remover_despesa).pack(side='left')
        ttk.Button(bar2, text="Limpar lista", command=self._limpar_despesas).pack(side='left', padx=6)
        self.lbl_desp_info = ttk.Label(f, text="Nenhuma despesa cadastrada.", foreground='#888')
        self.lbl_desp_info.pack(anchor='w', padx=10, pady=(0,10))

    def _montar_anterior(self):
        f = self.aba_ant
        ttk.Label(f, text="Backup da ECD do Ano Anterior",
                  font=('Segoe UI', 12, 'bold')).pack(anchor='w', padx=10, pady=(10, 4))
        ttk.Label(f, text="Se esta NÃO for a primeira entrega, importe o .txt da ECD "
                          "transmitida no ano anterior.",
                  foreground='#555', justify='left').pack(anchor='w', padx=10, pady=(0, 10))
        self.var_usar_anterior = tk.BooleanVar(value=False)
        ttk.Checkbutton(f, text="Usar backup da ECD do ano anterior",
                        variable=self.var_usar_anterior,
                        command=self._toggle_anterior).pack(anchor='w', padx=10, pady=4)
        bar = ttk.Frame(f); bar.pack(fill='x', padx=10, pady=6)
        self.btn_sel_anterior = ttk.Button(bar, text="Selecionar arquivo .txt...",
                                            command=self._selecionar_anterior, state='disabled')
        self.btn_sel_anterior.pack(side='left')
        self.lbl_anterior = ttk.Label(f, text="Nenhum backup selecionado.", foreground='#888')
        self.lbl_anterior.pack(anchor='w', padx=10, pady=4)
        self.txt_anterior = scrolledtext.ScrolledText(f, height=16, font=('Consolas', 9))
        self.txt_anterior.pack(fill='both', expand=True, padx=10, pady=6)
        self.txt_anterior.insert('1.0', "Aguardando seleção do backup...")
        self.txt_anterior.config(state='disabled')

    def _montar_gerar(self):
        f = self.aba_ger
        ttk.Label(f, text="Geração e Validação do Arquivo SPED ECD",
                  font=('Segoe UI', 12, 'bold')).pack(anchor='w', padx=10, pady=(10,4))
        ttk.Label(f, text="Antes de gerar, confirme o cadastro na aba '1. Cadastro'.",
                  foreground='#555').pack(anchor='w', padx=10, pady=(0,8))
        bar = ttk.Frame(f); bar.pack(fill='x', padx=10, pady=6)
        ttk.Button(bar, text="Gerar Arquivo SPED ECD", command=self._gerar_arquivo).pack(side='left')
        ttk.Button(bar, text="Validar", command=self._validar_arquivo).pack(side='left', padx=6)
        ttk.Button(bar, text="Salvar Como...", command=self._salvar_como).pack(side='left', padx=6)
        self.lbl_gerar_status = ttk.Label(f, text="Aguardando geração...",
                                           font=('Segoe UI', 10))
        self.lbl_gerar_status.pack(anchor='w', padx=10, pady=6)
        ttk.Label(f, text="Pré-visualização:").pack(anchor='w', padx=10, pady=(8,0))
        self.txt_preview = scrolledtext.ScrolledText(f, height=20, font=('Consolas', 8))
        self.txt_preview.pack(fill='both', expand=True, padx=10, pady=6)

    def _montar_log(self):
        f = self.aba_log
        ttk.Label(f, text="Log de Operações", font=('Segoe UI', 12, 'bold')).pack(anchor='w', padx=10, pady=(10,4))
        self.txt_log = scrolledtext.ScrolledText(f, font=('Consolas', 9))
        self.txt_log.pack(fill='both', expand=True, padx=10, pady=10)

    # ── CADASTRO ─────────────────────────────────────────────────
    def _carregar_cadastro(self):
        arq = filedialog.askopenfilename(title="Carregar cadastro",
            filetypes=[("JSON", "*.json"), ("Todos", "*.*")])
        if not arq: return
        try:
            with open(arq, 'r', encoding='utf-8') as f:
                d = json.load(f)
            for k, v in d.get('empresa', {}).items():
                if k in self.emp: self.emp[k].set(v)
            for k, v in d.get('contador', {}).items():
                if k in self.cont: self.cont[k].set(v)
            for k, v in d.get('representante', {}).items():
                if k in self.rep: self.rep[k].set(v)
            self._log(f"[CADASTRO] Carregado de {arq}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _salvar_cadastro(self):
        arq = filedialog.asksaveasfilename(title="Salvar cadastro",
            defaultextension=".json", initialfile="cadastro_ecd.json",
            filetypes=[("JSON", "*.json")])
        if not arq: return
        try:
            d = {'empresa': {k: v.get() for k, v in self.emp.items()},
                 'contador': {k: v.get() for k, v in self.cont.items()},
                 'representante': {k: v.get() for k, v in self.rep.items()}}
            with open(arq, 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            self._log(f"[CADASTRO] Salvo em {arq}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _limpar_cadastro(self):
        for v in self.emp.values(): v.set('')
        for v in self.cont.values(): v.set('')
        for v in self.rep.values(): v.set('')
        self.empresa = None; self.contador = None; self.representante = None
        self.lbl_cad.config(text="Cadastro ainda não confirmado.", foreground='#a00')
        self._log("[CADASTRO] Campos limpos.")

    def _confirmar_cadastro(self):
        e = {k: v.get().strip() for k, v in self.emp.items()}
        c = {k: v.get().strip() for k, v in self.cont.items()}
        rp = {k: v.get().strip() for k, v in self.rep.items()}
        if not e['nome'] or not e['cnpj']:
            messagebox.showwarning("Cadastro incompleto",
                "Preencha pelo menos Razão Social e CNPJ do contribuinte."); return
        if not _cnpj_ok(e['cnpj']):
            messagebox.showerror("CNPJ inválido", f"O CNPJ '{e['cnpj']}' não é válido."); return
        if not _data_ok(e['dt_ini']):
            messagebox.showerror("Data inicial inválida",
                "Informe a data inicial no formato DDMMAAAA (ex.: 01012023)."); return
        if not _data_ok(e['dt_fin']):
            messagebox.showerror("Data final inválida",
                "Informe a data final no formato DDMMAAAA (ex.: 31122023)."); return
        if e['dt_ini'] > e['dt_fin']:
            messagebox.showerror("Período inválido",
                "A data inicial não pode ser posterior à data final."); return
        if not c['nome'] or not c['cpf']:
            messagebox.showerror("Contador incompleto",
                "O nome e o CPF do contador são obrigatórios para o "
                "registro J930.\n\nPreencha esses campos."); return
        if not _cpf_ok(c['cpf']):
            messagebox.showerror("CPF inválido",
                f"O CPF do contador '{c['cpf']}' não é válido."); return
        if rp['cnpj'] and not _cnpj_ok(rp['cnpj']):
            messagebox.showerror("CNPJ inválido",
                f"O CNPJ do representante '{rp['cnpj']}' não é válido."); return

        e.setdefault('uf', 'MG')
        if not e['dt_arq']: e['dt_arq'] = e['dt_fin']
        if not e['dt_ex_social']: e['dt_ex_social'] = e['dt_fin']
        self.empresa = e; self.contador = c; self.representante = rp
        ano = e['dt_fin'][4:8]
        self.lbl_cad.config(text=f"✅ Cadastro confirmado — Ano-calendário {ano}.",
                             foreground='#0a0')
        self._log(f"[CADASTRO] Confirmado: {e['nome']} | CNPJ {e['cnpj']} | "
                  f"Período {_fmt_data(e['dt_ini'])} a {_fmt_data(e['dt_fin'])} (ano {ano})")
        messagebox.showinfo("Cadastro",
            f"Cadastro confirmado com sucesso!\n\n"
            f"Ano-calendário da ECD: {ano}\n"
            f"Período: {_fmt_data(e['dt_ini'])} a {_fmt_data(e['dt_fin'])}")

    # ── NOTAS PDF ────────────────────────────────────────────────
    def _add_pdfs(self):
        if not PDF_OK:
            messagebox.showerror("Biblioteca ausente",
                "A biblioteca 'pypdf' não está instalada.\n\n"
                "Execute no terminal:\n    pip install pypdf"); return
        arquivos = filedialog.askopenfilenames(title="Selecione os PDFs",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos", "*.*")])
        if not arquivos: return

        dt_ini = self.emp['dt_ini'].get().strip()
        dt_fin = self.emp['dt_fin'].get().strip()
        periodo_definido = _data_ok(dt_ini) and _data_ok(dt_fin)
        if not periodo_definido:
            resp = messagebox.askyesno("Período não definido",
                "O período da ECD ainda não foi preenchido.\n\n"
                "Sem o período, o programa NÃO poderá validar se as notas estão "
                "dentro do ano-calendário.\n\nDeseja continuar mesmo assim?")
            if not resp:
                self.nb.select(0); return

        preencheu_cadastro = False
        notas_ignoradas = 0
        notas_fora = 0
        for arq in arquivos:
            try:
                d = extrair_dados_pdf(arq)
                fora = False; motivo = ""
                if periodo_definido and d['data']:
                    dentro, motivo = _nota_no_periodo(d['data'], dt_ini, dt_fin)
                    if not dentro:
                        fora = True; notas_fora += 1
                        resp = messagebox.askyesno("⚠ Nota fora do período",
                            f"O arquivo:\n  {d['arquivo']}\n\n"
                            f"tem data {_fmt_data(d['data'])}, que está FORA do período da ECD.\n\n"
                            f"Período configurado:\n  {_fmt_data(dt_ini)} a {_fmt_data(dt_fin)}\n\n"
                            f"Motivo: {motivo}.\n\n"
                            f"Deseja INCLUIR esta nota mesmo assim?")
                        if not resp:
                            self._log(f"[PDF] IGNORADO: {d['arquivo']} — fora do período ({motivo})")
                            notas_ignoradas += 1; continue
                self.notas.append(d)
                tag = 'fora' if fora else ''
                self.tv_notas.insert('', 'end', values=(
                    d['arquivo'], d['cnpj'] or '—',
                    (d['razao_social'] or '—')[:30],
                    _fmt_data(d['data']) if d['data'] else '—',
                    d['valor'] or '—',
                    '⚠ FORA' if fora else 'OK'), tags=(tag,))
                self._log(f"[PDF] {d['arquivo']} → CNPJ={d['cnpj']} "
                          f"Razão={d['razao_social']} Data={d['data']} Valor={d['valor']} "
                          f"{'[FORA DO PERÍODO]' if fora else ''}")
                if not preencheu_cadastro and not self.empresa:
                    if self._preencher_cadastro_da_nota(d):
                        preencheu_cadastro = True
            except Exception as e:
                self._log(f"[ERRO PDF] {arq}: {e}")
                messagebox.showwarning("Erro ao ler PDF", f"{os.path.basename(arq)}\n\n{e}")

        info = f"{len(self.notas)} nota(s) importada(s)."
        if notas_ignoradas: info += f"  Ignorada(s): {notas_ignoradas}."
        if notas_fora: info += f"  ⚠ Fora do período: {notas_fora}."
        self.lbl_notas_info.config(text=info)

        if preencheu_cadastro:
            self._log("[CADASTRO] Preenchido automaticamente a partir da nota fiscal.")
            self.nb.select(0)
            messagebox.showinfo("Cadastro preenchido",
                "Os dados do contribuinte foram preenchidos automaticamente.\n\n"
                "Confira os campos na aba '1. Cadastro' e clique em 'Confirmar cadastro'.\n\n"
                "⚠  Lembre-se de preencher o CONTADOR (nome e CPF).")

    def _preencher_cadastro_da_nota(self, dados):
        def set_se_vazio(var, valor):
            if valor and not var.get().strip():
                var.set(valor); return True
            return False
        preenchidos = 0
        if set_se_vazio(self.emp['nome'], dados.get('razao_social')): preenchidos += 1
        if set_se_vazio(self.emp['cnpj'], dados.get('cnpj')): preenchidos += 1
        if set_se_vazio(self.emp['ie'],   dados.get('ie')): preenchidos += 1
        if set_se_vazio(self.emp['municipio'], dados.get('municipio')): preenchidos += 1
        if set_se_vazio(self.emp['uf'], dados.get('uf')): preenchidos += 1
        if set_se_vazio(self.emp['im'], dados.get('im')): preenchidos += 1
        if dados.get('cnpj') and not self.rep['cnpj'].get().strip():
            self.rep['cnpj'].set(dados['cnpj'])
        if dados.get('razao_social') and not self.rep['nome'].get().strip():
            self.rep['nome'].set(dados['razao_social'])
        if dados.get('data') and len(dados['data']) == 8:
            if not self.emp['dt_ini'].get().strip():
                self.emp['dt_ini'].set('01' + '01' + dados['data'][4:])
            if not self.emp['dt_fin'].get().strip():
                self.emp['dt_fin'].set('31' + '12' + dados['data'][4:])
        return preenchidos >= 2

    def _remover_pdf(self):
        for item in self.tv_notas.selection():
            idx = self.tv_notas.index(item)
            self.tv_notas.delete(item)
            if idx < len(self.notas): self.notas.pop(idx)
        self.lbl_notas_info.config(text=f"{len(self.notas)} nota(s) importada(s).")

    def _limpar_pdfs(self):
        self.notas.clear()
        for it in self.tv_notas.get_children(): self.tv_notas.delete(it)
        self.lbl_notas_info.config(text="Nenhuma nota importada.")

    def _ver_detalhes_nota(self):
        sel = self.tv_notas.selection()
        if not sel:
            messagebox.showinfo("Detalhes", "Selecione uma nota na lista."); return
        idx = self.tv_notas.index(sel[0])
        if idx >= len(self.notas): return
        d = self.notas[idx]
        win = tk.Toplevel(self.root); win.title(f"Detalhes — {d['arquivo']}")
        win.geometry("720x600")
        txt = scrolledtext.ScrolledText(win, font=('Consolas', 10))
        txt.pack(fill='both', expand=True, padx=8, pady=8)
        txt.insert('end', f"Arquivo         : {d['arquivo']}\n")
        txt.insert('end', f"CNPJ            : {d.get('cnpj')}\n")
        txt.insert('end', f"Razão Social    : {d.get('razao_social')}\n")
        txt.insert('end', f"Endereço        : {d.get('endereco')}\n")
        txt.insert('end', f"Município       : {d.get('municipio')}\n")
        txt.insert('end', f"UF              : {d.get('uf')}\n")
        txt.insert('end', f"CEP             : {d.get('cep')}\n")
        txt.insert('end', f"Inscr. Estadual : {d.get('ie')}\n")
        txt.insert('end', f"Inscr. Municipal: {d.get('im')}\n")
        txt.insert('end', f"Data            : {d.get('data')}\n")
        txt.insert('end', f"Valor           : {d.get('valor')}\n\n")
        txt.insert('end', "── Emitente ──\n")
        for k, v in (d.get('emitente') or {}).items():
            txt.insert('end', f"  {k}: {v}\n")
        txt.insert('end', "\n── Destinatário ──\n")
        for k, v in (d.get('destinatario') or {}).items():
            txt.insert('end', f"  {k}: {v}\n")
        txt.insert('end', "\n── Texto completo do PDF ──\n")
        txt.insert('end', d.get('texto_completo', ''))
        txt.config(state='disabled')

    # ── DESPESAS MANUAIS ─────────────────────────────────────────
    def _add_despesa(self):
        data = self.desp_data.get().strip()
        valor = self.desp_valor.get().strip().replace('.', '').replace(',', '.')
        hist = self.desp_hist.get().strip()
        conta_str = self.desp_conta.get().strip()
        if not _data_ok(data):
            messagebox.showwarning("Data inválida",
                "Informe a data no formato DDMMAAAA (ex.: 15032023)."); return
        try:
            valor_f = float(valor)
            if valor_f <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Valor inválido",
                "Informe um valor numérico maior que zero (ex.: 1500,00)."); return
        if not hist:
            messagebox.showwarning("Histórico obrigatório",
                "Informe o histórico da despesa."); return
        if not conta_str:
            messagebox.showwarning("Conta referencial",
                "Selecione a conta referencial da despesa."); return
        dt_ini = self.emp['dt_ini'].get().strip()
        dt_fin = self.emp['dt_fin'].get().strip()
        if _data_ok(dt_ini) and _data_ok(dt_fin):
            dentro, motivo = _nota_no_periodo(data, dt_ini, dt_fin)
            if not dentro:
                resp = messagebox.askyesno("⚠ Despesa fora do período",
                    f"A data {_fmt_data(data)} está FORA do período da ECD.\n\n"
                    f"Período: {_fmt_data(dt_ini)} a {_fmt_data(dt_fin)}\n"
                    f"Motivo: {motivo}.\n\nDeseja incluir mesmo assim?")
                if not resp: return
        cod_conta = conta_str.split()[0]
        valor_fmt = f"{valor_f:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        desp = {'data': data, 'valor': valor_f, 'valor_fmt': valor_fmt,
                'historico': hist, 'conta_ref': cod_conta}
        self.despesas_manuais.append(desp)
        self.tv_desp.insert('', 'end', values=(
            _fmt_data(data), f"R$ {valor_fmt}", hist, cod_conta))
        self._limpar_form_despesa()
        self.lbl_desp_info.config(text=f"{len(self.despesas_manuais)} despesa(s) cadastrada(s).")
        self._log(f"[DESPESA] {data} | R$ {valor_fmt} | {hist} | {cod_conta}")

    def _limpar_form_despesa(self):
        self.desp_data.set(''); self.desp_valor.set('')
        self.desp_hist.set(''); self.desp_conta.set('')

    def _remover_despesa(self):
        for item in self.tv_desp.selection():
            idx = self.tv_desp.index(item)
            self.tv_desp.delete(item)
            if idx < len(self.despesas_manuais):
                self.despesas_manuais.pop(idx)
        self.lbl_desp_info.config(text=f"{len(self.despesas_manuais)} despesa(s) cadastrada(s).")

    def _limpar_despesas(self):
        self.despesas_manuais.clear()
        for it in self.tv_desp.get_children(): self.tv_desp.delete(it)
        self.lbl_desp_info.config(text="Nenhuma despesa cadastrada.")

    # ── ECD ANTERIOR ─────────────────────────────────────────────
    def _toggle_anterior(self):
        estado = 'normal' if self.var_usar_anterior.get() else 'disabled'
        self.btn_sel_anterior.config(state=estado)
        if not self.var_usar_anterior.get():
            self.ecd_anterior = None
            self.lbl_anterior.config(text="Nenhum backup selecionado.", foreground='#888')
            self.txt_anterior.config(state='normal')
            self.txt_anterior.delete('1.0', 'end')
            self.txt_anterior.insert('1.0', "Aguardando seleção do backup...")
            self.txt_anterior.config(state='disabled')

    def _selecionar_anterior(self):
        arq = filedialog.askopenfilename(title="ECD do ano anterior",
            filetypes=[("Arquivos TXT", "*.txt"), ("Todos", "*.*")])
        if not arq: return
        try:
            self.ecd_anterior = ler_ecd_anterior(arq)
            info = self.ecd_anterior
            self.lbl_anterior.config(text=f"Backup: {os.path.basename(arq)}", foreground='#0a0')
            self.txt_anterior.config(state='normal')
            self.txt_anterior.delete('1.0', 'end')
            self.txt_anterior.insert('1.0',
                f"Arquivo: {os.path.basename(arq)}\n"
                f"CNPJ: {info['cnpj']}\n"
                f"Empresa: {info['nome']}\n"
                f"Período: {info['dt_ini']} a {info['dt_fin']}\n\n"
                f"Saldos finais ({len(info['saldos_finais'])} contas):\n")
            for cod, (vl, ind) in sorted(info['saldos_finais'].items()):
                self.txt_anterior.insert('end', f"  {cod}  →  {vl:,.2f} {ind}\n")
            self.txt_anterior.config(state='disabled')
            self._log(f"[ECD ANTERIOR] {arq} | {len(info['saldos_finais'])} contas")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ── GERAR / VALIDAR / SALVAR ─────────────────────────────────
    def _gerar_arquivo(self):
        if not self.empresa:
            messagebox.showwarning("Cadastro",
                "Confirme o cadastro na aba '1. Cadastro' antes de gerar.")
            self.nb.select(0); return
        faltas = []
        if not self.empresa.get('nome'):  faltas.append("Razão social")
        if not self.empresa.get('cnpj'):  faltas.append("CNPJ")
        if not self.contador.get('nome'): faltas.append("Nome do contador")
        if not self.contador.get('cpf'):  faltas.append("CPF do contador")
        if faltas:
            messagebox.showerror("Dados incompletos",
                "Preencha antes de gerar:\n\n• " + "\n• ".join(faltas))
            self.nb.select(0); return
        try:
            ano = self.empresa['dt_fin'][4:8]
            self._log(f"[GERAR] Iniciando geração para o ano-calendário {ano}...")
            self._log(f"[GERAR] Período: {_fmt_data(self.empresa['dt_ini'])} a "
                      f"{_fmt_data(self.empresa['dt_fin'])}")
            self._log(f"[GERAR] {len(self.despesas_manuais)} despesa(s) manual(is).")
            sped = SpedECD(
                empresa=self.empresa, contador=self.contador,
                representante=self.representante, notas=self.notas,
                ecd_anterior=self.ecd_anterior,
                despesas_manuais=self.despesas_manuais)
            self.linhas_geradas = sped.gerar()
            n_i051 = sum(1 for l in self.linhas_geradas if l.startswith('|I051|'))
            n_i052 = sum(1 for l in self.linhas_geradas if l.startswith('|I052|'))
            n_i200 = sum(1 for l in self.linhas_geradas if l.startswith('|I200|'))
            self._log(f"[GERAR] {len(self.linhas_geradas)} linhas | "
                      f"I051={n_i051} | I052={n_i052} | I200={n_i200}")
            self.txt_preview.delete('1.0', 'end')
            for l in self.linhas_geradas[:400]:
                self.txt_preview.insert('end', l + '\n')
            if len(self.linhas_geradas) > 400:
                self.txt_preview.insert('end',
                    f"\n... ({len(self.linhas_geradas)-400} linhas restantes)\n")
            self.lbl_gerar_status.config(
                text=f"Arquivo {ano} gerado: {len(self.linhas_geradas)} linhas — pronto para validar.",
                foreground='#0a0')
        except Exception as e:
            self._log(f"[ERRO GERAR] {e}\n{traceback.format_exc()}")
            messagebox.showerror("Erro", str(e))

    def _extrair_notas_explicativas(self):
        """
        Extrai os textos das notas explicativas e fatos contábeis
        dos registros J210, J215 e J800 do arquivo gerado.
        """
        j210, j215, j800 = [], [], []

        for l in self.linhas_geradas:
            p = split_sped(l)
            if not p: continue
            reg = p[0]

            # J210 — Lucros Acumulados / Prejuízos Acumulados
            if reg == 'J210' and len(p) >= 8:
                j210.append(
                    f"  • {p[3]}\n"
                    f"      Saldo inicial : R$ {p[4]:>14} ({p[5]})\n"
                    f"      Saldo final   : R$ {p[6]:>14} ({p[7]})"
                )

            # J215 — Fatos Contábeis Relevantes
            elif reg == 'J215' and len(p) >= 5:
                j215.append(
                    f"  • {p[2]}\n"
                    f"      Valor: R$ {p[3]} ({p[4]})"
                )

            # J800 — Notas Explicativas
            elif reg == 'J800' and len(p) >= 3:
                texto = p[2]
                extras = [x for x in p[3:] if x and x != 'J800FIM']
                if extras:
                    texto += " " + " ".join(extras)
                j800.append(f"  • {texto}")

        partes = []
        partes.append("── J210 — Lucros Acumulados ──")
        partes.extend(j210 if j210 else ["  (nenhum registro)"])
        partes.append("")
        partes.append("── J215 — Fatos Contábeis Relevantes ──")
        partes.extend(j215 if j215 else ["  (nenhum registro)"])
        partes.append("")
        partes.append("── J800 — Notas Explicativas ──")
        partes.extend(j800 if j800 else ["  (nenhum registro)"])

        return "\n".join(partes)

    def _validar_arquivo(self):
        if not self.linhas_geradas:
            messagebox.showwarning("Nada para validar", "Gere o arquivo primeiro.")
            return

        erros, avisos, info = validar(self.linhas_geradas)
        self._log(f"[VALIDAR] {len(erros)} erro(s), {len(avisos)} aviso(s).")
        for e in erros: self._log(f"  [ERRO] {e}")
        for a in avisos: self._log(f"  [AVISO] {a}")
        for i in info: self._log(f"  [INFO] {i}")

        # ── CASO 1: REPROVADO — mostra lista de erros ──────────
        if erros:
            self.lbl_gerar_status.config(
                text=f"❌ {len(erros)} erro(s) — corrija antes de importar.",
                foreground='#c00')
            messagebox.showerror("Validação",
                f"{len(erros)} erro(s):\n\n" + "\n".join(erros[:15]) +
                ("\n..." if len(erros) > 15 else ""))
            return

        # ── CASO 2: APROVADO — mostra notas explicativas ───────
        self.lbl_gerar_status.config(
            text="✅ 0 erros — APTO PARA O PVA", foreground='#0a0')

        notas = self._extrair_notas_explicativas()
        resumo = "\n".join(info) if info else "(sem informações adicionais)"

        corpo = (
            "✅ 0 erros — arquivo APTO para o PVA.\n\n"
            "RESUMO DA VALIDAÇÃO\n"
            "──────────────────────────────────────────────────────\n"
            f"{resumo}\n\n"
            "══════════════════════════════════════════════════════\n"
            "  NOTAS EXPLICATIVAS / FATOS CONTÁBEIS GERADOS\n"
            "══════════════════════════════════════════════════════\n\n"
            f"{notas}\n"
        )

        win = tk.Toplevel(self.root)
        win.title("Validação — Arquivo APTO")
        win.geometry("760x600")
        win.transient(self.root)

        tk.Label(win, text="✅  Arquivo aprovado na validação",
                 bg='#e8f5e9', fg='#1a7f37',
                 font=('Segoe UI', 13, 'bold')).pack(fill='x', pady=(10, 6))

        txt = scrolledtext.ScrolledText(win, font=('Consolas', 10),
                                        wrap='word', bg='#fafafa')
        txt.pack(fill='both', expand=True, padx=12, pady=6)
        txt.insert('end', corpo)
        txt.config(state='disabled')

        ttk.Button(win, text="OK", command=win.destroy).pack(pady=(6, 12))

    def _salvar_como(self):
        if not self.linhas_geradas:
            messagebox.showwarning("Nada para salvar", "Gere o arquivo primeiro."); return
        ano = self.empresa['dt_fin'][4:8] if self.empresa else '2025'
        arq = filedialog.asksaveasfilename(
            title="Salvar arquivo SPED ECD", defaultextension=".txt",
            initialfile=f"sped_ecd_{ano}.txt",
            filetypes=[("Arquivos TXT", "*.txt")])
        if not arq: return
        try:
            with open(arq, 'wb') as f:
                for l in self.linhas_geradas:
                    f.write((l + '\r\n').encode('iso-8859-1'))
            with open(arq, 'rb') as f: cont = f.read()
            sha = hashlib.sha256(cont).hexdigest()[:16]
            self._log(f"[SALVAR] {arq} | {len(cont):,} bytes | SHA256:{sha}")
            self.lbl_gerar_status.config(text=f"Salvo: {os.path.basename(arq)}", foreground='#0a0')
            messagebox.showinfo("Salvo",
                f"Arquivo salvo!\n\n{arq}\n\nTamanho: {len(cont):,} bytes\nSHA256: {sha}")
        except Exception as e:
            self._log(f"[ERRO SALVAR] {e}")
            messagebox.showerror("Erro", str(e))

    def _log(self, msg):
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        self.txt_log.insert('end', f"[{ts}] {msg}\n")
        self.txt_log.see('end')

# ================================================================
# MAIN
# ================================================================
def main():
    root = tk.Tk()
    root.title("Gerador SPED ECD — v2.9")
    root.geometry("980x760"); root.minsize(900, 680)
    try: root.tk.call('tk', 'scaling', 1.2)
    except Exception: pass
    root.update_idletasks()
    w, h = 980, 760
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def mostrar_app():
        for w_ in root.winfo_children(): w_.destroy()
        AppSpedECD(root)
    def mostrar_welcome():
        for w_ in root.winfo_children(): w_.destroy()
        TelaInicial(root, callback_iniciar=mostrar_app, callback_sair=root.destroy)
    mostrar_welcome()
    root.mainloop()

if __name__ == '__main__':
    main()