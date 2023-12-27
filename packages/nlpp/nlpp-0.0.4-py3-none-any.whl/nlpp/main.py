def program1a():
    code = """
    import pandas as pd
    import os
    import docx
    import PyPDF2
    dir_path='C:\\Users\\ayush\\OneDrive\\Desktop\\DSCE\\7\\nl\\1'
    files=[f for f in os.listdir(dir_path) if (f.endswith('.txt') or f.endswith('.docx') or f.endswith('.pdf'))]
    data = []
    for txt_file in files:
        if(txt_file.endswith('.txt')):
            with open(os.path.join(dir_path, txt_file), 'r') as file:
                content = file.read()
                data.append({'filename': txt_file, 'content': content })
        elif(txt_file.endswith('.docx')):
            docx_path = os.path.join(dir_path, txt_file)
            doc = docx.Document(docx_path)
            content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            data.append({'filename': txt_file, 'content': content })
        elif(txt_file.endswith('.pdf')):
            with open(os.path.join(dir_path, txt_file), 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                num_pages = len(pdf_reader.pages)
                for page in range(num_pages):
                    content=pdf_reader.pages[page].extract_text()
                data.append({'filename': txt_file, 'content': content}) 
    df = pd.DataFrame(data)
    print(df)    """
    print(code)

def program1b():
    code="""
    import os

    dir_path = 'C:\\Users\\ayush\\OneDrive\\Desktop\\DSCE\\7\\nl\\1'
    files = [f for f in os.listdir(dir_path) if f.endswith('.txt')]
    data = []

    for txt_file in files:
        with open(os.path.join(dir_path, txt_file), 'r') as file:
            content = file.read()
            data.append({'filename': txt_file, 'content': content})

    # Print the content of text files
    for item in data:
        print("Filename:", item['filename'])
        print("Content:")
        print(item['content'])
        print("\n")  
"""
    print(code)

def program2a():
    code="""
    import pandas as pd
    import re
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    nltk.download('punkt')
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    def clean_text(text):
        text = re.sub(r'[^A-Za-z\s]', '', text)
        text = text.lower()
        tokens = word_tokenize(text)
        tokens = [ps.stem(word) for word in tokens if word not in stop_words]
        return ' '.join(tokens)
        df['cleaned_content'] = df['content'].apply(clean_text)
        lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in tokens])
        print(lemmatized_output)
    df['cleaned_content'] = df['content'].apply(clean_text)
    print(df)"""
    print(code)

def program2b():
    code="""
    import pandas as pd
    import re

    # Sample data creation (replace this with your actual data loading logic)
    data = {'content': ["This is an example sentence.", "Another example sentence."]}
    df = pd.DataFrame(data)

    def clean_text(text):
        # Remove non-alphabetic characters
        text = re.sub(r'[^A-Za-z\s]', '', text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize
        tokens = text.split()
        
        # Remove stopwords
        stop_words = set(["is", "an", "the", "this", "another"])  # Add more stopwords as needed
        tokens = [word for word in tokens if word not in stop_words]
        
        # Stemming (using a simple example)
        tokens = [word[:-1] if word.endswith('s') else word for word in tokens]
        
        # Lemmatization (using a simple example)
        tokens = [word[:-1] if word.endswith('s') else word for word in tokens]

        return ' '.join(tokens)

    df['cleaned_content'] = df['content'].apply(clean_text)
    print(df)    
"""
    print(code)

def program3a():
    code="""
    from nltk.util import ngrams
    import pandas as pd
    # Sample data creation
    data = {'cleaned_content': ["this is an example sentence", "another example sentence"]}
    df = pd.DataFrame(data)
    def generate_ngrams(text, n):
        tokens = text.split()
        return [' '.join(gram) for gram in ngrams(tokens, n)]
    df['trigram'] = df['cleaned_content'].apply(generate_ngrams, n=2)
    print(df)

    """
    print(code)

def program3b():
    code="""
    import pandas as pd

    # Sample data creation
    data = {'cleaned_content': ["this is an example sentence", "another example sentence"]}
    df = pd.DataFrame(data)

    # Function to generate bigrams
    def generate_ngrams(text, n):
        tokens = text.split()
        ngrams_list = [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]
        return ngrams_list

    # Apply the function to generate bigrams
    df['bigrams'] = df['cleaned_content'].apply(generate_ngrams, n=2)

    # Print the dataframe
    print(df)
"""
    print(code)


def program4a():
    code="""
    import nltk
    nltk.download('averaged_perceptron_tagger')
    def pos_tagging(text):
        tokens = nltk.word_tokenize(text)
        return nltk.pos_tag(tokens)
    # Apply POS tagging to the cleaned_content
    df['POS_tags'] = df['cleaned_content'].apply(pos_tagging)
    print(df)
"""
    print(code)


def program4b():
    code="""
    import pandas as pd

    # Sample data creation
    data = {'cleaned_content': ["this is an example sentence", "another example sentence"]}
    df = pd.DataFrame(data)

    # Function to generate simple POS tags (Noun, Verb, Adjective)
    def simple_pos_tagging(text):
        tokens = text.split()
        pos_tags = []
        for token in tokens:
            if token.endswith('ing'):
                pos_tags.append((token, 'Verb'))
            elif token.endswith('ly'):
                pos_tags.append((token, 'Adverb'))
            else:
                pos_tags.append((token, 'Noun'))
        return pos_tags

    # Apply the function to generate POS tags
    df['POS_tags'] = df['cleaned_content'].apply(simple_pos_tagging)

    # Print the dataframe
    print(df)

"""
    print(code)


def program5a():
    code="""
    import nltk 
    nltk.download('maxent_ne_chunker') 
    nltk.download('words')
    def noun_phrase_chunking(text_with_tags): 
        grammar = "NP: {<DT>?<JJ>*<NN>}"
        cp = nltk.RegexpParser(grammar)
        tree = cp.parse(text_with_tags)
        noun_phrases = [] 
        for subtree in tree.subtrees(): 
            if subtree.label() == 'NP': 
                noun_phrases.append(' '.join(word for word, tag in subtree.leaves())) 
        return noun_phrases
    df['noun_phrases'] = df['POS_tags'].apply(noun_phrase_chunking) 
    print(df)"""


    print(code)


def program5b():
    code="""
    import pandas as pd
    # Sample data creation
    data = {'POS_tags': [
        [('this', 'Noun'), ('is', 'Noun'), ('an', 'Noun'), ('example', 'Noun'), ('sentence', 'Noun')],
        [('another', 'Noun'), ('example', 'Noun'), ('sentence', 'Noun')]
    ]}
    df = pd.DataFrame(data)

    # Function to perform simple noun phrase chunking
    def simple_noun_phrase_chunking(pos_tags):
        noun_phrases = []
        current_phrase = []
        
        for token, tag in pos_tags:
            if tag in ['Noun', 'Adjective']:
                current_phrase.append(token)
            elif current_phrase:
                noun_phrases.append(' '.join(current_phrase))
                current_phrase = []
        
        if current_phrase:
            noun_phrases.append(' '.join(current_phrase))
        
        return noun_phrases

    # Apply the function to generate noun phrases
    df['noun_phrases'] = df['POS_tags'].apply(simple_noun_phrase_chunking)

    # Print the dataframe
    print(df)
"""


    print(code)


def program6a():
    code="""
    import spacy
    import random

    # Load the spaCy model
    nlp = spacy.load("en_core_web_sm")

    # Sentence prompts dictionary
    sentence_prompts = {
        "She opened the door and saw a": ["beautiful garden", "mysterious figure", "bright light"],
        "After a long day at work, I like to relax by": ["watching my favorite TV show", "going for a walk", "reading a book"]
    }

    # Input prompt
    input_prompt = "After a long day at work, I like to relax by"

    # Check if the input prompt is in the dictionary
    if input_prompt in sentence_prompts:
        possible_completions = sentence_prompts[input_prompt]
        print("Possible Completions:")
        for completion in possible_completions:
            print(f"- {input_prompt} {completion}")
    else:
        print("Prompt not found in the dictionary.")
        # Use spaCy to generate a random sentence completion
        doc = nlp(input_prompt)
        random_completion = " ".join([token.text for token in doc] + [random.choice(["enjoying", "listening", "playing"])])
        print(f"- {random_completion}")"""
    
    print(code)


def program6b():
    code="""
    sentence_prompts = {
    "She opened the door and saw a": ["beautiful garden", "mysterious figure", "bright light"],
    "After a long day at work, I like to relax by": ["watching my favorite TV show", "going for a walk", "reading a book"]
    }

    input_prompt = "After a long day at work, I like to relax by"

    if input_prompt in sentence_prompts:
        possible_completions = sentence_prompts[input_prompt]
        print("Possible Completions:")
        for completion in possible_completions:
            print(f"- {input_prompt} {completion}")
    else:
        print("Prompt not found in the dictionary.")
        # Use random to create a random sentence completion
        random_completion = random.choice(["enjoying a cup of tea", "listening to music", "playing video games"])
        print(f"- {input_prompt} {random_completion}")
"""
    print(code)

def program7a():
    code="""
    from textblob import TextBlob
    data = ["I love this product!", "It's terrible.", "Neutral statement."]
    sentiments = [TextBlob(text).sentiment.polarity for text in data]
    labels = ['positive' if score > 0 else 'negative' if score < 0 else'neutral' for score in sentiments]
    result_df = pd.DataFrame({'text': data, 'sentiment_score': sentiments,'label': labels})
    print(result_df)"""

    print(code)



def program7b():
    code="""
    data = ["I love this product!", "It's terrible.", "Neutral statement."]

    def determine_sentiment_label(text):
        if "love" in text.lower():
            return 'positive'
        elif "terrible" in text.lower():
            return 'negative'
        else:
            return 'neutral'

    result_dict = {'text': data, 'label': [determine_sentiment_label(text) for text in data]}

    for text, label in zip(result_dict['text'], result_dict['label']):
        print(f"Text: {text}")
        print(f"Label: {label}")
        print()
"""

    print(code)




def program8a():
    code="""
    pip install transformers
    pip install sentence-transformers
    from transformers import GPT2Tokenizer, GPT2LMHeadModel, BartTokenizer, BartForConditionalGeneration
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    def abstractive_summarization(text):
        # GPT-2 model for abstractive summarization
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        model = GPT2LMHeadModel.from_pretrained("gpt2")

        # Tokenize and generate summary
        inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs, max_length=150, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return summary



    def extractive_summarization_sentence_transformers(text, num_sentences=3):
        # Sentence Transformers for extractive summarization
        model = SentenceTransformer("bert-base-nli-mean-tokens")

        # Split text into sentences
        sentences = text.split('. ')

        # Compute sentence embeddings
        embeddings = model.encode(sentences)

        # Calculate pairwise cosine similarity between embeddings
        similarity_matrix = cosine_similarity(embeddings, embeddings)

        # Get indices of top-ranked sentences based on similarity
        top_sentence_indices = np.argsort(similarity_matrix.sum(axis=1))[-num_sentences:]

        # Sort sentences based on their original order
        top_sentence_indices = sorted(top_sentence_indices)

        # Generate extractive summary
        extractive_summary = '. '.join(sentences[i] for i in top_sentence_indices)

        return extractive_summary

    # Example usage
    text = "In the heart of the bustling city, there stood an old bookstore with creaky woodenfloors and shelves that seemed to lean under the weight of countless stories. The air wasfilled with the comforting scent of aged paper and the soft murmur of people lost in the  worlds between the covers. A the afternoon sun streamed through dusty windows, casting awarm glow on antique book covers, occasionally knocking over a book or two. The bookstore, with its charm and character, was a haven for book lovers seeking solace and adventure within the pages of both old classics and new releases."
    abstractive_summary = abstractive_summarization(text)

    extractive_summary_sentence_transformers = extractive_summarization_sentence_transformers(text)

    print("Abstractive Summary:", abstractive_summary)

    print("\nExtractive Summary:", extractive_summary_sentence_transformers)    
    """
    print(code)


def program8b():
    code="""
    def simple_summarization(article, num_sentences=3):
        sentences = article.split(".")
        # Remove empty strings from the list
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Calculate the importance score for each sentence (based on sentence length)
        scores = [len(sentence) for sentence in sentences]
        
        # Select the top N sentences with the highest importance scores
        selected_sentences = sorted(zip(sentences, scores), key=lambda x: x[1], reverse=True)[:num_sentences]
        
        # Extract the selected sentences
        summary = [sentence for sentence, _ in selected_sentences]
        
        return '. '.join(summary)

    # Article text
    article = "Enter your text here"

    # Perform summarization
    summary = simple_summarization(article)

    # Print the summary
    print(summary)

"""
    print(code)

def program9a():
    code="""
    import nltk
    from nltk import pos_tag
    from nltk.tokenize import word_tokenize
    from nltk.chunk import ne_chunk
    nltk.download('punkt')
    nltk.download('maxent_ne_chunker')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('words')
    text = "Barack Obama was born in Hawaii and served as the 44th President of the United States."
    words = word_tokenize(text)
    pos_tags = pos_tag(words)
    named_entities = ne_chunk(pos_tags)
    print(named_entities)"""
    
    print(code)


def program9b():
    code="""
    sentence = "Barack Obama was born in Hawaii and served as the 44th President of the United States"

    # Initialize lists
    person_list = []
    place_list = []

    # Extract entities and populate lists
    entities = sentence.split()
    for entity in entities:
        if entity in ["Barack", "Obama"]:
            person_list.append(entity)
        elif entity in ["Hawaii", "United", "States"]:
            place_list.append(entity)

    # Print the lists
    print("Person List:", person_list)
    print("Place List:", place_list)"""
    
    print(code)

def program10a():
    code="""
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer, WordNetLemmatizer
    from nltk.corpus import wordnet
    nltk.download('punkt')
    nltk.download('wordnet')
    text = "The quick brown foxes are jumping over the lazy dogs."
    words = word_tokenize(text)
    porter_stemmer = PorterStemmer()
    stemmed_words = [porter_stemmer.stem(word) for word in words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, pos=wordnet.VERB) for
    word in words]
    print("Original words:", words)
    print("Stemmed words:", stemmed_words)
    print("Lemmatized words:", lemmatized_words)
    print("\n")
    word = "misunderstanding"
    prefixes = ["mis"]
    root = "understand"
    suffixes = ["ing"]
    morphemes = []
    for prefix in prefixes:
        if word.startswith(prefix):
            morphemes.append(prefix)
            word = word[len(prefix):]
    morphemes.append(word)
    print("Word:", word)
    print("Morphemes:", morphemes)     
    """
    print(code)


def program10b():
    code="""
    def simple_tokenizer(text):
    return text.split()

    def simple_porter_stemmer(word):
        # A simple stemming function (for illustration purposes)
        if word.endswith("es"):
            return word[:-2]
        elif word.endswith("s"):
            return word[:-1]
        elif word.endswith("ing"):
            return word[:-3]
        return word

    def simple_wordnet_lemmatizer(word):
        # A simple lemmatization function (for illustration purposes)
        if word.endswith("es"):
            return word[:-2]
        elif word.endswith("s"):
            return word[:-1]
        elif word.endswith("ing"):
            return word[:-3]
        return word

    def analyze_morphemes(word, prefixes, root, suffixes):
        morphemes = []
        for prefix in prefixes:
            if word.startswith(prefix):
                morphemes.append(prefix)
                word = word[len(prefix):]
        morphemes.append(root)
        for suffix in suffixes:
            if word.endswith(suffix):
                morphemes.append(suffix)
                word = word[:-len(suffix)]
        return morphemes

    text = "The quick brown foxes are jumping over the lazy dogs"
    words = simple_tokenizer(text)

    stemmed_words = [simple_porter_stemmer(word) for word in words]
    lemmatized_words = [simple_wordnet_lemmatizer(word) for word in words]

    print("Original words:", words)
    print("Stemmed words:", stemmed_words)
    print("Lemmatized words:", lemmatized_words)
    print("\n")

    word = "misunderstanding"
    prefixes = ["mis"]
    root = "understand"
    suffixes = ["ing"]
    morphemes = analyze_morphemes(word, prefixes, root, suffixes)

    print("Word:", word)
    print("Morphemes:", morphemes)
"""
    print(code)


    