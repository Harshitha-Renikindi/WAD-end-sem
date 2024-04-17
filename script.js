function addTransaction(e) {
    e.preventDefault();

    let type = document.getElementById('type').value;
    let name = document.getElementById('name').value;
    let amount = document.getElementById('amount').value;

    if (type != 'chooseOne' && name.length > 0 && amount > 0) {
        const transaction = {
            type,
            name,
            amount
        };

        fetch('/addtransaction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(transaction)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showTransactions(); // Update the UI with the new transaction
                updateBalance(); // Update the balance
            } else {
                console.error(data.error);
            }
        })
        .catch(error => {
            console.error('Error adding transaction:', error);
        });
    }
}
