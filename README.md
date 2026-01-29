# GitHub Webhook Receiver & Dashboard

This project is a full-stack solution built for the **TechStaX Developer Assessment**. It consists of a Python (Flask) backend that listens for real-time GitHub events (Push, Pull Request, Merge), stores them in a MongoDB database, and displays them on a live-updating dashboard.

## 🚀 Features

* [cite_start]**Webhook Receiver:** Captures `PUSH`, `PULL_REQUEST`, and `MERGE` events from a GitHub repository. [cite: 5, 23]
* [cite_start]**Database Integration:** Stores event data in **MongoDB** using a strict schema (Author, Branch, Timestamp, etc.). [cite: 24, 26]
* [cite_start]**Live Dashboard:** A clean, minimal UI that polls the database every 15 seconds to show the latest activity without refreshing. [cite: 6, 28]
* **Action Handling:**
    * [cite_start]**Push:** Logs the author, branch, and commit hash. [cite: 8]
    * [cite_start]**Pull Request:** Logs the author, source branch, and target branch. [cite: 11]
    * [cite_start]**Merge:** Detects closed PRs as merge events (Bonus Feature). [cite: 13, 14]

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask
* **Database:** MongoDB (Atlas)
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
* **Tools:** Ngrok (for local tunneling), PyMongo

---

## ⚙️ Installation & Setup

### 1. Prerequisites
* Python 3.x installed.
* A MongoDB Atlas account (or local MongoDB).
* [Ngrok](https://ngrok.com/) installed for local testing.

### 2. Clone the Repository
```bash
git clone <your-webhook-repo-url>
cd webhook-repo
