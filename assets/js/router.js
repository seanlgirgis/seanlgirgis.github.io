/**
 * Simple Router for Single Page Application behavior
 */
const routes = {
    'home': ['components/resume.html', 'components/downloads.html'],
    'resume': ['components/resume.html', 'components/downloads.html'], // Alias for home
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

    // Update URL hash without triggering scroll
    if (window.location.hash.substring(1) !== pageName) {
        window.location.hash = pageName;
    }

    // Update Active Navigation State
    updateActiveNav(pageName);

    // Update Download Links based on page context (Resume vs CV)
    updateDownloadLinks(pageName);
}


function updateActiveNav(pageName) {
    /**
     * Updates the CSS class of the navigation menu.
     * Highlights the link corresponding to the current page.
     */
    // Map 'resume' alias to 'home' for highlighting
    const targetPage = (pageName === 'resume') ? 'home' : pageName;

    document.querySelectorAll('.nav-menu li a').forEach(link => {
        link.classList.remove('active');
        // Simple check: matches exact data-page attribute
        if (link.getAttribute('data-page') === targetPage) {
            link.classList.add('active');
        }
    });
}

function updateDownloadLinks(pageName) {
    /**
     * Dynamically updates the "Offline Access" download buttons.
     * Since 'components/downloads.html' is shared, we must toggle the HREFs
     * depending on whether we are viewing the Resume (Home) or the CV.
     */
    // Determine target based on page
    const target = (pageName === 'cv') ? 'cv' : 'resume';
    const label = (pageName === 'cv') ? 'CV' : 'Resume';

    // Select buttons
    const btnPdf = document.querySelector('.btn-download.pdf');
    const btnWord = document.querySelector('.btn-download.word');
    const btnMd = document.querySelector('.btn-download.markdown');

    // Update Description Text
    const desc = document.querySelector('.download-center p');
    if (desc) {
        desc.innerText = (pageName === 'cv')
            ? "Download a copy of my detailed Curriculum Vitae for your records:"
            : "Download a copy of my targeted ML & Performance resume for your records:";
    }

    // Update hrefs and labels (only if buttons exist on this page)
    if (btnPdf) {
        btnPdf.href = `${target}.pdf`;
        btnPdf.innerText = `Download ${label} (PDF)`;
    }
    if (btnWord) {
        btnWord.href = `${target}.docx`;
        btnWord.innerText = `Download ${label} (.docx)`;
    }
    if (btnMd) {
        btnMd.href = `${target}.md`;
        btnMd.innerText = `Download ${label} (.md)`;
    }
}


// Initial Load
document.addEventListener('DOMContentLoaded', () => {
    // Check for hash in URL (e.g. #about)
    const hash = window.location.hash.substring(1);

    // Validate hash against routes, default to 'home'
    const page = routes[hash] ? hash : 'home';

    loadPage(page);
});

// Handle Back/Forward Browser Buttons
window.addEventListener('hashchange', () => {
    const hash = window.location.hash.substring(1);
    if (routes[hash]) {
        loadPage(hash);
    }
});
