from .base import ElasticBaseModel


class InnerFilmWork(ElasticBaseModel):
    title: str
    imdb_rating: float
    roles: list[str]

    def to_elastic(self) -> dict:
        return {
            'id': str(self.id),
            'title': self.title,
            'imdb_rating': self.imdb_rating,
            'roles': self.roles,
        }


class Person(ElasticBaseModel):
    name: str
    movies: list[InnerFilmWork]

    def to_elastic(self) -> dict:
        return {
            'id': str(self.id),
            'name': self.name,
            'movies': [movie.to_elastic() for movie in self.movies],
        }
