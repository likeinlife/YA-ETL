from typing import Generator

from common import coroutine, get_logger
from psycopg2.extensions import connection

logger = get_logger(__name__)


@coroutine
def get_genres(session: connection, next_node: Generator) -> Generator[None, list[dict], None]:
    while genre_dicts := (yield):
        cursor = session.cursor()
        logger.info('Fetching genres')
        _ids = tuple([genre.get('id') for genre in genre_dicts])
        sql = '''SELECT
                g.id,
                g.name,
                g.description,
                JSON_AGG(
                        DISTINCT jsonb_build_object(
                            'id', fw.id,
                            'title', fw.title,
                            'imdb_rating', fw.rating
                        )
                ) as film_works
                FROM content.genre g
                JOIN content.genre_film_work gfw ON g.id = gfw.genre_id
                JOIN content.film_work fw ON gfw.film_work_id = fw.id
                WHERE g.id IN %s
                GROUP BY g.id;'''
        # [ ] Фильмы не сортируются по рейтингу. Соответственно, нельзя поставить лимит.
        cursor.execute(sql, (_ids,))

        while results := cursor.fetchmany(size=100):
            next_node.send(results)
