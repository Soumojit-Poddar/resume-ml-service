import re

class SkillExtractor:
    def __init__(self):
        # Comprehensive list of technical skills
        self.known_skills = {
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 
            'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'matlab', 'perl',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django',
            'flask', 'spring', 'asp.net', 'laravel', 'rails', 'next.js', 'nuxt.js',
            
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'oracle',
            'sqlite', 'dynamodb', 'firebase', 'elasticsearch',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github',
            'gitlab', 'ci/cd', 'terraform', 'ansible', 'linux', 'unix',
            
            # Data Science & ML
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras',
            'scikit-learn', 'pandas', 'numpy', 'data analysis', 'statistics',
            'nlp', 'computer vision', 'neural networks',
            
            # Other Technical Skills
            'rest api', 'graphql', 'microservices', 'agile', 'scrum', 'testing',
            'selenium', 'junit', 'jest', 'mocha', 'webpack', 'babel',
            
            # Mobile
            'android', 'ios', 'react native', 'flutter', 'xamarin',
            
            # Design
            'ui/ux', 'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator'
        }
    
    def extract_skills(self, text):
        """
        Extract skills from text using pattern matching
        
        Args:
            text (str): Input text to extract skills from
            
        Returns:
            list: List of extracted skills
        """
        if not text:
            return []
        
        text_lower = text.lower()
        found_skills = []
        
        # Check each known skill
        for skill in self.known_skills:
            # Use word boundaries to match whole words
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        # Remove duplicates and sort
        found_skills = sorted(list(set(found_skills)))
        
        return found_skills
    
    def extract_experience_years(self, text):
        """
        Extract years of experience from resume text
        
        Args:
            text (str): Resume text
            
        Returns:
            int: Years of experience (0 if not found)
        """
        if not text:
            return 0
        
        # Pattern to match "X years of experience" or "X+ years"
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of)?\s*experience',
            r'experience\s*:\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*in\s*(?:software|development|engineering)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1))
        
        return 0