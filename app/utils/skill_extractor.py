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