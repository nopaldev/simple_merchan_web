// Add smooth scrolling to top links
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function (event) {
        event.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        target.scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Highlight active link
window.addEventListener('scroll', function () {
    const links = document.querySelectorAll('.nav-link');
    let scrollPos = window.scrollY;

    links.forEach(link => {
        const section = document.querySelector(link.getAttribute('href'));
        if (section && section.offsetTop <= scrollPos && (section.offsetTop + section.offsetHeight) > scrollPos) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});
