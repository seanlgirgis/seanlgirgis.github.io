# Git Deployment Check-In Guide

This guide outlines the standard workflow for saving your work on the `dev` branch, merging it into the production `main` branch, and publishing it to GitHub.

## Prerequisite
Ensure you are currently on the `dev` branch (your `git status` output confirmed this).

---

## 1. Check Status
**Command:**
```powershell
git status
```
**Reason:**
Before doing anything, you need to know exactly which files have been changed. This prevents you from accidentally committing files you didn't mean to (like temporary test files) or missing files that need to be tracked.

---

## 2. Stage Changes (Add)
**Command:**
```powershell
git add .
```
*(Or `git add assets/css/style.css` to be specific)*

**Reason:**
Git has a "staging area". Changes aren't committed immediately; you must choose which changes "ride the bus" for the next commit. `git add .` stages *all* modified and new files.
*Note: Your `requirements.txt` is untracked. If you want it in the repo, `git add .` will include it. If not, ignore it or add it to `.gitignore`.*

---

## 3. Commit to Dev
**Command:**
```powershell
git commit -m "Fix mobile layout scrolling issue"
```
**Reason:**
This saves a snapshot of your staged changes to your local history. The message (`-m`) explains *what* changed so you (and others) can understand the history later without reading the code difference.

---

## 4. Push Dev (Backup)
**Command:**
```powershell
git push origin dev
```
**Reason:**
This uploads your local `dev` commits to the remote server (GitHub).
1.  **Backup**: If your computer crashes, your work is safe.
2.  **Collaboration**: Other developers can see your work-in-progress.

---

## 5. Switch to Main
**Command:**
```powershell
git checkout main
```
**Reason:**
To deploy to production, you need to be *on* the production branch. This command switches your active directory to match the state of `main`.

---

## 6. Pull Latest Main (Updates)
**Command:**
```powershell
git pull origin main
```
**Reason:**
Always ensure your local `main` is up-to-date with the remote `main` before merging. This prevents conflicts if someone else pushed changes while you were working.

---

## 7. Merge Dev into Main
**Command:**
```powershell
git merge dev
```
**Reason:**
This takes the history and changes from `dev` and combines them into `main`. Since `dev` is ahead of `main`, this usually performs a "fast-forward" merge, simply moving the `main` pointer forward to match `dev`.

---

## 8. Push Main (Deploy)
**Command:**
```powershell
git push origin main
```
**Reason:**
This sends the updated `main` branch to GitHub.
*   **Production Trigger**: For GitHub Pages, pushing to `main` (or `master`) usually triggers the live site to update. This is the "Deploy" step.

---

## 9. Switch Back to Dev
**Command:**
```powershell
git checkout dev
```
**Reason:**
Never stay on `main`. You should always do new work on `dev` or a feature branch. This ensures `main` remains stable and deployable at all times.

---

### Summary Checklist
1.  `git status` (Check files)
2.  `git add .` (Stage files)
3.  `git commit -m "Message"` (Save locally)
4.  `git push origin dev` (Upload dev)
5.  `git checkout main` (Switch to prod)
6.  `git pull origin main` (Update prod)
7.  `git merge dev` (Bring changes to prod)
8.  `git push origin main` (Publish site)
9.  `git checkout dev` (Return to work)
