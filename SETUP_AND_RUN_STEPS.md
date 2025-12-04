# Setup and Run Instructions for Resume Matcher Flask App

## Step 1: Install Required Dependencies
Install the necessary Python packages globally or in your current Python environment with:

```bash
pip install flask scikit-learn PyPDF2 docx2txt werkzeug
```

## Step 3: Create Uploads Folder
Ensure the uploads folder exists for file storage:

```bash
mkdir uploads
```

(The Flask app will also create this folder automatically if missing when you run it.)

## Step 4: Run the Flask Application
Run the Flask application inside the app directory:

```bash
python -m app.main
```

By default, this will start the Flask server on `http://127.0.0.1:5000/`.
python -m app.main

## Step 5: Use the Application
1. Open your web browser and navigate to `http://127.0.0.1:5000/`.
2. Enter the job description in the provided text area.
3. Upload at least 5 resume files (.pdf, .docx, or .txt).
4. Click **Match Resumes**.
5. The app will display the top 5 matching resumes with similarity scores.

## Step 6: Monitor Logs and Errors
- The Flask server logs will appear in the terminal.
- Errors during resume processing will be logged and shown on the web page.

## Additional Notes
- Ensure uploaded resume files are supported formats.
- The matching is based on TF-IDF vectorization and cosine similarity.
- You can stop the Flask server by pressing `Ctrl+C` in the terminal.

---

This completes the necessary steps to set up, run, and use the resume matcher app.
