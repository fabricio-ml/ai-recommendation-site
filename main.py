# Import necessary libraries
from fastapi import FastAPI, Form  # FastAPI framework and Form for handling form data
from fastapi.responses import HTMLResponse  # For returning HTML content
from typing import List  # For type hinting
import numpy as np  # For numerical operations
from sklearn.feature_extraction.text import TfidfVectorizer  # For text vectorization
from sklearn.metrics.pairwise import cosine_similarity  # For calculating similarity
from fuzzywuzzy import process  # For fuzzy string matching

# Initialize the FastAPI application
app = FastAPI()

# Define the database of music artists and their descriptions
music_db = {
    "The Beatles": "Iconic British rock band known for their innovative sound and cultural impact.",
    "Led Zeppelin": "Influential hard rock band with blues-inspired riffs and powerful vocals.",
    "Queen": "Legendary rock band known for their theatrical style and diverse musical palette.",
    "Pink Floyd": "Progressive rock band famous for their philosophical lyrics and concept albums.",
    "David Bowie": "Innovative rock artist known for his musical reinvention and visual presentation.",
    "Radiohead": "Alternative rock band praised for their experimental sound and emotional depth.",
    "Nirvana": "Grunge pioneers who brought alternative rock to the mainstream in the early 1990s.",
    "Bob Dylan": "Influential singer-songwriter known for his poetic, often political lyrics.",
    "Michael Jackson": "King of Pop, known for his innovative dance moves and catchy pop tunes.",
    "Madonna": "Pop icon known for her constant reinvention and provocative style.",
    "Prince": "Versatile musician known for his flamboyant style and wide vocal range.",
    "Taylor Swift": "Pop and country singer-songwriter known for her narrative songs and evolution of style.",
    "Beyoncé": "R&B and pop superstar known for her powerful vocals and stage presence.",
    "Adele": "Soul-influenced pop singer known for her emotive ballads and powerful voice.",
    "Ed Sheeran": "Pop singer-songwriter known for his heartfelt lyrics and acoustic-driven songs.",
    "Eminem": "Controversial and skilled rapper known for his complex rhyme schemes and rapid delivery.",
    "Kendrick Lamar": "Critically acclaimed rapper known for his storytelling and socially conscious lyrics.",
    "Drake": "Chart-topping rapper and singer known for his melodic style and emotional lyrics.",
    "Kanye West": "Influential and controversial hip-hop artist known for his innovative production and ego.",
    "Jay-Z": "Legendary rapper known for his wordplay and business acumen.",
    "Daft Punk": "Electronic music duo known for their robot personas and influential dance tracks.",
    "The Chemical Brothers": "Electronic music duo known for their big beat sound and psychedelic elements.",
    "Aphex Twin": "Innovative electronic musician known for his experimental and often complex compositions.",
    "Skrillex": "EDM producer and DJ who popularized dubstep in the mainstream.",
    "Deadmau5": "Progressive house producer known for his iconic mouse helmet and technical productions.",
    "Mozart": "Classical composer of the Classical era, known for his prolific and influential output.",
    "Beethoven": "Revolutionary composer bridging the Classical and Romantic eras, known for his symphonies.",
    "Bach": "Baroque composer known for his technical command and intellectual depth in his compositions.",
    "Chopin": "Romantic era pianist and composer known for his expressive piano compositions.",
    "Tchaikovsky": "Romantic era Russian composer known for his emotional symphonies and ballets.",
    "Miles Davis": "Innovative jazz trumpeter who played a crucial role in the development of jazz.",
    "Louis Armstrong": "Influential jazz trumpeter and singer known for his distinctive voice and improvisation.",
    "John Coltrane": "Revolutionary jazz saxophonist known for his complex, spiritual approach to music.",
    "Ella Fitzgerald": "Jazz singer known as the 'First Lady of Song' for her pure tone and vocal improvisation.",
    "Frank Sinatra": "Iconic singer and actor known for his distinctive voice and interpretation of the American songbook.",
    "Bob Marley": "Reggae icon who brought Jamaican music to an international audience.",
    "Fela Kuti": "Pioneer of Afrobeat music, known for his musical innovation and political activism.",
    "Ravi Shankar": "Renowned Indian sitar player who popularized classical Indian music in the West.",
    "Youssou N'Dour": "Senegalese singer known for his distinctive voice and fusion of traditional African music with pop.",
    "Buena Vista Social Club": "Cuban ensemble that revived interest in traditional Cuban music worldwide.",
    "The Rolling Stones": "Legendary British rock band known for their bluesy sound and longevity.",
    "U2": "Irish rock band known for their anthemic sound and socially conscious lyrics.",
    "Coldplay": "British rock band known for their melodic pop rock and emotional ballads.",
    "Fleetwood Mac": "Rock band known for their interpersonal drama and classic album 'Rumours'.",
    "Bruce Springsteen": "American rock singer-songwriter known as 'The Boss' for his poetic lyrics about working-class life.",
    "Elton John": "British singer, pianist, and composer known for his flamboyant style and numerous hit songs.",
    "Whitney Houston": "Powerhouse vocalist known for her extraordinary range and pop-soul crossover hits.",
    "Marvin Gaye": "Soul and R&B singer known for his smooth voice and socially conscious music.",
    "Stevie Wonder": "Blind musical prodigy known for his innovative recordings and virtuosic instrumental abilities.",
    "Aretha Franklin": "The 'Queen of Soul', known for her powerful voice and influential R&B recordings.",
    "James Brown": "The 'Godfather of Soul', known for his dynamic dancing and influential funk music.",
    "Elvis Presley": "The 'King of Rock and Roll', who popularized rockabilly and became a cultural icon.",
    "Johnny Cash": "Influential country singer-songwriter known as the 'Man in Black' for his distinctive bass-baritone voice.",
    "Dolly Parton": "Country music icon known for her distinctive soprano, songwriting, and larger-than-life persona.",
    "Willie Nelson": "Country music outlaw known for his distinctive voice and relaxed, jazzy singing style.",
    "Tupac Shakur": "Influential rapper known for his poetic lyrics addressing social issues.",
    "The Notorious B.I.G.": "East Coast rapper known for his fluid flow and vivid, often humorous lyrics.",
    "Dr. Dre": "Rapper and producer who played a significant role in popularizing West Coast G-funk.",
    "Snoop Dogg": "West Coast rapper known for his laid-back delivery and iconic persona.",
    "Björk": "Icelandic singer-songwriter known for her eclectic style and avant-garde artistry.",
    "Kraftwerk": "Pioneers of electronic music, known for their innovative use of technology.",
    "The Prodigy": "Electronic dance music group known for their high-energy performances and fusion of various styles.",
    "Massive Attack": "Trip hop pioneers known for their dark, atmospheric sound.",
    "Portishead": "Trip hop band known for their haunting melodies and innovative production techniques.",
    "Nina Simone": "Jazz singer and civil rights activist known for her powerful voice and emotional intensity.",
    "Ray Charles": "Pioneer of soul music, known for blending blues, jazz, and gospel styles.",
    "B.B. King": "Blues guitarist and singer known as the 'King of the Blues' for his expressive playing style.",
    "Chuck Berry": "Rock and roll pioneer known for his showmanship and development of guitar techniques.",
    "Jimi Hendrix": "Revolutionary rock guitarist known for his innovative playing and psychedelic sound.",
    "Eric Clapton": "Influential blues and rock guitarist known as 'Slowhand' for his virtuosic playing.",
    "Joni Mitchell": "Canadian singer-songwriter known for her poetic lyrics and innovative guitar tunings.",
    "Carole King": "Influential singer-songwriter known for her introspective and confessional style.",
    "Simon & Garfunkel": "Folk rock duo known for their close harmonies and poetic lyrics.",
    "The Beach Boys": "American rock band known for their intricate vocal harmonies and early surf rock sound.",
    "Buddy Holly": "Early rock and roll star who influenced countless musicians despite his short career.",
    "Patsy Cline": "Country and pop music singer known for her rich tone and emotional delivery.",
    "Hank Williams": "Legendary country singer-songwriter known for his poetic, melancholy lyrics.",
    "Muddy Waters": "Influential blues musician known as the 'father of modern Chicago blues'.",
    "Robert Johnson": "Delta blues singer and guitarist whose mysterious life and death became legendary.",
    "Billie Holiday": "Jazz singer known for her distinctive voice and ability to convey deep emotion.",
    "Duke Ellington": "Jazz composer, pianist, and bandleader who played a pivotal role in the genre's development.",
    "Charlie Parker": "Revolutionary jazz saxophonist and pioneer of bebop.",
    "Thelonious Monk": "Jazz pianist and composer known for his unique improvisational style.",
    "Janis Joplin": "Rock singer known for her powerful, blues-inspired vocals and electric stage presence.",
    "Amy Winehouse": "British singer-songwriter known for her deep, expressive contralto vocals and eclectic mix of musical genres.",
    "Kurt Cobain": "Nirvana frontman who became an icon of alternative rock and grunge music.",
    "Freddie Mercury": "Queen's lead vocalist, known for his four-octave vocal range and flamboyant stage persona.",
    "John Lennon": "Beatles co-founder known for his songwriting partnership with Paul McCartney and later solo career.",
    "Paul McCartney": "Beatles bassist and co-songwriter who went on to have a successful solo career.",
    "David Gilmour": "Pink Floyd guitarist known for his atmospheric, effects-laden playing style.",
    "Jimmy Page": "Led Zeppelin guitarist known for his innovative production techniques and diverse playing styles.",
    "Mick Jagger": "Rolling Stones frontman known for his energetic performances and distinctive voice.",
    "Sting": "Lead singer of The Police who went on to have a successful solo career blending rock, jazz, and world music.",
    "Peter Gabriel": "Genesis frontman turned solo artist known for his innovative music videos and world music influences.",
    "Kate Bush": "British singer-songwriter known for her wide vocal range and theatrical, literary-inspired songs.",
    "Lauryn Hill": "Singer, rapper, and songwriter known for her work with the Fugees and influential solo album.",
    "Erykah Badu": "Neo-soul singer known for her eccentric style and introspective lyrics.",
    "D'Angelo": "R&B and neo-soul singer known for his smooth vocals and funk-influenced sound.",
    "Fiona Apple": "Singer-songwriter known for her piano-driven songs and intense, confessional lyrics.",
    "Tori Amos": "Singer-songwriter and pianist known for her emotionally intense songs and unique vocal style.",
    "Jeff Buckley": "Singer-songwriter known for his ethereal voice and eclectic style, despite his short career.",
    "Nick Drake": "English singer-songwriter known for his intricate fingerpicking guitar style and haunting lyrics.",
    "Leonard Cohen": "Canadian singer-songwriter and poet known for his deep, resonant voice and poetic lyrics.",
    "Tom Waits": "Singer-songwriter known for his distinctive gravelly voice and experimental music incorporating diverse genres."
}

# Extract artist names and descriptions from the database
artist_names = list(music_db.keys())  # Create a list of all artist names
artist_descriptions = list(music_db.values())  # Create a list of all artist descriptions

# Initialize and fit the TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')  # Create a TF-IDF vectorizer, removing common English words
tfidf_matrix = tfidf_vectorizer.fit_transform(artist_descriptions)  # Transform the descriptions into TF-IDF feature vectors

# Calculate the cosine similarity matrix
similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)  # Compute similarity between all pairs of artists

# Define the root route, returning an HTML form
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <body>
            <h1>AI-Powered Music Recommendation App</h1>
            <form action="/recommend" method="post">
                <label for="artist">Favorite Artist:</label>
                <input type="text" id="artist" name="artist"><br><br>
                <input type="submit" value="Get AI Recommendations">
            </form>
        </body>
    </html>
    """  # Return a simple HTML form for user input

# Define the recommendation route
@app.post("/recommend")
async def recommend(artist: str = Form(...)):  # Receive the artist name from the form
    # Use fuzzy matching to find the closest artist name
    closest_match, score = process.extractOne(artist, artist_names)  # Find the best match for the input artist name
    
    # If the match score is less than 70, consider it not found
    if score < 70:
        return {"error": f"Artist not found. Did you mean {closest_match}?"}  # Return an error message with a suggestion
    
    # Get the index of the matched artist
    artist_index = artist_names.index(closest_match)  # Find the index of the matched artist in our list
    
    # Get similarity scores for the matched artist
    similarity_scores = list(enumerate(similarity_matrix[artist_index]))  # Get similarity scores for the matched artist
    
    # Sort the similarity scores in descending order
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)  # Sort artists by similarity
    
    # Get top 5 similar artists (excluding the input artist)
    top_similar = similarity_scores[1:6]  # Select the top 5 most similar artists (excluding the input artist)
    
    # Prepare the recommendations list
    recommendations = [
        {
            "name": artist_names[i[0]],  # Get the name of the recommended artist
            "description": music_db[artist_names[i[0]]],  # Get the description of the recommended artist
            "similarity_score": round(i[1] * 100, 2)  # Calculate and round the similarity score
        } for i in top_similar
    ]
    
    # Return the input artist details and recommendations
    return {
        "input_artist": closest_match,  # Return the name of the input artist (or closest match)
        "input_artist_description": music_db[closest_match],  # Return the description of the input artist
        "recommendations": recommendations  # Return the list of recommendations
    }

# Run the application if this script is the main program
if __name__ == "__main__":
    import uvicorn  # Import the ASGI server we'll use to run the app
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run the app on localhost, port 8000
