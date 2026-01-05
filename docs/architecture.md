# Web Architecture & Frontend Documentation

## Overview
The website is a **Single Page Application (SPA)** built with vanilla HTML, CSS, and JavaScript. It does not rely on a backend framework (like React or Vue) or a server-side runtime. It simulates a dynamic application using a client-side router.

## Directory Structure
- **`index.html`**: The main entry point. It contains the sidebar navigation (`<nav>`) and a `<main id="content-area">` container where pages are injected.
- **`assets/js/router.js`**: The core logic engine. It handles navigation clicks, fetches HTML content, and updates the view without reloading the page.
- **`components/`**: Contains HTML fragments for each "page" (e.g., `resume.html`, `cv.html`, `projects.html`). These are partials, not full HTML documents.
- **`assets/css/style.css`**: Global styles for the sidebar, layout, and responsiveness.

## The Router (`router.js`)
The `router.js` file is responsible for the SPA behavior.

### 1. Route Definitions
Routes are defined as a mapping of page names to a list of HTML components to load.
```javascript
const routes = {
    'home': ['components/resume.html', 'components/downloads.html'],
    'cv': ['components/cv.html', 'components/downloads.html'],
    // ...
};
```
Note how `downloads.html` is reused across multiple pages.

### 2. Loading Pages (`loadPage`)
When a user clicks a nav link:
1.  `loadPage(pageName)` is called.
2.  It looks up the list of components for that route.
3.  It fetches each HTML file using `fetch()`. (A timestamp `?v=...` is added to prevent caching during development).
4.  It injects the fetched HTML into the `#content-area`.

### 3. Dynamic Download Links (`updateDownloadLinks`)
The website features an "Offline Access" section (`components/downloads.html`). Since this is a static file shared between the Resume and CV pages, the links (resume.pdf vs cv.pdf) must be updated dynamically.

The function `updateDownloadLinks(pageName)` in start of `router.js` checks the active page and modifies the `href` attributes of the download buttons:
- **Home/Resume Page**: Links point to `resume.pdf`, `resume.docx`, `resume.md`.
- **CV Page**: Links point to `cv.pdf`, `cv.docx`, `cv.md`.

## Running Locally
Because the router uses `fetch()`, you cannot open `index.html` directly from the file system (`file://`). Browsers block cross-origin requests for local files.
You must run a local server:
```bash
python -m http.server 8000
```
Then access the site at `http://localhost:8000`.
