from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List

class ResumeMatcher:
    """Calculate similarity between resume and job description"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)  # Use both unigrams and bigrams
        )
    
    def calculate_match_score(
        self,
        job_description: str,
        resume_text: str,
        job_skills: List[str],
        resume_skills: List[str]
    ) -> Dict:
        """
        Calculate comprehensive match score between JD and resume
        
        Args:
            job_description: Full job description text
            resume_text: Full resume text
            job_skills: List of required skills from JD
            resume_skills: List of skills from resume
            
        Returns:
            Dict with match details
        """
        
        # 1. Text Similarity Score (using TF-IDF + Cosine Similarity)
        try:
            tfidf_matrix = self.vectorizer.fit_transform([job_description, resume_text])
            similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            similarity_score = float(similarity_score)  # Convert to Python float
        except:
            similarity_score = 0.0
        
        # 2. Skill Matching Score
        job_skills_set = set(s.lower() for s in job_skills)
        resume_skills_set = set(s.lower() for s in resume_skills)
        
        matched_skills = list(job_skills_set.intersection(resume_skills_set))
        missing_skills = list(job_skills_set - resume_skills_set)
        
        if len(job_skills_set) > 0:
            skill_match_ratio = len(matched_skills) / len(job_skills_set)
        else:
            skill_match_ratio = 0.0
        
        # 3. Keyword Matching
        keywords = self._extract_keywords(job_description)
        keyword_matches = []
        
        for keyword in keywords:
            count = resume_text.lower().count(keyword.lower())
            if count > 0:
                keyword_matches.append({
                    'keyword': keyword,
                    'count': count
                })
        
        # 4. Calculate Overall Match Score (0-100)
        # Weighted combination:
        # - 40% text similarity
        # - 50% skill match
        # - 10% keyword matches
        keyword_score = min(len(keyword_matches) / max(len(keywords), 1), 1.0)
        
        overall_score = (
            similarity_score * 0.4 +
            skill_match_ratio * 0.5 +
            keyword_score * 0.1
        ) * 100
        
        overall_score = round(overall_score, 2)
        
        # 5. Experience Match (basic heuristic)
        experience_match = self._check_experience_match(job_description, resume_text)
        
        return {
            'match_score': overall_score,
            'similarity_score': round(similarity_score * 100, 2),
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'skill_match_percentage': round(skill_match_ratio * 100, 2),
            'keyword_matches': keyword_matches[:10],  # Top 10
            'experience_match': experience_match,
            'recommendation': self._get_recommendation(overall_score)
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from job description"""
        # Use TF-IDF to get important terms
        try:
            vectorizer = TfidfVectorizer(max_features=20, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_names = vectorizer.get_feature_names_out()
            
            # Get top keywords
            tfidf_scores = tfidf_matrix.toarray()[0]
            top_indices = tfidf_scores.argsort()[-10:][::-1]
            
            keywords = [feature_names[i] for i in top_indices]
            return keywords
        except:
            return []
    
    def _check_experience_match(self, job_desc: str, resume_text: str) -> bool:
        """Check if resume experience matches job requirements"""
        import re
        
        # Extract required years from job description
        job_exp_pattern = r'(\d+)\+?\s*years?\s*(?:of)?\s*experience'
        job_match = re.search(job_exp_pattern, job_desc.lower())
        
        # Extract candidate years from resume
        resume_match = re.search(job_exp_pattern, resume_text.lower())
        
        if job_match and resume_match:
            required_years = int(job_match.group(1))
            candidate_years = int(resume_match.group(1))
            return candidate_years >= required_years
        
        # If we can't determine, return True (give benefit of doubt)
        return True
    
    def _get_recommendation(self, score: float) -> str:
        """Get hiring recommendation based on score"""
        if score >= 75:
            return "Highly Recommended - Strong Match"
        elif score >= 60:
            return "Recommended - Good Match"
        elif score >= 45:
            return "Consider - Moderate Match"
        elif score >= 30:
            return "Review Manually - Low Match"
        else:
            return "Not Recommended - Poor Match"