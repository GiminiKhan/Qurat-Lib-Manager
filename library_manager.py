import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import time
import random 
import requests 

#set page configuration 
st.set_page_config(
    page_title="Personal Library Management System",
    page_icon= "📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #111111;
            color: #f5f5f5;
        }
        .main-header {
            font-size: 3rem !important;
            color: #f5f5f5;
            font-weight: 700;
            margin-bottom: 1rem;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .sub-header {
            font-size: 1.8rem !important;
            color: #3882F6;
            font-weight: 600;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        .success-message {
            padding: 1rem;
            background-color: #ECFDF5;
            border-left: 5px solid #108981;
            border-radius: 0.375rem;
        }
        .warning-message {
            padding: 1rem;
            background-color: #FEF3C7;
            border-left: 5px solid #F59E08;
            border-radius: 0.375rem;
        }
        .book-card {
            background-color: #2C2C2C;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 5px solid #1882F6;
            transition: transform 0.3s ease;
        }
        .book-card-hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        }
        .read-badge {
            background-color: #10b981;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.875rem;
            font-weight: 600;
        }
        .unread-badge {
            background-color: #108981;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.875rem;
            font-weight: 600;
        }
        .action-button {
            margin-right: 0.5rem;
        }
        .stButton>button {
            border-radius: 0.375rem;
        }
    </style>
""", unsafe_allow_html=True)

def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None
    
if 'library' not in st.session_state:
    st.session_state.library = []
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'book_added' not in st.session_state:
    st.session_state.book_added = False 
if 'book_removed' not in st.session_state:
    st.session_state.book_removed = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = "library"

#load library
def load_library():
    try:
        if os.path.exists('library.json'):
            with open('library.json', 'r') as file:
                st.session_state.library = json.load(file)
                return True 
        return False
    except Exception as e:
        st.error(f"Error loading library: {e}")
        return False

def save_library():
    try:
        with open('library.json', 'w') as file:
            json.dump(st.session_state.library, file)
            return True
    except Exception as e:
        st.error(f"Error saving library: {e}")
        return False

def add_book(title, author, publication_year, genre, read_status):
    book = {
        'title': title,
        'author': author,
        'publication_year': publication_year,
        'genre': genre,
        'read_status': read_status,
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.5)

def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True
        return True
    return False 

def search_books(search_term, search_by):
    search_term = search_term.lower()
    results = []
    for book in st.session_state.library:
        if search_by == "Title" and search_term in book['title'].lower():
            results.append(book)
        elif search_by == "Author" and search_term in book['author'].lower():
            results.append(book)
        elif search_by == "Genre" and search_term in book['genre'].lower():
            results.append(book)
    st.session_state.search_results = results

# Initialize library
load_library()

# Sidebar setup for navigation
st.sidebar.markdown("<h1 style='text-align: center;'> Navigation</h1>", unsafe_allow_html=True)
nav_options = st.sidebar.radio(
    "Choose an option:",
    ["View Library", "Add Book", "Search Books", "Library Statistics"]
)

if nav_options == "View Library":
    st.session_state.current_view = 'library'
elif nav_options == "Add Book":
    st.session_state.current_view = 'add'
elif nav_options == 'Search Books':
    st.session_state.current_view = 'search'
elif nav_options == 'Library Statistics':
    st.session_state.current_view = 'stats'

# Main content header
st.markdown("<h1 class='main-header'> Personal Library Manager 📚 </h1>", unsafe_allow_html=True)

# Add book form
if st.session_state.current_view == "add":
    st.markdown("<h2 class='sub-header'> Add a new book</h2>", unsafe_allow_html=True)
    with st.form(key='add_book_form'):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Book Title", max_chars=100)
            author = st.text_input("Author", max_chars=100)
            publication_year = st.number_input("Publication year", min_value=1000, max_value=datetime.now().year, step=1, value=2023)
        with col2:
            genre = st.selectbox("Genre", [
                "Fiction", "Non-Fiction", "Science", "Technology", "Fantasy", "Art", "Religion", "Historic"
            ])
            read_status = st.radio("Read Status", ["Read", "Unread"], horizontal=True)
            read_bool = read_status == "Read"
        submit_button = st.form_submit_button(label="Add Book")
        if submit_button and title and author:
            add_book(title, author, publication_year, genre, read_bool)

    if st.session_state.book_added:
        st.markdown("<div class='success-message'> Book added successfully! 🎉</div>", unsafe_allow_html=True)
        st.balloons()
        st.session_state.book_added = False

# View library
elif st.session_state.current_view == "library":
    st.markdown("<h2 class = 'sub-header'> Your Library </h2>", unsafe_allow_html=True)
    if not st.session_state.library:
        st.markdown("<div class = 'warning-message'> Your library is empty. Add some books to get started! 😔</div>", unsafe_allow_html=True)
    else:
        cols = st.columns(2)
        for i, book in enumerate(st.session_state.library):
            with cols[i % 2]:
                st.markdown(f"""<div class = 'book-card'>
                            <h3>{book['title']}</h3>
                            <p><strong>Author:</strong>{book['author']}</p>
                            <p><strong>Publication Year:</strong> {book['publication_year']}</p>
                            <p><strong>Genre:</strong>{book['genre']}</p>
                            <p><span class='{"read-badge" if book["read_status"] else "unread-badge"}'>{
                            "Read" if book["read_status"] else "Unread"
                            }</span></p>
                            </div>
                """, unsafe_allow_html=True)

# Search books
elif st.session_state.current_view == "search":
    st.markdown("<h2 class='sub-header'> Search Books </h2>", unsafe_allow_html=True)
    search_term = st.text_input("Enter search term")
    search_by = st.selectbox("Search by", ["Title", "Author", "Genre"])
    if st.button("Search"):
        search_books(search_term, search_by)
    
    if st.session_state.search_results:
        for book in st.session_state.search_results:
            st.markdown(f"📖 **{book['title']}** by {book['author']} (Genre: {book['genre']}, Published: {book['publication

