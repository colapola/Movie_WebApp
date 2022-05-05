import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


def load_df_best(df):
    """
    Create new dataframe for "top movie" task
    :param df: input dataframe
    :return: a new pandas dataframe
    """
    df_best = df[["overview", "title", "budget_musd", "revenue_musd",
              "vote_count", "vote_average", "popularity"]].copy()

    df_best["profit_musd"] = df.revenue_musd.sub(df.budget_musd)
    df_best["return"] = df.revenue_musd.div(df.budget_musd)

    df_best.columns = ["Overview", "Title", "Budget", "Revenue", "Votes",
                       "Average Rating", "Popularity", "Profit", "ROI"]
    df_best.set_index("Title", inplace=True)

    return df_best


def filter_year_range(year_range):
    """
    Filter the original data base the year range user input
    :param year_range: range of year in a tube form: (min year, max year)
    :return: filtered pandas dataframe
    """
    return df.loc[(df.release_date.dt.year > year_range[0]) & (df.release_date.dt.year < year_range[1])]


def best_worst(data, n, by, ascending=False, min_bud=0, min_votes=0):
    """
    Filter given dataframe base on user inputs.
    :param data: pandas dataframe
    :param n: number of results desire
    :param by: field uses to filter
    :param ascending: boolean, True for ascending and false for decensing
    :param min_bud: filter data with a budget threshold
    :param min_votes: filter data with a number of votes threshold
    :return: new pandas dataframe
    """
    df2 = data.loc[(data.Budget >= min_bud) & (data.Votes >= min_votes), ["Overview", by]].sort_values(by=by, ascending=ascending).head(n).copy()

    return df2.reset_index()


### Introduction

_, row0_1, _, row0_2, _ = st.columns((.1, 2.3, .1, 1.2, .1))
with row0_1:
    st.title('Movie Lover Web Application')
with row0_2:
    st.caption('A Streamlit App by Huy Nguyen')

_, row1_1, _ = st.columns((.1, 3.2, .1))
with row1_1:
    st.markdown("Welcome to Movie Lover! This is a place where you can discover tons of movie from every genres and hopefully, by spending time on this web, you could find the answer to the question: 'What movie I'm gonna watch this evening?")
    st.markdown("You can find the source code in [my GitHub repository.]()")
    st.markdown('--------------------------')
    st.title('Top Movies')
    st.write('Show top movies base on filter on the side bar.')

df = pd.read_csv('data/movies_completed.csv', parse_dates=['release_date'])
year_max = df.release_date.dt.year.max()

# sidebar

# Filter for year range
year_range = st.sidebar.slider('Select a year range you want the movies to be in:', 1950, int(year_max), (1950, 2017))
filtered_data = filter_year_range(year_range)

# Filter for top movies
df_best = load_df_best(filtered_data)
select_value_list = list(df_best.columns)[1:]

st.sidebar.write('__________________________')
st.sidebar.subheader('Filter options for you top Movies:')
selected_feature = st.sidebar.selectbox('Field to filter:', select_value_list, index=3)
n_results = st.sidebar.slider('Number of results:', 3, 10, 5)
min_vote = st.sidebar.slider('Minimum vote to consider:', 0, 100, 50)
min_bud = st.sidebar.slider('Minimum budget (millions usd) to consider:', 0, 100, 0)
show_worst = st.sidebar.selectbox('Show worst?', ['Yes', 'No'], index=1)
ascending = True if show_worst == 'Yes' else False
results = best_worst(df_best, n_results, selected_feature, min_bud=min_bud, min_votes=min_vote, ascending=ascending)

# Filter for next movies


# Display top movies
row2_1, _, row2_2, _, row2_3 = st.columns((1, .2, 1, .2, 1))
with row2_1:
    st.caption('Title')
with row2_2:
    st.caption('Overview')
with row2_3:
    st.caption(selected_feature)

for n in range(n_results):
    n_1, _, n_2, _, n_3 = st.columns((1, .2, 1, .2, 1))
    with n_1:
        st.subheader(results.Title[n])
    with n_2:
        st.markdown(results.Overview[n])
    with n_3:
        st.markdown(results[selected_feature][n])

# break
_, row3_1, _ = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown('--------------------------')
    st.title('What is your next movie?')

# Filter by genres
st.subheader('By Genres')
st.markdown('Show movie base on your favorite genres.')

gen_box = ['Animation', 'Comedy', 'Family', 'Adventure', 'Fantasy', 'Romance', 'Drama', 'Action', 'Crime', 'Thriller',
           'Horror', 'History', 'Science Fiction', 'Mystery', 'War', 'Foreign', 'Music', 'Documentary', 'Western', 'TV Movie', 'None']

rc = {'figure.figsize': (10, 5),
      'axes.facecolor': '#0e1117',
      'axes.edgecolor': '#0e1117',
      'axes.labelcolor': 'white',
      'figure.facecolor': '#0e1117',
      'patch.edgecolor': '#0e1117',
      'text.color': 'white',
      'xtick.color': 'white',
      'ytick.color': 'white',
      'grid.color': 'grey',
      'font.size': 11,
      'axes.labelsize': 16,
      'xtick.labelsize': 8,
      'ytick.labelsize': 10}

row4_1, row4_2 = st.columns(2)
with row4_1:
    gen_filter1 = st.selectbox('Select your favorite genre:', gen_box, index=20)

if gen_filter1 != 'None':
    with row4_2:
        gen_filter2 = st.selectbox('Combine with (optional)', [i for i in gen_box if i != gen_filter1], index=19)

    if gen_filter2 != 'None':
        mask_genres = df.genres.str.contains(gen_filter1) & df.genres.str.contains(gen_filter2)
    else:
        mask_genres = df.genres.str.contains(gen_filter1)

    vote_threshold = df.vote_count > 50
    df_gen = filtered_data.loc[mask_genres & vote_threshold, ["title", "vote_average"]].nlargest(10, 'vote_average')
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    sns.barplot(x="vote_average", y="title", data=df_gen, label="Highest Rating Movies By Genres", color="r")
    ax.set(xlim=(df_gen.vote_average.min()-1.5, df_gen.vote_average.max()+0.5), xlabel='Average rating', ylabel='Movies')
    st.pyplot(fig)

# Franchise vs stand alone
_, row5_1, _ = st.columns((.1, 3.2, .1))
with row5_1:
    st.markdown('--------------------------')
    st.title('Are Franchise more Successful?')

filtered_data['Franchise'] = filtered_data.belongs_to_collection.notna()
filtered_data['ROI'] = filtered_data.revenue_musd.div(filtered_data.budget_musd)
value_map = {
    False: 'Stand-alone Movies',
    True: 'Franchises'
}

column_map = {'Average Revenue (million USD)': 'revenue_musd',
              'Average Profit (million USD)': 'ROI',
             'Average Budget (million USD)': 'budget_musd',
             'Popularity': 'popularity',
             'Average Rating': 'vote_average'}

compare_field = [key for key, value in column_map.items()]
selected_field = st.selectbox('Select filed to compare:', compare_field)


rc2 = {'figure.figsize': (10, 5),
      'axes.facecolor': '#0e1117',
      'axes.edgecolor': '#0e1117',
      'axes.labelcolor': 'white',
      'figure.facecolor': '#0e1117',
      'patch.edgecolor': '#0e1117',
      'text.color': 'white',
      'xtick.color': 'white',
      'ytick.color': 'white',
      'grid.color': 'grey',
      'font.size': 11,
      'axes.labelsize': 16,
      'xtick.labelsize': 8,
      'ytick.labelsize': 10}

plt.rcParams.update(rc2)
fig1, ax1 = plt.subplots()
if selected_field == 'Number of Movies':
    df_field = filtered_data.Franchise.value_counts()
    df_field.index = df_field.index.map(value_map)
else:
    df_field = filtered_data.groupby('Franchise')[column_map[selected_field]].mean()
    df_field.index = df_field.index.map(value_map)

sns.barplot(x=df_field.index, y=df_field.values, color="r")
ax1.set(title=f"Franchises vs. Stand-alone: {selected_field}")
st.pyplot(fig1)






