import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

positive_books_and_genres = {
    'Марс наш!':'Фантастика',
    'Солярис':'Фантастика',
    'Бронзовая птица':'Детективы',
    'Том и Джерри: Классические комиксы':'Мультфильмы',
    'Дядя Фёдор, пёс и кот':'Комедии',
    'Оно':'Ужасы'
}

positive_books = list(positive_books_and_genres.keys())
positive_genres = list(positive_books_and_genres.values())

class TestBooksCollector:

    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Марс наш!')
        collector.add_new_book('Бронзовая птица')

        assert len(collector.get_books_genre()) == 2

    def test_add_new_book_over_forty_one_symbols_name(self, collector):
        collector.add_new_book('Название книги на точно сорок один символ')
        assert 'Название книги на точно сорок один символ' not in collector.get_books_genre()
    
    def test_get_book_genre_existing_genre(self, collector):
        collector.add_new_book('Марс наш!')
        collector.set_book_genre('Марс наш!', 'Фантастика')
        assert collector.get_book_genre('Марс наш!') == 'Фантастика'

    def test_set_book_genre_non_existing_genre(self, collector):
        collector.add_new_book('Марс наш!')
        collector.set_book_genre('Марс наш!', 'Попаданцы')
        assert collector.get_book_genre('Марс наш!') == ''

    @pytest.mark.parametrize("books", [positive_books_and_genres])    
    def test_get_books_with_specific_genre_sci_fi(self, collector, books):
        for name in books:
            collector.add_new_book(name)
        for name, genre in positive_books_and_genres.items():
            collector.set_book_genre(name, genre)
        assert len(collector.get_books_with_specific_genre('Фантастика')) == 2

    @pytest.mark.parametrize("books", [positive_books_and_genres])
    def test_get_books_genre_full_added_books_dictionary(self, collector, books):
        for name in books:
            collector.add_new_book(name)
        for name, genre in positive_books_and_genres.items():
            collector.set_book_genre(name, genre)
        assert collector.get_books_genre() == {
        'Марс наш!':'Фантастика',
        'Солярис':'Фантастика',
        'Бронзовая птица':'Детективы',
        'Том и Джерри: Классические комиксы':'Мультфильмы',
        'Дядя Фёдор, пёс и кот':'Комедии',
        'Оно':'Ужасы'
        }

    @pytest.mark.parametrize("books", [positive_books_and_genres])
    def test_get_books_for_children_age_restricted_genres_filtered(self, collector, books):
        for name in books:
            collector.add_new_book(name)
        for name, genre in positive_books_and_genres.items():
            collector.set_book_genre(name, genre)
        assert collector.get_books_for_children() == ['Марс наш!', 'Солярис', 'Том и Джерри: Классические комиксы', 'Дядя Фёдор, пёс и кот']

    def test_add_book_in_favorites_no_duplicates(self, collector):
        collector.add_new_book('Солярис')
        collector.add_book_in_favorites('Солярис')
        collector.add_book_in_favorites('Солярис')
        assert collector.get_list_of_favorites_books() == ['Солярис']

    def test_delete_book_from_favorites_book_exists_in_favorites(self, collector):
        collector.add_new_book('Солярис')
        collector.add_book_in_favorites('Солярис')
        collector.delete_book_from_favorites('Солярис')
        assert collector.get_list_of_favorites_books() == []
    
    @pytest.mark.parametrize("books", [positive_books_and_genres])
    def test_get_list_of_favorites_books_returns_current_state(self, collector, books):
        for name in books:
            collector.add_new_book(name)
        collector.add_book_in_favorites('Солярис')
        collector.add_book_in_favorites('Дядя Фёдор, пёс и кот')
        collector.delete_book_from_favorites('Солярис')
        assert collector.get_list_of_favorites_books() == ['Дядя Фёдор, пёс и кот']