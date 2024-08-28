import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [books, setBooks] = useState([]);
  const [selectedBook, setSelectedBook] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/books')
      .then(response => {
      console.log('Fetched books:', response.data);
      setBooks(response.data);
      })
      .catch(error => {
      console.error('Error fetching books:', error);
      setError(`Failed to fetch books. Error: ${error.message}`);
      });
  }, []);

  const handleBookClick = (book) => {
    setSelectedBook(book);
  };

  const handleBackClick = () => {
    setSelectedBook(null);
  };

  const getRandomHue = () => Math.floor(Math.random() * 360);

  if (error) {
    return (
      <div className="App">
        <h1>Library Book Reading App</h1>
        <p className="error">{error}</p>
      </div>
    );
  }

  return (
    <div className="App">
      <h1>Mock Reader App</h1>
      {selectedBook ? (
        <div className="book-content">
          <button onClick={handleBackClick}>Back to Library</button>
          <h2>{selectedBook.title}</h2>
          <p>{selectedBook.content}</p>
        </div>
      ) : (
        <div className="book-list">
          {books.length === 0 ? (
            <p>Loading books...</p>
          ) : (
            books.map(book => (
              <div
                key={book.id}
                className="book-icon"
                style={{ backgroundColor: `hsl(${getRandomHue()}, 70%, 80%)` }}
                onClick={() => handleBookClick(book)}
              >
                <h3>{book.title}</h3>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default App;
