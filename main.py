import os.path

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import spacy

from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from collections import Counter

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

nlp = spacy.load("pt_core_news_sm")

# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = "1ua12PFD2G6yS5ttMtIry8gUJHHh1hgjluHZGB3Bq8B4"
# SAMPLE_RANGE_NAME = "Respostas!A1:C84"

EMOTION_COLORS = {
    "Nojo": "green",
    "Felicidade": "yellow",
    "Tristeza": "blue",
    "Medo": "purple",
    "Raiva": "red",
    "Surpresa": "orange",
}

def main():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "cliente_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId='1-CjhQY3miJV8xkf38kP7WNFz6kwpCa9mwnahQQYYKro', range="Respostas!A:I")
            .execute()
        )
        values = result.get("values", [])

      
        # # Filtra e organiza os dados por emoção
        # emotion_data = {emotion: [] for emotion in EMOTION_COLORS.keys()}
        # for row in values:
        #     if len(row) > 2:  # Garante que há pelo menos dois índices
        #         emotion = "Raiva"
        #         if emotion in EMOTION_COLORS:
        #             # Limpa o texto da frase antes de adicionar
        #             cleaned_phrase = clean_text(row[2].strip())
        #             emotion_data[emotion].append(cleaned_phrase)

        # # Gera nuvens de palavras para cada emoção
        # for emotion, phrases in emotion_data.items():
        #     if phrases:  # Gera a nuvem apenas se houver frases
        #         text = " ".join(phrases)  # Junta todas as frases em um único texto
        #         color = EMOTION_COLORS[emotion]

        #         # Configuração da nuvem de palavras
        #         wordcloud = WordCloud(
        #             background_color="white",
        #             color_func=lambda *args, **kwargs: color,
        #             width=800,
        #             height=400,
        #         ).generate(text)

        #         # Exibe a nuvem de palavras
        #         plt.figure(figsize=(10, 5))
        #         plt.imshow(wordcloud, interpolation="bilinear")
        #         plt.axis("off")
        #         plt.title(f"Nuvem de Palavras - {emotion}", fontsize=16)
        #         plt.show()
        #     else:
        #         print(f"Sem frases para gerar nuvem de: {emotion}")

  # Dicionário para organizar as frases e datas por turma
        turmas = {}

        for row in values[1:]:
            if len(row) >= 8:
                selected_items = row[0:9]
                itemNulo = [item.strip() for item in selected_items if item]
                if len(itemNulo) > 3:
                    data_hora, frase, turma, emocao = itemNulo[0], itemNulo[2], itemNulo[3], itemNulo[1]
                    if turma not in turmas:
                        turmas[turma] = {"frases": [], "emocoes": []}
                    # Armazena a data e a frase como uma tupla
                    turmas[turma]["frases"].append((data_hora, frase))
                    turmas[turma]["emocoes"].append(emocao)  # Adiciona a emoção associada

        # Função para remover stopwords
        def remover_stopwords(frases):
            frases_sem_stopwords = []
            for frase in frases:
                doc = nlp(frase)
                frase_limpa = ' '.join([token.text for token in doc if not token.is_stop])
                frases_sem_stopwords.append(frase_limpa)
            return ' '.join(frases_sem_stopwords)  # Junta todas as frases de uma turma

        # Função para determinar a cor da nuvem baseada na emoção predominante
        def cor_predominante(emocoes):
            if not emocoes:
                return "gray"  # Cor padrão para turmas sem emoção
            contagem_emocoes = Counter(emocoes)
            emocao_mais_comum = contagem_emocoes.most_common(1)[0][0]  # Emoção mais comum
            return EMOTION_COLORS.get(emocao_mais_comum, "gray")  # Retorna a cor correspondente

        # Função para gerar nuvem de palavras de uma turma específica, com prioridade nas frases mais recentes
        def gerar_nuvem_turma(turma):
            if turma in turmas:
                # Ordena as frases da turma pela data, da mais recente para a menos recente
                turmas[turma]["frases"].sort(key=lambda x: datetime.strptime(x[0], "%d/%m/%Y %H:%M:%S"), reverse=True)
                
                # Extrai as frases em ordem e remove stopwords
                frases_ordenadas = [frase for _, frase in turmas[turma]["frases"]]
                frases_sem_stopwords = remover_stopwords(frases_ordenadas)
                
                # Determina a cor predominante com base nas emoções
                cor_nuvem = cor_predominante(turmas[turma]["emocoes"])
                
                # Gera e exibe a nuvem de palavras
                wordcloud = WordCloud(
                    width=800,
                    height=400,
                    background_color='white',
                    max_words=200,
                    color_func=lambda *args, **kwargs: cor_nuvem
                ).generate(frases_sem_stopwords)
                
                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                plt.title(f"Nuvem de Palavras - Turma {turma} ({cor_nuvem.upper()})")
                plt.show()
            else:
                print(f"Turma {turma} não encontrada.")

        # Exemplo de uso: Gerar nuvem para a turma '1ºI'
        gerar_nuvem_turma("1ºI")


        # filtro = []

        # for row in values[1:]:
        #     if len(row) >= 8:
        #         selected_items = row[0:9]
        #         itemNulo = [item.strip() for item in selected_items if item]  # Remove espaços em branco
        #         filtro.append(itemNulo)


        # for i, data in enumerate(filtro):
        #     if len(data) > 3:  # Garante que a lista tenha pelo menos 4 elementos
        #         filtro[i] = [data[0], data[2], data[3]]
        #     else:
        #         print(f"A lista na posição {i} tem menos de 4 elementos e foi ignorada: {data}")



        # filtro.sort(key=lambda x: datetime.strptime(x[0], "%d/%m/%Y %H:%M:%S"), reverse=True)        

        # # Verifica o conteúdo de filtro
        # # for data in filtro:
        # #     print(data) 


        # frases2C = []

        # for data in filtro:
        #     # Verifica se há um segundo item e se é '2ºC' após remover espaços em branco
        #     if len(data) > 2 and data[2].strip() == '2°C':
        #         frases2C.append(data[1])

        # # Exibe o resultado
        # for data in frases2C:
        #     print(data) 


    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
