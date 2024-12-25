import random
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS

# Set up the Flask app
app = Flask(__name__)
CORS(app)

# Function to load roasts from the file and shuffle them
def load_and_shuffle_roasts():
    with open('roasts.txt', 'r') as file:
        roasts = file.readlines()
    random.shuffle(roasts)  # Shuffle the list of roasts to mix them
    return roasts

# Function to fetch a random roast from the shuffled list
def fetch_roast(username):
    roasts = load_and_shuffle_roasts()
    return f"{username}, {roasts[0].strip()}"  # Return the first shuffled roast

# Function to scrape TryHackMe user data
def scrape_tryhackme_user_data(username):
    tryhackme_url = f"https://tryhackme.com/p/{username}"  # User profile URL
    response = requests.get(tryhackme_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract user points from profile page
        points_section = soup.find('div', {'class': 'profile-points'})
        points = points_section.get_text(strip=True) if points_section else '0'

        # Extract user badges from profile page
        badges = [badge.get_text(strip=True) for badge in soup.find_all('span', {'class': 'badge-name'})]

        # Extract user skills from profile page
        skills = [skill.get_text(strip=True) for skill in soup.find_all('span', {'class': 'skill-name'})]

        return {'points': points, 'badges': badges, 'skills': skills}
    else:
        return None  # If the profile page is not found or the request fails

# Function to interact with Gemini API to generate content
def generate_gemini_content(prompt):
    gemini_api_key = ""  # Replace with your Gemini API key
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + gemini_api_key
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        try:
            result = response.json()
            print("Full Response from Gemini API:", result)  # Print the entire response for debugging

            # Extract the roast from the response based on the updated structure
            roast = result['candidates'][0]['content']['parts'][0]['text']
            return roast
        except ValueError:
            return "Error: Could not parse response from Gemini API."
    else:
        return f"Error: {response.status_code} - {response.text}"

# API route to get a roast using Gemini API and scraped TryHackMe data
@app.route('/roast', methods=['POST'])
def roast():
    data = request.json
    username = data.get("username", "Anonymous")
    
    # Scrape TryHackMe user data
    tryhackme_data = scrape_tryhackme_user_data(username)
    
    if tryhackme_data:
        points = tryhackme_data.get('points', '0')
        badges = ", ".join(tryhackme_data.get('badges', []))
        skills = ", ".join(tryhackme_data.get('skills', []))
        
        # Print the scraped TryHackMe data for debugging
        print(f"Scraped TryHackMe Data for {username}:")
        print(f"Points: {points}")
        print(f"Badges: {badges}")
        print(f"Skills: {skills}")

        # Create a roast message based on scraped data
        roast_message = f"{username}, you have {points} points, these skills: {skills}, and badges: {badges}. But, your hacking skills are so basic, even a noob VM could outsmart you!"
    else:
        # If no data is found, fall back to a generic roast
        roast_message = fetch_roast(username)
    
    # Create a prompt for Gemini API with the username and roast
    prompt = f"You are a witty bot. Roast the user '{username}' humorously. Here's a roast: {roast_message}"

    # Generate content using Gemini AI
    gemini_roast = generate_gemini_content(prompt)
    
    return jsonify({"roast": gemini_roast})

if __name__ == "__main__":
    app.run(debug=True)
