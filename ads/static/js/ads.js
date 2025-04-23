document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const searchInput = document.getElementById('search-input');
    const adsContainer = document.getElementById('ads-container');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            const category = this.dataset.category;
            const adCards = adsContainer.querySelectorAll('.ad-card-wrapper');

            adCards.forEach(card => {
                if (category === "" || card.dataset.category === category) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const adCards = adsContainer.querySelectorAll('.ad-card-wrapper');

        adCards.forEach(card => {
            const title = card.querySelector('.ad-title').textContent.toLowerCase();
            const description = card.querySelector('.ad-description').textContent.toLowerCase();

            if (title.includes(searchTerm) || description.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
});

