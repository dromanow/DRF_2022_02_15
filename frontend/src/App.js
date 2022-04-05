import React from 'react'
import logo from './logo.svg';
import './App.css';
import AuthorList from './components/AuthorList.js'
import BookList from './components/BookList.js'
import AuthorBookList from './components/AuthorBookList.js'
import LoginForm from './components/LoginForm.js'
import BookForm from './components/BookForm.js'
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
            'books': [],
            'token': ''
        }
    }

    getData() {
        let headers = this.getHeader()

        axios
            .get('http://127.0.0.1:8000/api/authors/', {headers})
            .then(response => {
                const authors = response.data

                this.setState({
                    'authors': authors
                })
            })
            .catch(error => {
                console.log(error)
                this.setState({
                    'authors': []
                })
            })

        axios
            .get('http://127.0.0.1:8000/api/books/', {headers})
            .then(response => {
                const books = response.data

                this.setState({
                    'books': books
                })
            })
            .catch(error => {
                console.log(error)
                this.setState({
                    'books': []
                })
            })
    }

    componentDidMount() {
        let token = localStorage.getItem('token')
        this.setState({
            'token': token
        }, this.getData)
    }

    isAuth() {
        return !!this.state.token
    }

    getHeader() {
        if (this.isAuth()) {
            return {
                'Authorization': 'Token ' + this.state.token
            }
        }
        return {}
//        return {
//            'Accept': 'application/json; version=2.0'
//        }
    }

    getToken(login, password) {
        console.log(login, password)
        axios
            .post('http://127.0.0.1:8000/api-auth-token/', {'username': login, 'password': password})
            .then(response => {
                const token = response.data.token
                console.log(token)
                localStorage.setItem('token', token)
                this.setState({
                    'token': token
                }, this.getData)
            })
            .catch(error => console.log(error))
    }

    newBook(title, authors) {
        let headers = this.getHeader()
        console.log(title, authors)
        axios
            .post('http://127.0.0.1:8000/api/books/', {'title': title, 'authors': authors}, {headers})
            .then(response => {
                this.getData()
            })
            .catch(error => {
                console.log(error)
            })
    }

    deleteBook(id) {
        let headers = this.getHeader()
        console.log(id)
        axios
            .delete(`http://127.0.0.1:8000/api/books/${id}`, {headers})
            .then(response => {
                this.setState({
                    'books': this.state.books.filter((book) => book.id != id)
                })
            })
            .catch(error => {
                console.log(error)
            })

    }

    logout() {
        localStorage.setItem('token', '')
        this.setState({
            'token': ''
        }, this.getData)
    }

    render () {
        return (
            <div>
                <BrowserRouter>
                    <nav>
                        <li><Link to='/'>Authors</Link></li>
                        <li><Link to='/books'>Books</Link></li>
                        <li><Link to='/books/create'>New book</Link></li>
                        <li>
                            { this.isAuth() ? <button onClick={()=>this.logout()} >Logout</button> : <Link to='/login'>Login</Link> }
                        </li>
                    </nav>
                    <Routes>
                        <Route exact path='/' element = {<AuthorList authors={this.state.authors} />} />
                        <Route exact path='/books' element = {<BookList books={this.state.books} deleteBook={(id) => this.deleteBook(id)}/>} />
                        <Route exact path='/books/create' element = {<BookForm authors={this.state.authors} newBook={(title, authors) => this.newBook(title, authors)}/>} />
                        <Route exact path='/login' element = {<LoginForm getToken={(login, password) => this.getToken(login, password)} />} />
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
