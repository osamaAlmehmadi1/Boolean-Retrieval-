from flask import Flask,render_template,redirect,url_for,request
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os
import time

# nltk.download("punkt")
# nltk.download("stopwords")

def preprocess_document(document):
    tokens=word_tokenize(document)
    token = [token.lower() for token in tokens if token.isalpha()]
    stop_words= set(stopwords.words("english"))
    tokens=[token for token in tokens if token not in stop_words]
    stemmer = PorterStemmer()
    tokens= [stemmer.stem(token) for token in tokens]
    return tokens
  
def build_inverted_index(documents):
    inverted_index={}
    for doc_id,document in enumerate(documents):
        terms=preprocess_document(document)
        for term in terms:
            if term not in inverted_index:
                inverted_index[term]=set()
            inverted_index[term].add(doc_id)
           
    return inverted_index
def boolean_query(query,inverted_index,documents):
    query_terms= preprocess_document(query)
    result=None
    results=[]
    for term in query_terms:
        if term in inverted_index:
            term_docs= inverted_index[term]
            if result is None:
                 results=term_docs
                 
            else:
                results=result.intersection(term_docs)
    return results


documents=[]

folder_path = r'C:\Users\osama\OneDrive\سطح المكتب\المواد\استرجاع المعلومات\Boolean_Retrieval\Boolean_Retrieval\Documents'



def get_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        return text


for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        if file_name.endswith('.txt'):
            file_path = os.path.join(root, file_name)
            text = get_text(file_path)
            documents.append(text)



        
search_app= Flask(__name__)


@search_app.route("/")
def search_page():
    return render_template("search.html")

@search_app.route("/", methods=["POST"])
def result_page():
    start_time=time.time()
    query = request.form["query"]
    inverted_index = build_inverted_index(documents)
    results = boolean_query(query, inverted_index, documents)
    end_time=time.time()
    execution_time=end_time-start_time
    if results is None:
      return render_template("result.html", query=query, matching_documents="No Matching Documents")
    
    else:
      matching_documents = [documents[doc_id] for doc_id in results]
      return render_template("result.html", query=query, matching_documents=matching_documents,effectiveness=len(matching_documents),execution_time=round(execution_time,2))
        

if __name__=="__main__":
    search_app.run(debug=True)

