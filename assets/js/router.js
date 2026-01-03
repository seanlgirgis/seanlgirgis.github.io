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
            const response = await fetch(componentPath);
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

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
    loadPage('home');
});
