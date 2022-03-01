import React from 'react'
import logo from './logo.svg';
import './App.css';
import AuthorList from './components/AuthorList.js'
import BookList from './components/BookList.js'
import AuthorBookList from './components/AuthorBookList.js'
import axios from 'axios'
import {HashRouter, BrowserRouter, Route, Routes, Link, useLocation, Navigate} from 'react-router-dom'


const NotFound = () => {
    let location = useLocation()
    return (
        <div> Page {location.pathname} not found </div>
    )
}


class App extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            'authors': [],
            'books': []
        }
    }

    componentDidMount() {
        axios
            .get('http://127.0.0.1:8000/api/authors/')
            .then(response => {
                const authors = response.data

                this.setState({
                    'authors': authors
                })
            })
            .catch(error => console.log(error))
        axios
            .get('http://127.0.0.1:8000/api/books/')
            .then(response => {
                const books = response.data

                this.setState({
                    'books': books
                })
            })
            .catch(error => console.log(error))
    }
//                        http://localhost:3000/#/books

    render () {
        return (
            <div>
                <BrowserRouter>
                    <nav>
                        <li><Link to='/'>Authors</Link></li>
                        <li><Link to='/books'>Books</Link></li>
                    </nav>
                    <Routes>
                        <Route exact path='/' element = {<AuthorList authors={this.state.authors} />} />
                        <Route exact path='/books' element = {<BookList books={this.state.books} />} />
                        <Route exact path='/authors' element = {<Navigate to='/' />} />
                        <Route path='/author/:id' element = {<AuthorBookList books={this.state.books} />} />
                        <Route path="*" element = {<NotFound />} />
                    </Routes>
                </BrowserRouter>
            </div>
        )
    }
}

export default App;
