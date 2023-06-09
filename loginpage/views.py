from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import spacy
from .models import AmazonProduct
from .scraper import scrape_amazon
# Create your views here.
nlp = spacy.load("en_core_web_sm")

def home(request):
    return render(request, 'loginpage/index.html')

def welcome(request):
    return render(request, 'loginpage/index1.html')

def signup(request): 
    
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']

        myuser = User.objects.create_user(email, password)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect('signin')
        
    return render(request, 'loginpage/signup.html')

def signin(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password= password)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "loginpage/index1.html", {'fname': fname})

        else:
            messages.error(request, "Wrong Credentials")
            return redirect('welcome')
            
    return render(request, 'loginpage/signin.html')

def signout(request):
    pass

def signout_user(request):
    return render(request, 'loginpage/index.html')

def namesearch(request):
    if request.method == 'GET':
        query = request.GET.get('query')  
        if query:
            pages_to_scrape = 2  # Number of pages to scrape
            products = scrape_amazon(query)
            return render(request, 'loginpage/search_results.html', {'products': products})
        
    return render(request, 'loginpage/namesearch.html')

def descsearch(request):
    if request.method == 'GET':
        query = request.GET.get('query')  
        if query:
            nlp = spacy.load('en_core_web_sm')

            
            doc = nlp(query)

            # Extract named entities
            named_entities = [(ent.text, ent.label_) for ent in doc.ents]

            # Format the retrieved data and pass it to the template
            
            return render(request, 'loginpage/search_results.html')
        return render(request, 'loginpage/descsearch.html')

def search_results(request):
    if request.method == 'GET':
        # Retrieve the necessary data for rendering the search results page
        products = AmazonProduct.objects.all()
        return render(request, 'loginpage/search_results.html', {'products': products})

    return redirect('namesearch')  # Redirect to the namesearch page if a POST request is received

    

def process_query(query):
    # Tokenization of the query using spaCy
    doc = nlp(query)
    tokens = [token.text for token in doc]
    processed_query = " ".join(tokens)
    return processed_query