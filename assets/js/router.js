/**
 * Simple Router for Single Page Application behavior
 */
const routes = {
    'home':    ['components/resume.html', 'components/latest_posts.html', 'components/downloads.html'],
    'resume':  ['components/resume.html', 'components/latest_posts.html', 'components/downloads.html'],
    'cv':      ['components/cv.html', 'components/downloads.html'],
    'projects':  ['components/projects.html'],
    'articles':  ['components/articles.html'],
    'leetcode':  ['components/leetcode.html'],
    'tutorials': ['components/tutorials.html'],
    'blog':      ['components/blog.html'],
    'site-map':  ['components/site_map.html'],
    'about':     ['components/about.html'],

    // Learning Hub index
    'learning': ['components/learning-nav.html'],

    // Layer 1 — Technology References
    'learning-aws-analytics':     ['components/learning-aws-analytics.html'],
    'learning-aws-compute':       ['components/learning-aws-compute.html'],
    'learning-aws-events':        ['components/learning-aws-events.html'],
    'learning-aws-security':      ['components/learning-aws-security.html'],
    'learning-cloud-other':       ['components/learning-cloud-other.html'],
    'learning-streaming':         ['components/learning-streaming.html'],
    'learning-orchestration':     ['components/learning-orchestration.html'],
    'learning-bigdata':           ['components/learning-bigdata.html'],
    'learning-transformation':    ['components/learning-transformation.html'],
    'learning-data-architecture': ['components/learning-data-architecture.html'],
    'learning-ai-genai':          ['components/learning-ai-genai.html'],
    'learning-ml':                ['components/learning-ml.html'],
    'learning-python':            ['components/learning-python.html'],
    'learning-governance':        ['components/learning-governance.html'],
    'learning-devops':            ['components/learning-devops.html'],
    'learning-databases':         ['components/learning-databases.html'],
    'learning-visualization':     ['components/learning-visualization.html'],

    // Layer 2 & 3
    'learning-craft':  ['components/learning-craft.html'],
    'learning-design': ['components/learning-design.html'],
};

/**
 * Ordered list of all learning sub-pages — drives prev/next navigation.
 */
const learningOrder = [
    { route: 'learning-aws-analytics',     label: 'AWS — Analytics & Storage' },
    { route: 'learning-aws-compute',       label: 'AWS — Compute & Containers' },
    { route: 'learning-aws-events',        label: 'AWS — Orchestration & Events' },
    { route: 'learning-aws-security',      label: 'AWS — Security & Networking' },
    { route: 'learning-cloud-other',       label: 'Cloud — Other Platforms' },
    { route: 'learning-streaming',         label: 'Streaming & Messaging' },
    { route: 'learning-orchestration',     label: 'Orchestration' },
    { route: 'learning-bigdata',           label: 'Big Data & Processing' },
    { route: 'learning-transformation',    label: 'Data Transformation' },
    { route: 'learning-data-architecture', label: 'Data Architecture Patterns' },
    { route: 'learning-ai-genai',          label: 'AI & GenAI Engineering' },
    { route: 'learning-ml',               label: 'ML & Forecasting' },
    { route: 'learning-python',           label: 'Python for Data Engineering' },
    { route: 'learning-governance',       label: 'Data Governance & Quality' },
    { route: 'learning-devops',           label: 'DevOps & Infrastructure' },
    { route: 'learning-databases',        label: 'Databases' },
    { route: 'learning-visualization',    label: 'Visualization & Reporting' },
    { route: 'learning-craft',            label: 'Engineering Craft & Patterns' },
    { route: 'learning-design',           label: 'System Design' },
];

/**
 * Injects a top nav bar and bottom prev/next bar for learning sub-pages.
 */
function injectLearningNav(pageName) {
    const idx = learningOrder.findIndex(p => p.route === pageName);
    if (idx === -1) return;

    const prev = idx > 0 ? learningOrder[idx - 1] : null;
    const next = idx < learningOrder.length - 1 ? learningOrder[idx + 1] : null;
    const pos  = `${idx + 1} / ${learningOrder.length}`;

    const topBar = `
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap;
                    gap:10px; padding:12px 0 20px; border-bottom:1px solid #eef0f4; margin-bottom:28px;">
            <a href="#" onclick="loadPage('learning');return false;"
               style="color:#004a99; font-size:0.9em; font-weight:600; text-decoration:none;">← Learning Hub</a>
            <span style="font-size:0.8em; color:#bbb;">${pos}</span>
        </div>`;

    const bottomBar = `
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap;
                    gap:10px; margin-top:44px; padding:18px 0 8px; border-top:1px solid #eef0f4;">
            <div>
                ${prev
                    ? `<a href="#" onclick="loadPage('${prev.route}');return false;"
                          style="color:#004a99; font-size:0.88em; text-decoration:none;">← ${prev.label}</a>`
                    : `<a href="#" onclick="loadPage('learning');return false;"
                          style="color:#aaa; font-size:0.88em; text-decoration:none;">← Learning Hub</a>`}
            </div>
            <a href="#" onclick="loadPage('learning');return false;"
               style="color:#aaa; font-size:0.82em; text-decoration:none;">↑ Hub</a>
            <div>
                ${next
                    ? `<a href="#" onclick="loadPage('${next.route}');return false;"
                          style="color:#004a99; font-size:0.88em; text-decoration:none;">${next.label} →</a>`
                    : `<span style="color:#ccc; font-size:0.88em;">End of Learning Hub</span>`}
            </div>
        </div>`;

    const mainContent = document.getElementById('content-area');

    // Inject top bar before first child
    const topEl = document.createElement('div');
    topEl.style.cssText = 'padding:0 0 0 0;';
    topEl.innerHTML = topBar;
    mainContent.insertBefore(topEl, mainContent.firstChild);

    // Append bottom bar
    const bottomEl = document.createElement('div');
    bottomEl.innerHTML = bottomBar;
    mainContent.appendChild(bottomEl);
}

/**
 * Loads page content dynamically.
 */
async function loadPage(pageName) {
    const mainContent = document.getElementById('content-area');
    if (!mainContent) return;

    mainContent.innerHTML = '';
    mainContent.scrollTop = 0;
    window.scrollTo(0, 0);

    const components = routes[pageName] || routes['home'];

    try {
        const v = new Date().getTime();
        const htmlParts = await Promise.all(
            components.map(async (componentPath) => {
                const response = await fetch(`${componentPath}?v=${v}`);
                if (!response.ok) throw new Error(`Failed to load ${componentPath}`);
                return response.text();
            })
        );

        htmlParts.forEach((html) => {
            const wrapper = document.createElement('div');
            wrapper.innerHTML = html;
            mainContent.appendChild(wrapper);
        });

        // Inject prev/next navigation for all learning sub-pages
        if (pageName.startsWith('learning-')) {
            injectLearningNav(pageName);
        }

    } catch (error) {
        console.error('Error loading page:', error);
        mainContent.innerHTML = '<div class="container"><p>Error loading content.</p></div>';
    }

    if (window.location.hash.substring(1) !== pageName) {
        window.location.hash = pageName;
    }

    updateActiveNav(pageName);
    updateDownloadLinks(pageName);
}


function updateActiveNav(pageName) {
    // 'resume' → 'home', all 'learning-*' sub-pages → 'learning'
    const targetPage = (pageName === 'resume')           ? 'home'
                     : pageName.startsWith('learning-')  ? 'learning'
                     : pageName;

    document.querySelectorAll('.nav-menu li a').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-page') === targetPage) {
            link.classList.add('active');
        }
    });
}

function updateDownloadLinks(pageName) {
    const target = (pageName === 'cv') ? 'cv' : 'resume';
    const label  = (pageName === 'cv') ? 'CV' : 'Resume';

    const btnPdf  = document.querySelector('.btn-download.pdf');
    const btnWord = document.querySelector('.btn-download.word');
    const btnMd   = document.querySelector('.btn-download.markdown');
    const desc    = document.querySelector('.download-center p');

    if (desc) {
        desc.innerText = (pageName === 'cv')
            ? "Download a copy of my detailed Curriculum Vitae for your records:"
            : "Download a copy of my targeted ML & Performance resume for your records:";
    }
    if (btnPdf)  { btnPdf.href  = `${target}.pdf`;  btnPdf.innerText  = `Download ${label} (PDF)`; }
    if (btnWord) { btnWord.href = `${target}.docx`; btnWord.innerText = `Download ${label} (.docx)`; }
    if (btnMd)   { btnMd.href   = `${target}.md`;   btnMd.innerText   = `Download ${label} (.md)`; }
}


// Initial load
document.addEventListener('DOMContentLoaded', () => {
    const hash = window.location.hash.substring(1);
    const page = routes[hash] ? hash : 'home';
    loadPage(page);
});

// Back/forward browser buttons
window.addEventListener('hashchange', () => {
    const hash = window.location.hash.substring(1);
    if (routes[hash]) loadPage(hash);
});
