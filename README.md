Gerador de Nuvem de Palavras por Turmas — Google Sheets + spaCy + WordCloud

Projeto que lê respostas de um Google Sheets, processa textos emocionais de alunos, identifica a emoção predominante por turma e gera nuvens de palavras personalizadas, priorizando as frases mais recentes e filtrando stopwords em português.

1. Visão Geral

Este script:

Conecta à API do Google Sheets (modo leitura).

Extrai dados de uma planilha no formato:
Data/Hora – Emoção – Frase – Turma – …

Organiza as frases por turma.

Remove stopwords usando spaCy (pt_core_news_sm).

Calcula a emoção predominante da turma.

Gera uma WordCloud colorida baseada nessa emoção.

Ordena as frases por data, dando mais peso ao que é recente.

2. Tecnologias Utilizadas

Python 3

Google Sheets API

spaCy (pt_core_news_sm)

WordCloud

matplotlib

collections.Counter

OAuth2 (token.json)

3. Instalação
Clone o projeto
git clone https://github.com/.../seu-repo.git
cd seu-repo

Instale dependências
pip install -r requirements.txt

Instale o modelo do spaCy
python -m spacy download pt_core_news_sm

4. Configuração da API Google

Entre em
https://console.cloud.google.com

Crie um projeto.

Ative Google Sheets API.

Baixe o arquivo credentials.json (renomeado no projeto para cliente_secret.json).

Coloque-o na raiz do projeto.

O script gerará automaticamente um token.json na primeira execução.

5. Como Rodar
python main.py


Na primeira execução, abrirá uma janela de autenticação Google.

6. Estrutura Interna do Script
Extração dos dados

Lê a aba "Respostas!A:I" da planilha.

Remove itens vazios.

Extrai:
data/hora, emoção, frase, turma.

Organização por turmas
turmas[turma] = {
    "frases": [(data_hora, frase), ...],
    "emocoes": [emocao1, emocao2, ...]
}

Limpeza com spaCy

Remove stopwords mantendo apenas palavras relevantes.

Emoção predominante

Conta frequência e escolhe a mais comum:

Counter(emocoes).most_common(1)

Cores por emoção
EMOTION_COLORS = {
    "Nojo": "green",
    "Felicidade": "yellow",
    "Tristeza": "blue",
    "Medo": "purple",
    "Raiva": "red",
    "Surpresa": "orange",
}

Geração da nuvem

Ordena frases por data (mais recentes primeiro)

Remove stopwords

Gera WordCloud colorida com a predominância emocional

wordcloud = WordCloud(
    width=800, height=400,
    background_color="white",
    color_func=lambda *args, **kwargs: cor_nuvem
)

7. Alterar a turma desejada

Edite a linha final:

gerar_nuvem_turma("1ºI")


Exemplos:

gerar_nuvem_turma("2ºC")
gerar_nuvem_turma("3ºA")

8. Estrutura da Planilha Esperada
Data/Hora	Emoção	Frase	Turma	...
12/11/2024 10:15:03	Raiva	Estou cansado	1ºI	…
9. Possíveis Erros
Erro de autenticação

Delete token.json e rode novamente.

Modelo spaCy não instalado
OSError: [E050] Can't find model 'pt_core_news_sm'


Instale:

python -m spacy download pt_core_news_sm

Formato de data inválido

O script espera:

"%d/%m/%Y %H:%M:%S"

10. Melhorias Futuras

Exportar nuvens como PNG automaticamente

Dashboard web com Streamlit

Agrupar emoções por período

Comparar evolução emocional por turma

11. Licença

MIT – Livre para uso e adaptação.
