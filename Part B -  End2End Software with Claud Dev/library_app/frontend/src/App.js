import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function LoginForm({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/login', { username, password });
      if (response.data.success) {
        onLogin();
      } else {
        setError('Invalid credentials');
      }
    } catch (error) {
      setError('Login failed. Please try again.');
    }
  };

  return (
    <form className="login-form" onSubmit={handleSubmit}>
      <h2>Login</h2>
      {error && <p className="error-message">{error}</p>}
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit">Login</button>
    </form>
  );
}

function Navigation({ onSignOut, onSearch }) {
  return (
    <nav className="navigation">
      <div className="nav-logo">Mock Reader App</div>
      <div className="search-container">
        <input
          type="text"
          placeholder="Search books..."
          onChange={(e) => onSearch(e.target.value)}
          className="search-input"
        />
      </div>
      <button className="sign-out-button" onClick={onSignOut}>Sign Out</button>
    </nav>
  );
}

function App() {
  const [books, setBooks] = useState([]);
  const [filteredBooks, setFilteredBooks] = useState([]);
  const [selectedBook, setSelectedBook] = useState(null);
  const [error, setError] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    if (isLoggedIn) {
      fetchBooks();
    }
  }, [isLoggedIn]);

  useEffect(() => {
    const filtered = books.filter(book =>
      book.title.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredBooks(filtered);
  }, [searchTerm, books]);

  const fetchBooks = () => {
    axios.get('http://127.0.0.1:5000/api/books')
      .then(response => {
        console.log('Fetched books:', response.data);
        setBooks(response.data);
      })
      .catch(error => {
        console.error('Error fetching books:', error);
        setError(`Failed to fetch books. Error: ${error.message}`);
      });
  };

  const handleBookClick = (book) => {
    setSelectedBook(book);
  };

  const handleBackClick = () => {
    setSelectedBook(null);
  };

  const getRandomHue = () => Math.floor(Math.random() * 360);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleSignOut = () => {
    setIsLoggedIn(false);
    setSelectedBook(null);
    setBooks([]);
    setSearchTerm('');
  };

  const handleSearch = (term) => {
    setSearchTerm(term);
  };

  if (error) {
    return (
      <div className="App">
        <h1>Library Book Reading App</h1>
        <p className="error">{error}</p>
      </div>
    );
  }

  if (!isLoggedIn) {
    return (
      <div className="App">
        <h1>Mock Reader App</h1>
        <LoginForm onLogin={handleLogin} />
      </div>
    );
  }

  return (
    <div className="App">
      <Navigation onSignOut={handleSignOut} onSearch={handleSearch} />
      <main className="main-content">
        {selectedBook ? (
          <div className="book-content">
            <button onClick={handleBackClick}>Back to Library</button>
            <h2>{selectedBook.title}</h2>
            <p>{selectedBook.content}</p>
          </div>
        ) : (
          <div className="book-list">
            <h2>Library Books</h2>
            {filteredBooks.length === 0 ? (
              <p>No books found</p>
            ) : (
              filteredBooks.map(book => (
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
      </main>
    </div>
  );
}

export default App;
