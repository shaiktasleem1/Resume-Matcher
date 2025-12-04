# TODO for Resume Matcher App

## Changes made:
- Updated `app/main.py` to require a minimum of 5 resume uploads instead of 1 to match test expectations and setup instructions.

## Next Steps:
1. Install required dependencies:
   ```
   pip install flask scikit-learn PyPDF2 docx2txt werkzeug
   ```

2. Run the Flask application:
   ```
   python -m app.main
   ```
   The server will run at `http://127.0.0.1:5000/`

3. Open your web browser and use the app:
   - Enter a job description
   - Upload at least 5 resumes (.pdf, .docx, .txt)
   - Click Match Resumes to see results

4. Run tests to verify functionality:
   ```
   python tests/test_resume_matcher.py
   ```

## Notes:
- Ensure `uploads/` folder is created or let the app create it automatically on first run.
- Monitor server logs for any processing errors.
