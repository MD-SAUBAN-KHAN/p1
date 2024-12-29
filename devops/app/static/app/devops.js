// Script for smooth scroll to the specific sections
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

window.onload = function() {
    const [navigationEntry] = performance.getEntriesByType('navigation');
    const pageLoadTime = navigationEntry.loadEventEnd - navigationEntry.startTime;
    fetch('/track_page_load', {
        method: 'POST',
        body: JSON.stringify({ load_time: pageLoadTime }),
        headers: { 'Content-Type': 'application/json' }
    });
}