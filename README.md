# 🧠✨ **Gerador de Nuvens de Palavras por Emoção e Turma**  
### *Google Sheets → Análise Linguística → WordCloud Inteligente*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)]()  
[![spaCy](https://img.shields.io/badge/spaCy-NLP-orange)]()  
[![Google Sheets API](https://img.shields.io/badge/Google%20Sheets-API-success?logo=google-sheets&logoColor=white)]()  
[![WordCloud](https://img.shields.io/badge/WordCloud-Visualization-blue)]()  
[![License MIT](https://img.shields.io/badge/License-MIT-yellow)]()

---

## 🚀 **Sobre o Projeto**

Este projeto conecta-se a uma planilha do **Google Sheets**, lê frases emocionais enviadas por alunos, identifica a emoção predominante em cada turma e gera **nuvens de palavras coloridas**, filtradas por relevância e priorizando as frases mais recentes.

A análise inclui:

- 🧹 Remoção de *stopwords* em português (spaCy)  
- 🎨 Escolha automática da cor da nuvem com base na emoção predominante  
- 🕒 Ordenação por data (da mais recente para a mais antiga)  
- ☁️ Geração visual com WordCloud  
- 🏫 Processamento por **turma**  
- 🔐 Autenticação OAuth2 integrada ao Google  

É plug-and-play: basta colocar o `cliente_secret.json` e rodar.

---

## 📸 **Exemplo de Resultado**
*(adicione aqui o print da nuvem se quiser)*

---

## 📦 **Tecnologias Utilizadas**

| Tecnologia | Uso |
|-----------|------|
| **Python** | Execução do projeto |
| **Google Sheets API** | Leitura dos dados |
| **spaCy (pt_core_news_sm)** | NLP + remoção de stopwords |
| **WordCloud** | Visualização |
| **matplotlib** | Renderização das nuvens |
| **OAuth2** | Autenticação |

---

## 🔧 **Instalação**

### 1️⃣ Clone o projeto
```sh
git clone https://github.com/SEU-REPO-AQUI
cd projeto-wordcloud
```

### 2️⃣ Instale as dependências
```sh
pip install -r requirements.txt
```

### 3️⃣ Baixe o modelo spaCy
```sh
python -m spacy download pt_core_news_sm
```

### 4️⃣ Configure a API Google

1. Acesse https://console.cloud.google.com  
2. Crie um projeto.  
3. Ative **Google Sheets API**.  
4. Baixe o `credentials.json`.  
5. Renomeie para:  
   ```
   cliente_secret.json
   ```
6. Coloque na raiz do projeto.

Na primeira execução, um navegador abrirá pedindo login.  
Depois disso, será criado automaticamente o arquivo `token.json`.

---

## ▶️ **Como Executar**

```sh
python main.py
```

Pronto. Ele gera automaticamente a nuvem da turma específica configurada:

```python
gerar_nuvem_turma("1ºI")
```

---

## 🎨 **Cores por Emoção**

| Emoção | Cor |
|--------|------|
| Raiva | 🔴 Red |
| Tristeza | 🔵 Blue |
| Felicidade | 🟡 Yellow |
| Medo | 🟣 Purple |
| Nojo | 🟢 Green |
| Surpresa | 🟠 Orange |

---

## 📊 **Formato da Planilha Esperado**

| Data/Hora | Emoção | Frase | Turma | ... |
|-----------|--------|--------|--------|------|
| 12/11/2024 10:15:03 | Raiva | Estou cansado | 1ºI | ... |

---

## 🛠️ **Como Alterar a Turma Processada**

No final do script:

```python
gerar_nuvem_turma("1ºI")
```

Exemplos:

```python
gerar_nuvem_turma("2ºC")
gerar_nuvem_turma("3ºA")
```

---

## ⚠️ **Possíveis Problemas e Soluções**

### ❌ spaCy não instalado
```
OSError: [E050] Can't find model 'pt_core_news_sm'
```
✔️ Solução:
```sh
python -m spacy download pt_core_news_sm
```

---

### ❌ Erro de autenticação Google
Apague o arquivo e execute de novo:
```
token.json
```

---

### ❌ Erro de data inválida
O script exige:
```
%d/%m/%Y %H:%M:%S
```

---

## 🧭 **Melhorias Futuras**

- Exportação automática em PNG/JPEG  
- Dashboard web (Streamlit)  
- Comparação emocional por período  
- Heatmaps emocionais por turma  
- Modo relatório PDF automático  

---

## 📄 **Licença**

MIT — Livre para usar, estudar, modificar e distribuir.
