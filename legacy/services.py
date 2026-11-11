# services.py
import requests
from urllib.parse import quote
from config import KINO_API_KEY

BASE_URL = "https://kinopoiskapiunofficial.tech/api/v2.1"

def search_kinopoisk(query: str):
    """
    Searches films, shows, and cartoons by keywords via Kinopoisk API.
    
    Args:
        query: Search term string
        
    Returns:
        List of film dictionaries matching the query
    """
    if not query or not query.strip():
        return []
        
    # URL encode the query to handle special characters
    encoded_query = quote(query.strip())
    url = f"{BASE_URL}/films/search-by-keyword?keyword={encoded_query}&page=1"

    headers = {
        "X-API-KEY": KINO_API_KEY,
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an exception for 4xx/5xx status codes
        
        data = response.json()
        films = data.get("films", [])
        
        if not films:
            print(f"No results found for: {query}")
        
        return films
        
    except requests.exceptions.Timeout:
        print("Request timed out. Please check your internet connection.")
    except requests.exceptions.ConnectionError:
        print("Connection error. Please check your internet connection.")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("Invalid API key. Please check your KINO_API_KEY in .env file.")
        elif response.status_code == 404:
            print(f"No results found for: {query}")
        elif response.status_code == 429:
            print("Too many requests. Please wait a moment before trying again.")
        else:
            print(f"HTTP Error {response.status_code}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except ValueError as e:
        print(f"JSON parsing error: {e}")
        
    return []


def get_film_details(film_id: int):
    """
    Gets detailed information about a specific film.
    
    Args:
        film_id: Kinopoisk film ID
        
    Returns:
        Film details dictionary or None if error
    """
    if not film_id:
        return None
        
    url = f"{BASE_URL}/films/{film_id}"
    
    headers = {
        "X-API-KEY": KINO_API_KEY,
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching film details: {e}")
        return None


def search_with_filters(query: str, film_type: str = None, year: int = None):
    """
    Searches with optional filters for film type and year.
    
    Args:
        query: Search term
        film_type: Type of film ('FILM', 'TV_SHOW', 'TV_SERIES', etc.)
        year: Release year
        
    Returns:
        Filtered list of film dictionaries
    """
    if not query or not query.strip():
        return []
        
    encoded_query = quote(query.strip())
    url = f"{BASE_URL}/films/search-by-keyword?keyword={encoded_query}&page=1"
    
    # Add optional filters
    if film_type:
        url += f"&type={film_type}"
    if year:
        url += f"&year={year}"
    
    headers = {
        "X-API-KEY": KINO_API_KEY,
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("films", [])
        
    except requests.exceptions.RequestException as e:
        print(f"Search error: {e}")
        return []