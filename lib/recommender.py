import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel


class Recommender:
    def __init__(self, movies_path, credits_path):
        self.movies_path = movies_path
        self.credits_path = credits_path
        self.sig = None
        self.indices = None
        self.movie_database = None

        self._load()

    def _get_movie_data(self):
        credits = pd.read_csv(self.credits_path)
        movies = pd.read_csv(self.movies_path)

        credits_renamed = credits.rename(index=str, columns={"movie_id": "id"})
        movies_merged = movies.merge(credits_renamed, on='id')
        for index, row in movies_merged.iterrows():
            movies_merged.loc[index, 'original_title_lowercase'] = row['original_title'].lower()

        return movies_merged.drop(columns=['homepage', 'title_x', 'title_y', 'status', 'production_countries'])

    def _load(self):
        self.movie_database = self._get_movie_data()

        tfv = TfidfVectorizer(min_df=3, max_features=None,
                              strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                              ngram_range=(1, 3), use_idf=1, smooth_idf=1, sublinear_tf=1,
                              stop_words='english')

        self.movie_database['overview'] = self.movie_database['overview'].fillna('')
        tfv_matrix = tfv.fit_transform(self.movie_database['overview'])

        self.sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
        self.indices = pd.Series(self.movie_database.index, index=self.movie_database['original_title_lowercase']).drop_duplicates()

    def get_proposals(self, title):
        if title not in self.indices:
            return None
        idx = self.indices[title]

        sig_scores = list(enumerate(self.sig[idx]))
        sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
        sig_scores = sig_scores[1:7]

        movie_indices = [i[0] for i in sig_scores]

        return self.movie_database['original_title'].iloc[movie_indices].tolist()
