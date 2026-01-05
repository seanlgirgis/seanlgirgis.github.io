/**
 * Simple Router for Single Page Application behavior
 */
const routes = {
    'home': ['components/resume.html', 'components/downloads.html'],
    'cv': ['components/cv.html', 'components/downloads.html'],
    'projects': ['components/projects.html'],
    'articles': ['components/articles.html'],
    'tutorials': ['components/tutorials.html'],
    'blog': ['components/blog.html'],
    'about': ['components/about.html']
};

/**
 * Loads page content dynamically
 * @param {string} pageName - The key in the routes object
 */
async function loadPage(pageName) {
    const mainContent = document.getElementById('content-area');
    if (!mainContent) return;

    // Clear current content
    mainContent.innerHTML = '';

    // Scroll to top
    mainContent.scrollTop = 0;

    // Get components for this route
    const components = routes[pageName] || routes['home'];

    try {
        for (const componentPath of components) {
            // Cache busting for development
            const response = await fetch(`${componentPath}?v=${new Date().getTime()}`);
            if (!response.ok) throw new Error(`Failed to load ${componentPath}`);
            const html = await response.text();

            // Create a wrapper div or append directly
            const wrapper = document.createElement('div');
            wrapper.innerHTML = html;
            mainContent.appendChild(wrapper);
        }
    } catch (error) {
        console.error('Error loading page:', error);
        mainContent.innerHTML = '<div class="container"><p>Error loading content.</p></div>';
    }

    // Update Active Navigation State
    updateActiveNav(pageName);

    // Update Download Links based on page context (Resume vs CV)
    updateDownloadLinks(pageName);
}

function updateActiveNav(pageName) {
    document.querySelectorAll('.nav-menu li a').forEach(link => {
        link.classList.remove('active');
        // Simple check: matches exact data-page attribute
        if (link.getAttribute('data-page') === pageName) {
            link.classList.add('active');
        }
    });
}

function updateDownloadLinks(pageName) {
    // Determine target based on page
    const target = (pageName === 'cv') ? 'cv' : 'resume';
    const label = (pageName === 'cv') ? 'CV' : 'Resume';

    // Select buttons
    const btnPdf = document.querySelector('.btn-download.pdf');
    const btnWord = document.querySelector('.btn-download.word');
    const btnMd = document.querySelector('.btn-download.markdown');

    // Update hrefs (only if buttons exist on this page)
    if (btnPdf) btnPdf.href = `${target}.pdf`;
    if (btnWord) btnWord.href = `${target}.docx`;
    if (btnMd) btnMd.href = `${target}.md`;
}

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
    loadPage('home');
});
