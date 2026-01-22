// Simple function to create a card
function addCard(rowId, title, rating) {
    const row = document.getElementById(rowId);
    row.innerHTML += `
        <div class="card">
            <img src="https://via.placeholder.com/200x120" alt="house">
            <p><strong>${title}</strong></p>
            <p>Rating: ${rating} ⭐</p>
        </div>
    `;
}

// Add 3 cards to "Buy" and 3 to "Rent"
addCard('buy-row', 'Luxury Villa', '4.9');
addCard('buy-row', 'Modern Flat', '4.5');
addCard('buy-row', 'Old House', '4.2');

addCard('rent-row', 'City Apartment', '4.8');
addCard('rent-row', 'Small Studio', '4.0');
addCard('rent-row', 'Beach House', '5.0');