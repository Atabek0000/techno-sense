function goBack() {
    window.history.back();
}

function deleteBook(title) {
    if (confirm("Are you sure you want to delete this book?")) {
        fetch(`/delete_book`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title: title })
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert("Failed to delete the book.");
            }
        });
    }
}

