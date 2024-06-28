from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain.prompts import PromptTemplate
from flask import Flask, jsonify, request, session
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from transformers import AutoTokenizer, pipeline
from transformers import AutoModelForSequenceClassification
from langchain_community.llms import HuggingFaceHub
from scipy.special import softmax
from flask import jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
from rake_nltk import Rake
from pytrends.request import TrendReq
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from flask_cors import CORS
import pymongo
import time
import os
import json
import numpy as np
import pandas as pd
import requests
import datetime
import torch
from dotenv import load_dotenv, get_key
load_dotenv()
import nltk

# # import statsmodels.api as sm

# # ---------------------------------------
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')
# # ---------------------------------------
app = Flask(__name__)
CORS(app)

reviewList = []
global_title = ""
revString = [""]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

def extract_starting_words(sentence):
    # Split the sentence into words
    words = sentence.split()

    # Extract the first 3 words
    starting_words = ' '.join(words[:3])

    return starting_words

def createProduct(url):
  global global_title
  page = requests.get(url, headers=headers)
  time.sleep(2)
  soup = BeautifulSoup(page.content, "html.parser")
  title = soup.find(id="productTitle").get_text()
  global_title = extract_starting_words(title)
  desc = soup.find(id="productDescription").get_text()
  img = soup.find('img', {'id': 'landingImage'})['src']
  price = soup.find('span', class_='a-offscreen').text.strip()
  date = datetime.datetime.now()
  avgRating = soup.find('span', {'data-hook': 'rating-out-of-text'}).text.strip()
  strDate = date.strftime("%Y-%m-%d %H:%M:%S")
  product_details = {
      'name': title.strip(),
      'url': url,
      'description': desc.strip(),
      'image': img,
      'price': price,
      'date': strDate,
       'avgRating': float(avgRating.split()[0]),
      }
#   print(f"product details : {product_details}")
  filter_query = { "email": "sonarsiddhesh105@gmail.com" }
  # print(db)
  client = pymongo.MongoClient("mongodb+srv://sonarsiddhesh105:K5NuO27RwuV2R986@cluster0.0aedb3y.mongodb.net/?retryWrites=true&w=majority")
  db = client['test']
  collect = db['cres_users']
  update_result = collect.update_one(filter_query, { "$push": { "products": product_details } })
#   print("Documents :", update_result)
  return url

def extractReviews(rurl, uurl):
  page = requests.get(rurl, headers=headers)
  soup = BeautifulSoup(page.content, "html.parser")
  reviews = soup.findAll('div', {'data-hook': 'review' })
#   print(f"reviews : {reviews}")
  for item in reviews:
    ratingText = item.find('i', {'data-hook': 'review-star-rating' }).text.strip()
    fullDate = item.find('span', {'data-hook': 'review-date' }).text.strip()
    date_obj = fullDate.split('on')[1].strip()
    review = {
        # 'title': title.strip(),
        'rating': ratingText,
        'star': float(ratingText.split()[0]),
        'body': item.find('span', {'data-hook': 'review-body' }).text.strip(),
        'fullDate': fullDate,
        'date': date_obj,
    }
    # print(review)
    reviewList.append(review)
    revString[0] = revString[0] + " " + review['body']
  filter_query = { "email": "sonarsiddhesh105@gmail.com" }  # Filter to find the user with the specified email
  update_query = { "$set": { "products.$[product].reviews": reviewList[:10] } }  # Update the reviews field of the matched product

  # Use arrayFilters to match the specific product within the products array
  array_filters = [{ "product.url": uurl }]
  client = pymongo.MongoClient("mongodb+srv://sonarsiddhesh105:K5NuO27RwuV2R986@cluster0.0aedb3y.mongodb.net/?retryWrites=true&w=majority")
  db = client['test']
  collect = db['cres_users']
  update_result = collect.update_one(filter_query, update_query, array_filters=array_filters)
  return reviewList

valid_timeframes = [
    "now 7-d",
    "today 1-m",
    "today 3-m",
    "today 12-m",
    "today 5-y"
]

data = pd.read_csv('db.csv')

# Sentimental Analysis

# Aspect Based Sentiment Analysis

tokenizer_for_deberta = AutoTokenizer.from_pretrained("yangheng/deberta-v3-large-absa-v1.1")
deberta_model = AutoModelForSequenceClassification.from_pretrained("yangheng/deberta-v3-large-absa-v1.1")
classifier_deberta = pipeline("text-classification", model=deberta_model, tokenizer=tokenizer_for_deberta)

# Sentimental Analysis
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

app.secret_key = 'supersecret'

# helper function to lemmatize the text
def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    tokenized = word_tokenize(text)
    lemmatized = [lemmatizer.lemmatize(word) for word in tokenized]
    lemmatized_text = ' '.join(lemmatized)
    return lemmatized_text

@app.route('/')
def index():
    return 'Hello, World!'


# Aspect Based Sentiment Analysis
@app.route('/absa', methods=['GET'])
def absa():
    review = revString[0]
    # review = request.form['text']
    # print(f"review : {review}")
    try:
        aspects = request.form['aspects']
        aspects = aspects.split(',')
    except Exception as e:
        print(str(e))
        aspects = ['performance','durability','pricing','sensitivity']
    try:
        res = []
        for aspect in aspects:
            element = classifier_deberta(review, text_pair=aspect)
            label = element[0]['label']
            score = element[0]['score']
            res.append({'aspect': aspect, 'label': label, 'score': score})
        # client = pymongo.MongoClient("mongodb+srv://sonarsiddhesh105:K5NuO27RwuV2R986@cluster0.0aedb3y.mongodb.net/?retryWrites=true&w=majority")
        # db = client['test']
        # collect = db['cres_users']
        # email = session.get('email')
        # filter_query = {"email": email}
        # update_query = {"$set": {"products.$[product].aspecSentiment": res}}
        # array_filters = [{"product.url": session.get('url')}]
        # update_result = collect.update_one(filter_query, update_query, array_filters=array_filters)
        # print("Documents matched:", update_result.matched_count)
        # print("Documents modified:", update_result.modified_count)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/kextract', methods=['GET'])
def kextract():
    text = revString[0]
    r = Rake()
    try:
        lemmatized_text = lemmatize_text(text)
        email = session.get('email')
        # print(email, session.get('url'),revString[0])
        r.extract_keywords_from_text(lemmatized_text)
        keywords_with_scores = r.get_ranked_phrases_with_scores()
        keywords_list = [{"word": keyword, "score": score} for score, keyword in keywords_with_scores]
        # client = pymongo.MongoClient("mongodb+srv://sonarsiddhesh105:K5NuO27RwuV2R986@cluster0.0aedb3y.mongodb.net/?retryWrites=true&w=majority")
        # db = client['test']
        # collect = db['cres_users']

        # filter_query = {"email": email}
        # update_query = {"$set": {"products.$[product].keywords": keywords_list}}
        # array_filters = [{"product.url": session.get('url')}]
        # update_result = collect.update_one(filter_query, update_query, array_filters=array_filters)
        # print("Documents matched:", update_result.matched_count)
        # print("Documents modified:", update_result.modified_count)
        return jsonify(keywords_list)
    except Exception as e:
        return jsonify({"error": str(e)})

# Sentimental Analysis    

def polarity_scores_roberta(example):
    encoded_text = tokenizer(example, return_tensors="pt")
    # trim the excess tokens
    encoded_text = {k: v[:, :512] for k, v in encoded_text.items()}
    with torch.no_grad():
        output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    scores = scores.astype(np.float64)

    return {
        "negative": float(scores[0]),
        "neutral": float(scores[1]),
        "positive": float(scores[2])
    }


# Sentimental Analysis
@app.route("/sentiment", methods=["GET"])
def analyze_sentiment():
    try:
        text = revString[0]

        scores = polarity_scores_roberta(text)
        
        return jsonify(scores)

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/start',methods=["POST"])
def start():
    try:
        url = request.form['url']
        session['email'] = request.form['email']
        # url = 'https://www.amazon.in/DABUR-Toothpaste-800G-Ayurvedic-Treatment-Protection/dp/B07HKXSC6K?ref_=Oct_d_otopr_d_1374620031_1&pd_rd_w=kY9CL&content-id=amzn1.sym.c4fc67ca-892d-48d9-b9ed-9d9fdea9998e&pf_rd_p=c4fc67ca-892d-48d9-b9ed-9d9fdea9998e&pf_rd_r=MHNFPBXAZ4VTV28WDF48&pd_rd_wg=kpToS&pd_rd_r=e5fbdca6-653c-4ace-80d9-a84f619d8dad&pd_rd_i=B07HKXSC6K'
        uniqueUrl = createProduct(url)
        nurl = url.split('?')
        url = nurl[0]
        reviewUrl = url.replace("dp", "product-reviews") + "?pageNumber=1"
        x = extractReviews(reviewUrl, uniqueUrl)
        client = pymongo.MongoClient("mongodb+srv://sonarsiddhesh105:K5NuO27RwuV2R986@cluster0.0aedb3y.mongodb.net/?retryWrites=true&w=majority")
        db = client['test']
        collect = db['cres_users']
        # print(f"revString : {revString}")
        user = collect.find_one({'email': session['email']})
        print(f"userrrr : {user['products']}")
        if user:
            # Retrieve product using URL
            for product in user['products']:
                if product['url'] == uniqueUrl:
                    return jsonify(product)
            return jsonify({'error': 'Product not found for the given URL'})
        else:
            return jsonify({'error': 'User not found'})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)})

# seasonal variation analysis
@app.route('/sva', methods=["GET"])
def interest_over_time():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        product_name = global_title
        print(f"\nproduct name {product_name}\n")
        kw_list = [product_name]
        geo_global = "IN"
        # geo_regional = "IN-IN"  # Regional level for India
        
        sva_data = {}
        regional_data = {}

        for timeframe in valid_timeframes:
            # Global Interest Over Time
            pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo=geo_global)
            interest_over_time_df = pytrends.interest_over_time().reset_index()
            interest_over_time_df['date'] = interest_over_time_df['date'].astype(str)
            sva_data[timeframe] = interest_over_time_df.rename(columns={product_name: 'score'})[['date', 'score']].to_dict(orient='records')

            # Regional Interest
            pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo=geo_global)
            regional_interest_df = pytrends.interest_by_region(resolution='CITY', inc_low_vol=True)
            regional_data[timeframe] = regional_interest_df.to_dict()

        result = {'sva': sva_data, 'regional': regional_data, 'product_name': global_title}
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

# ---------------------------------lda------------------------------------

def analyze_reviews(reviewList):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    print(reviewList)

    if len(reviewList)==0:
        return "List is Empty"
    # Combine review bodies into one string
    review_text = ' '.join([review['body'] for review in reviewList])

    # Tokenize the combined text into sentences
    review_sentences = sent_tokenize(review_text)

    # Lemmatize each sentence and remove stop words
    lemmatized_sentences = []
    for sentence in review_sentences:
        lemmatized_words = [lemmatizer.lemmatize(word) for word in sentence.split() if word.lower() not in stop_words]
        lemmatized_sentences.append(' '.join(lemmatized_words))

    # Vectorize the lemmatized sentences
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    X = vectorizer.fit_transform(lemmatized_sentences)

    # Apply NMF to find topics
    num_topics = 5
    nmf_model = NMF(n_components=num_topics, random_state=42)
    nmf_topic_matrix = nmf_model.fit_transform(X)

    feature_names = vectorizer.get_feature_names_out()
    word_freq = {}
    for topic_idx, topic in enumerate(nmf_model.components_):
        for word_idx, word_count in enumerate(topic):
            word = feature_names[word_idx]
            if word in word_freq:
                word_freq[word] += word_count
            else:
                word_freq[word] = word_count

    # Get the overall top words
    overall_top_words = sorted(word_freq, key=word_freq.get, reverse=True)[:5]

    # Find related sentences for each top word
    related_sentences = {}
    for word in overall_top_words:
        related_sentences[word] = []

    for sentence in lemmatized_sentences:
        for word in overall_top_words:
            if word in sentence:
                related_sentences[word].append(sentence)

    return related_sentences

# Define Flask endpoint
@app.route('/related_sentences', methods=['GET'])
def get_related_sentences():
    related_sentences = analyze_reviews(reviewList)
    return jsonify(related_sentences)

os.environ["HUGGINGFACEHUB_API_TOKEN"] = get_key(key_to_get="HUGGINGFACEHUB_API_KEY",dotenv_path=".env")

llm = HuggingFaceHub(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    model_kwargs={
        "max_new_tokens": 512,
        "top_k": 30,
        "temperature": 0.1,
        "repetition_penalty": 1.03,
    },
)

def chatwithbot(txt:str):
    prompt = PromptTemplate(template= "You're a helpful data assistant which can answer questions on following multiple reviews of a perticular product {reviews}",input_variables=["reviews"])

    chat_model = ChatHuggingFace(llm=llm)

    final_prompt = prompt.format(reviews=revString[0])
    user_template= PromptTemplate(template="{user_input}", input_variables=["user_input"])

    messages = [
    SystemMessage(content=final_prompt),
    HumanMessage(content=user_template.format(user_input=txt))
    ]
    res = chat_model(messages).content
    res = res[res.find("<|assistant|>")+len("<|assistant|>"):]
    return res


    

@app.route('/chat',methods=["POST"])
def chat():
    try:
        txt = request.form['text']
        res = chatwithbot(txt)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    
    app.run(debug=True)

# for now done 
