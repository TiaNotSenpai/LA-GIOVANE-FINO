document.addEventListener('DOMContentLoaded', function() {

// --- Gestione Menu Mobile ---
const menuToggle = document.getElementById('menu-toggle');
const mainNav = document.querySelector('.main-nav');

if (menuToggle) {
    menuToggle.addEventListener('click', () => {
        // Aggiunge/rimuove la classe .is-open sia al menu che al bottone stesso
        mainNav.classList.toggle('is-open');
        menuToggle.classList.toggle('is-open'); // Questa riga è nuova e fondamentale!

        // Aggiorna l'etichetta per l'accessibilità
        if (menuToggle.classList.contains('is-open')) {
            menuToggle.setAttribute('aria-label', 'Chiudi menu');
        } else {
            menuToggle.setAttribute('aria-label', 'Apri menu');
        }
    });
}


    // --- Animazione allo Scorrimento (Scroll Reveal) ---
    // Seleziona tutti gli elementi che devono essere animati.
    const scrollElements = document.querySelectorAll('.animate-on-scroll');

    // Crea un 'IntersectionObserver'. Questo strumento del browser
    // ci permette di sapere quando un elemento entra nello schermo.
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            // Se l'elemento è visibile...
            if (entry.isIntersecting) {
                // ...aggiungi la classe 'is-visible'.
                entry.target.classList.add('is-visible');
            }
        });
    }, {
        threshold: 0.1 // L'animazione parte quando almeno il 10% dell'elemento è visibile.
    });

    // Applica l'observer a ciascun elemento da animare.
    scrollElements.forEach(el => observer.observe(el));

});