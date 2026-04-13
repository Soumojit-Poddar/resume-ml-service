import spacy
import re
from typing import List, Set

class SkillExtractor:
    """Extract skills from text using NLP and pattern matching"""
    
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Downloading spaCy model...")
            import os
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Comprehensive skill database
        self.known_skills = {
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 
            'php', 'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'matlab',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
            'django', 'flask', 'fastapi', 'spring', 'asp.net', 'laravel',
            
            # Databases
            'mongodb', 'mysql', 'postgresql', 'oracle', 'sql server', 'redis',
            'cassandra', 'dynamodb', 'elasticsearch', 'sql', 'nosql',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab',
            'terraform', 'ansible', 'ci/cd', 'devops', 'microservices',
            
            # Data Science & ML
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 
            'scikit-learn', 'pandas', 'numpy', 'data analysis', 'statistics',
            'nlp', 'computer vision', 'neural networks',
            
            # Mobile
            'android', 'ios', 'react native', 'flutter', 'xamarin',
            
            # Tools & Others
            'git', 'linux', 'agile', 'scrum', 'jira', 'api', 'rest', 'graphql',
            'testing', 'junit', 'selenium', 'jest', 'cypress',
            
            # Soft Skills
            'leadership', 'communication', 'teamwork', 'problem solving',
            'project management', 'analytical thinking'
        }
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from text using multiple methods
        
        Args:
            text (str): Input text (resume or job description)
            
        Returns:
            List[str]: List of extracted skills
        """
        text_lower = text.lower()
        found_skills = set()
        
        # Method 1: Direct matching with known skills
        for skill in self.known_skills:
            if skill in text_lower:
                found_skills.add(skill)
        
        # Method 2: Extract noun chunks (potential skills)
        doc = self.nlp(text)
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.lower().strip()
            # Check if it looks like a skill (2-3 words max)
            if len(chunk_text.split()) <= 3:
                # Check if it's in known skills or looks technical
                if chunk_text in self.known_skills or self._is_technical_term(chunk_text):
                    found_skills.add(chunk_text)
        
        # Method 3: Pattern matching for common skill formats
        # e.g., "experience with X", "proficient in Y"
        patterns = [
            r'experience (?:with|in) ([\w\s\.\+\#]+?)(?:\,|\.|\n)',
            r'proficient in ([\w\s\.\+\#]+?)(?:\,|\.|\n)',
            r'skilled in ([\w\s\.\+\#]+?)(?:\,|\.|\n)',
            r'knowledge of ([\w\s\.\+\#]+?)(?:\,|\.|\n)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                skill = match.strip()
                if skill in self.known_skills:
                    found_skills.add(skill)
        
        return sorted(list(found_skills))
    
    def _is_technical_term(self, term: str) -> bool:
        """Check if a term looks like a technical skill"""
        # Contains version numbers, dots, or plus signs (e.g., "node.js", "c++")
        if re.search(r'[\d\.\+\#]', term):
            return True
        
        # All caps acronyms (e.g., "API", "SQL")
        if term.isupper() and len(term) >= 2:
            return True
        
        # Contains technical keywords
        technical_keywords = ['server', 'framework', 'library', 'platform', 'stack']
        if any(keyword in term for keyword in technical_keywords):
            return True
        
        return False
    
    def extract_experience_years(self, text: str) -> int:
        """
        Extract years of experience from text
        
        Returns:
            int: Years of experience (0 if not found)
        """
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of)?\s*experience',
            r'experience\s*(?:of)?\s*(\d+)\+?\s*years?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1))
        
        return 0