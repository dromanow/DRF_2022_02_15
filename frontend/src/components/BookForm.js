import React from 'react'

class BookForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            'title': '',
            'authors': ''
        }
    }

    handleSubmit(event) {
        this.props.newBook(this.state.title, this.state.authors)
        event.preventDefault()
    }

    handleAuthorsChange(event) {
        if (!event.target.selectedOptions) {
            return
        }

        let authors = []
        for (let i=0; i < event.target.selectedOptions.length; i++) {
            authors.push(parseInt(event.target.selectedOptions.item(i).value))
        }

        this.setState({
            'authors': authors
        })
    }

    handleTitleChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        })
    }

    render() {
        return (
            <form onSubmit={(event) => this.handleSubmit(event)} >
                <input
                    type="text"
                    name="title"
                    placeholder="title"
                    onChange={(event) => this.handleTitleChange(event)}
                    value={this.state.title}
                />
                <select multiple onChange={(event) => this.handleAuthorsChange(event)}>
                    {this.props.authors.map((author) => <option value={author.id}>{author.first_name} {author.last_name}</option>)}
                </select>
                <input type="submit" value="Create" />
            </form>
        )
    }
}

export default BookForm
