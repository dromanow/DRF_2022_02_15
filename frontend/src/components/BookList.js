const BookItem = ({book, deleteBook}) => {
    return (
        <tr>
            <td>
                {book.title}
            </td>
            <td>
                {book.authors}
            </td>
            <td>
                <button onClick={()=>deleteBook(book.id)}>Delete</button>
            </td>
        </tr>
    )
}


const BookList = ({books, deleteBook}) => {
    return (
        <table>
            <th>
                Title
            </th>
            <th>
                Authors
            </th>
            {books.map((book) => <BookItem book={book} deleteBook={deleteBook}/>)}
        </table>
    )
}

export default BookList
