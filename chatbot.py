import nltk
import random
import wikipedia
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
# baixe o recurso de stopwords
nltk.download('stopwords')

# inicialize a biblioteca wikipedia
wikipedia.set_lang('en')

# inicialize as respostas do chatbot
greetings = ['hello', 'hi', 'hey', 'hi there', 'hello there']
chatbot_info = ['I am a chatbot created by OpenAI. How can I help you today?']
default_responses = ["I'm sorry, I didn't understand your question.", "I'm not sure I can answer that.", "Could you please ask me something else?"]
stop_words = set(stopwords.words('english'))

# função para pré-processar o texto
def preprocess_text(text):
    # tokeniza o texto em palavras
    words = word_tokenize(text)
    # converte todas as palavras em minúsculas
    words = [word.lower() for word in words]
    # remove as palavras de parada (stop words)
    words = [word for word in words if word not in stop_words]
    # extrai o lema (raiz) de cada palavra
    lem = WordNetLemmatizer()
    words = [lem.lemmatize(word) for word in words]
    # junta as palavras novamente em um texto
    text = ' '.join(words)
    return text

# função para lidar com a entrada do usuário
def handle_input(user_input):
    # preprocessa a entrada do usuário
    user_input = preprocess_text(user_input)
    # verifica se a entrada do usuário é uma saudação
    for word in user_input.split():
        if word in greetings:
            return random.choice(greetings)
    # verifica se a entrada do usuário é uma pergunta sobre o chatbot
    if 'chatbot' in user_input:
        return random.choice(chatbot_info)
    # verifica se a entrada do usuário é uma pergunta sobre algum tópico
    if '?' in user_input:
        # extrai as palavras-chave da pergunta
        keywords = [word for word in user_input.split() if word not in ['what', 'when', 'where', 'why', 'how']]
        # pesquisa na Wikipedia as informações relacionadas às palavras-chave
        try:
            summary = wikipedia.summary(' '.join(keywords), sentences=1)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options[:5]
            return "Did you mean one of these: "
# função principal do chatbot
def chatbot():
    # saudação inicial do chatbot
    print(random.choice(greetings))
    while True:
        # obtém a entrada do usuário
        user_input = input('> ')
        # verifica se o usuário quer sair
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print('Goodbye!')
            break
        # processa a entrada do usuário e obtém uma resposta
        response = handle_input(user_input)
        # se não houver uma resposta, usa uma resposta padrão
        if not response:
            response = random.choice(default_responses)
        # exibe a resposta
        print(response)

# inicia o chatbot
if __name__ == '__main__':
    chatbot()
