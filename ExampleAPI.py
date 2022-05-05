import requests
import pandas as pd

api_key = 'api=please enter your api key'

# list of movie id that we want to request for information from theMoiveDatabase(TMDB)
movie_id = [0, 299534, 19995, 140607, 299536, 597, 135397,
            420818, 24428, 168259, 99861, 284054, 12445,
            181808, 330457, 351286, 109445, 321612, 260513]

# URl template from TMDB api document.
basic_url = 'https://api.themoviedb.org/3/movie/{}?{}'

# Sending info request and store the results in a list
json_list = []
for movie in movie_id:
    url = basic_url.format(movie, api_key)
    r = requests.get(url)
    if r.status_code != 200:
        continue
    else:
        data = r.json()
        json_list.append(data)

# Using pandas to read json files and a DataFrame
df = pd.DataFrame(json_list)

# Save dataframe to a csv
df.to_csv("movies_raw.csv", index = False)




