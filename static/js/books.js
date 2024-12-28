document.addEventListener('DOMContentLoaded', () => {
    const booksData = {
        community: [],
        popular: [],
        recentAdd: []
    };

    function createBookElement(book) {
        const bookDiv = document.createElement('div');
        bookDiv.className = 'book';

        const title = document.createElement('h3');
        title.textContent = book.TenSach;
        bookDiv.appendChild(title);

        const author = document.createElement('p');
        author.textContent = `Author: ${book.TacGia}`;
        bookDiv.appendChild(author);

        const status = document.createElement('p');
        status.textContent = book.TinhTrang;
        bookDiv.appendChild(status);
        const button = document.createElement('button');
        button.textContent = 'Borrow';
        bookDiv.appendChild(button);

        return bookDiv;
    }

    function populateColumn(columnId, books) {
        const column = document.querySelector(`.column.${columnId}`);
        const bookElements = column.querySelectorAll('.book');
        bookElements.forEach(bookElement => bookElement.remove());        
        // column.innerHTML = ''; // Clear existing content
        // column.appendChild(title);
        books.forEach(book => {
            const bookElement = createBookElement(book);
            column.appendChild(bookElement);
        });
    }

    async function fetchBooks() {
        try {
            const response = await fetch('/api/books/community');
            const data = await response.json();
            booksData.community = data;
        } catch (error) {
            console.log(error);
        }

        try {
            const response = await fetch('/api/books/popular');
            const data = await response.json();
            booksData.popular = data;
        } catch (error) {
            console.log(error);
        }

        try {
            const response = await fetch('/api/books/recentAdd');
            const data = await response.json();
            booksData.recentAdd = data;
        } catch (error) {
            console.log(error);
        }

        populateColumn('community', booksData.community);
        populateColumn('popular', booksData.popular);
        populateColumn('recentAdd', booksData.recentAdd);
    }

    fetchBooks();

    function searchBooks(query) {
        const allBooks = [...booksData.community, ...booksData.popular, ...booksData.recentAdd];
        return allBooks.filter(book => book.title.toLowerCase().includes(query.toLowerCase()));
    }

    document.querySelector('.search-container button').addEventListener('click', () => {
        const query = document.querySelector('.search-container input[type=text]').value;
        const results = searchBooks(query);
        const resultContainer = document.querySelector('.search-results');
        resultContainer.innerHTML = '';

        if (results.length > 0) {
            results.forEach(book => {
                const bookElement = createBookElement(book);
                resultContainer.appendChild(bookElement);
            });
        } else {
            resultContainer.innerHTML = '<p>No books found in the library.</p>';
        }
    });
});


