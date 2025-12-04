from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re

def generate_suggestions(job_description, resume_text, top_n_phrases=5):
    """
    Generate suggestions for improving resume based on the job description.
    This function compares important phrases (keywords and multi-word phrases) 
    from the job description and resume, identifies missing ones in the resume, 
    and suggests including them with more context.
    
    Args:
        job_description (str): The job description text.
        resume_text (str): The resume text.
        top_n_phrases (int): Number of top phrases to consider from job description.
        
    Returns:
        list of str: A list of suggestion strings.
    """
    if not job_description or not resume_text:
        return ["Job description or resume text is empty, unable to generate suggestions."]

    # Use TfidfVectorizer to extract important phrases (1 to 3 words)
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3))
    try:
        # Fit on job description to find its important terms
        job_tfidf_matrix = vectorizer.fit_transform([job_description])
        # Transform resume text using the same vocabulary
        resume_tfidf_matrix = vectorizer.transform([resume_text])
    except ValueError:
        return ["Insufficient text data to generate meaningful suggestions."]

    job_vector = job_tfidf_matrix.toarray()[0]
    resume_vector = resume_tfidf_matrix.toarray()[0]

    feature_names = np.array(vectorizer.get_feature_names_out())

    # Get top N phrases from job description sorted by tf-idf score
    # We'll check more than top_n_phrases initially to filter out single, less important words
    top_indices = job_vector.argsort()[::-1][:top_n_phrases * 3]

    # Find which top job phrases are missing or have low presence in the resume
    missing_phrases = []
    for idx in top_indices:
        # A score of 0 means the phrase is completely absent from the resume
        if job_vector[idx] > 0 and resume_vector[idx] == 0:
            phrase = feature_names[idx]
            # We prefer multi-word phrases as they are more specific
            if len(phrase.split()) > 1:
                missing_phrases.append(phrase)

    # Limit to the top N most relevant missing phrases
    missing_phrases = missing_phrases[:top_n_phrases]

    suggestions = []
    if missing_phrases:
        suggestions.append("To better align with the job description, consider highlighting your experience with the following skills or technologies:")
        # Create a list of sentences from the job description for context
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', job_description)
        for phrase in missing_phrases:
            context_sentence = ""
            # Find the sentence containing the missing phrase
            for sentence in sentences:
                if phrase.lower() in sentence.lower():
                    context_sentence = sentence.strip()
                    break
            suggestions.append(f"- **{phrase.title()}**: The job description mentions this in the context of: *\"{context_sentence}\"*. If you have relevant experience, consider describing how you've applied this skill.")
    else:
        suggestions.append("Your resume appears to cover the most important keywords and skills from the job description well. Great job!")

    return suggestions
