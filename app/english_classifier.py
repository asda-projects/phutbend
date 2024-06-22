import nltk
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from collections import Counter
import spacy

# Certifique-se de ter baixado os dados necessários
nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")

# Definir frases e seus níveis de complexidade
frases = [
    "The cat is on the table.",
    "I like to read books.",
    "She is my best friend.",
    "We go to school every day.",
    "They have two children.",
    "I have been learning English for three years.",
    "The weather is nice today, isn't it?",
    "She enjoys playing the piano in her free time.",
    "They are planning a trip to Europe next summer.",
    "The book you lent me was very interesting.",
    "Despite the challenges, she managed to complete the project on time.",
    "The film was fascinating, with a plot that kept the audience engaged throughout.",
    "He proposed a new theory that has the potential to revolutionize the field of physics.",
    "Although the meeting was lengthy, it was productive and resulted in several actionable items.",
    "Her eloquence and command of the language were evident in her persuasive speech."
]
labels = [
    0, 0, 0, 0, 0,  # Nível Básico (A1-A2)
    1, 1, 1, 1, 1,  # Nível Intermediário (B1-B2)
    2, 2, 2, 2, 2   # Nível Avançado (C1-C2)
]

# Função para tokenizar e lematizar frases usando SpaCy
def tokenize_lemmatize(sentence):
    doc = nlp(sentence)
    return [token.lemma_ for token in doc]

# Calcular frequência das palavras no corpus
word_freq = Counter([word for sentence in frases for word in tokenize_lemmatize(sentence)])

# Função para extrair características de uma frase
def extract_features(sentence):
    tokens = tokenize_lemmatize(sentence)
    num_words = len(tokens)
    word_frequencies = [word_freq[word] for word in tokens]
    avg_freq = sum(word_frequencies) / num_words if num_words > 0 else 0
    return [num_words, avg_freq]

# Extrair características de todas as frases
features = [extract_features(sentence) for sentence in frases]

# Dividir dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Treinar o modelo
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Prever nível de complexidade de novas frases
predictions = clf.predict(X_test)

# Avaliar o modelo
accuracy = accuracy_score(y_test, predictions)
report = classification_report(y_test, predictions)

print(f"Accuracy: {accuracy}")
print(f"Classification Report:\n{report}")

# Classificar uma nova frase
nova_frase = "This is a simple sentence."
nova_features = extract_features(nova_frase)
nivel_predito = clf.predict([nova_features])[0]

print(f"Frase: {nova_frase}")
print(f"Nível de Complexidade: {nivel_predito}")
