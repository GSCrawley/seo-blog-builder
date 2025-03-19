"""
NLP Keyword Analyzer for extracting keywords and topics from text.
"""
import logging
import re
import json
from typing import Dict, Any, List, Optional
from collections import Counter
import math

# We'll use NLTK - it's free and widely available
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from nltk.collocations import TrigramAssocMeasures, TrigramCollocationFinder

from app.config import settings

logger = logging.getLogger(__name__)

class NlpKeywordAnalyzer:
    """
    Service for analyzing text to extract keywords and topics using NLP techniques.
    """
    
    def __init__(self):
        """Initialize the NLP Keyword Analyzer service."""
        self.ensure_nltk_resources()
        self.stop_words = set(stopwords.words('english'))
        self.additional_stop_words = {
            'would', 'could', 'should', 'may', 'might', 'must', 'need',
            'going', 'things', 'thing', 'something', 'anything', 'everything',
            'nothing', 'way', 'ways', 'lot', 'lots', 'kind', 'kinds', 'type',
            'types', 'example', 'examples', 'like', 'good', 'great', 'best',
            'better', 'worst', 'bad', 'right', 'well', 'make', 'makes', 'made',
            'making', 'take', 'takes', 'taking', 'look', 'looks', 'looking',
            'see', 'sees', 'seeing', 'come', 'comes', 'coming', 'go', 'goes',
            'going', 'gone', 'know', 'knows', 'knowing', 'knew', 'get', 'gets',
            'getting', 'got', 'gotten', 'want', 'wants', 'wanting', 'wanted',
            'give', 'gives', 'giving', 'gave', 'given', 'use', 'uses', 'using',
            'used', 'try', 'tries', 'trying', 'tried'
        }
        self.stop_words.update(self.additional_stop_words)
        self.lemmatizer = WordNetLemmatizer()
    
    def ensure_nltk_resources(self):
        """Ensure required NLTK resources are downloaded."""
        try:
            required_resources = [
                'punkt',            # for tokenization
                'stopwords',        # for stopwords
                'wordnet',          # for lemmatization
                'averaged_perceptron_tagger'  # for POS tagging
            ]
            
            for resource in required_resources:
                try:
                    nltk.data.find(f'tokenizers/{resource}' if resource == 'punkt' else f'corpora/{resource}')
                except LookupError:
                    logger.info(f"Downloading NLTK resource: {resource}")
                    nltk.download(resource, quiet=True)
        except Exception as e:
            logger.error(f"Error ensuring NLTK resources: {str(e)}")
            logger.warning("Some NLP features may not work correctly")
    
    def analyze_text(self, text: str, max_keywords: int = 20) -> Dict[str, Any]:
        """
        Analyze text to extract keywords, topics, and other NLP metrics.
        
        Args:
            text: Text to analyze
            max_keywords: Maximum number of keywords to extract
            
        Returns:
            Dict: Text analysis results
        """
        logger.info(f"Analyzing text with {len(text)} characters")
        
        try:
            # Clean and tokenize the text
            cleaned_text = self._clean_text(text)
            sentences = sent_tokenize(cleaned_text)
            word_tokens = word_tokenize(cleaned_text)
            
            # Remove stopwords and punctuation
            filtered_tokens = [w.lower() for w in word_tokens if w.lower() not in self.stop_words and w.isalpha()]
            
            # Lemmatize tokens
            lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in filtered_tokens]
            
            # Get POS tags
            pos_tags = nltk.pos_tag(filtered_tokens)
            
            # Extract single-word keywords (nouns and proper nouns)
            nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
            
            # Extract bigrams (two-word phrases)
            bigram_measures = BigramAssocMeasures()
            bigram_finder = BigramCollocationFinder.from_words(filtered_tokens)
            # Filter bigrams that appear less than 3 times
            bigram_finder.apply_freq_filter(2)
            bigrams = bigram_finder.nbest(bigram_measures.pmi, 15)
            
            # Extract trigrams (three-word phrases)
            trigram_measures = TrigramAssocMeasures()
            trigram_finder = TrigramCollocationFinder.from_words(filtered_tokens)
            # Filter trigrams that appear less than 2 times
            trigram_finder.apply_freq_filter(1)
            trigrams = trigram_finder.nbest(trigram_measures.pmi, 10)
            
            # Count frequency of lemmatized tokens
            token_freq = Counter(lemmatized_tokens)
            
            # Calculate TF-IDF for tokens in sentences
            tfidf_scores = self._calculate_tfidf(sentences, lemmatized_tokens)
            
            # Extract top keywords by TF-IDF score
            top_keywords = [{"word": word, "score": score} for word, score in tfidf_scores[:max_keywords]]
            
            # Format n-grams
            formatted_bigrams = [' '.join(bigram) for bigram in bigrams]
            formatted_trigrams = [' '.join(trigram) for trigram in trigrams]
            
            # Readability metrics
            readability = self._calculate_readability(text, sentences, word_tokens)
            
            # Sentiment analysis (simplified)
            sentiment = self._analyze_sentiment(text)
            
            # Combine results
            analysis = {
                "keywords": top_keywords,
                "bigrams": formatted_bigrams,
                "trigrams": formatted_trigrams,
                "top_nouns": list(Counter(nouns).most_common(max_keywords)),
                "token_frequency": dict(token_freq.most_common(max_keywords)),
                "readability": readability,
                "sentiment": sentiment,
                "sentence_count": len(sentences),
                "word_count": len(word_tokens),
                "unique_word_count": len(set(lemmatized_tokens))
            }
            
            logger.info(f"Text analysis completed successfully")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            return {
                "error": str(e),
                "keywords": [],
                "bigrams": [],
                "trigrams": [],
                "readability": {},
                "sentiment": {"score": 0, "label": "neutral"}
            }
    
    def generate_related_keywords(self, seed_keyword: str, count: int = 20) -> List[str]:
        """
        Generate related keywords for a seed keyword using NLP techniques.
        
        Args:
            seed_keyword: Seed keyword to expand
            count: Number of related keywords to generate
            
        Returns:
            List: List of related keywords
        """
        logger.info(f"Generating related keywords for: {seed_keyword}")
        
        try:
            # Split seed keyword into words
            seed_words = seed_keyword.lower().split()
            
            # Generate variations with common modifiers
            modifiers_before = ['best', 'top', 'cheap', 'affordable', 'premium', 'professional', 
                             'ultimate', 'complete', 'essential', 'easy', 'quick', 'simple',
                             'advanced', 'beginners', 'expert', 'reliable', 'recommended',
                             'popular', 'trending', 'new', 'modern', 'high quality', 'low cost']
            
            modifiers_after = ['guide', 'tutorial', 'tips', 'tricks', 'ideas', 'examples', 'review', 
                             'reviews', 'comparison', 'alternatives', 'vs', 'for beginners',
                             'for experts', 'techniques', 'secrets', 'handbook', 'solutions',
                             'problems', 'help', 'support', 'advice', 'online', 'near me',
                             'service', 'services', 'software', 'tools', 'apps', 'application']
            
            question_prefixes = ['how to', 'what is', 'why', 'where to', 'when to',
                               'which', 'who', 'can I', 'should I', 'will']
            
            # Generate variations
            variations = []
            
            # Add original keyword
            variations.append(seed_keyword)
            
            # Add modifiers before
            for modifier in modifiers_before:
                variations.append(f"{modifier} {seed_keyword}")
            
            # Add modifiers after
            for modifier in modifiers_after:
                variations.append(f"{seed_keyword} {modifier}")
            
            # Add question forms
            for prefix in question_prefixes:
                variations.append(f"{prefix} {seed_keyword}")
            
            # Add year variations
            import datetime
            current_year = datetime.datetime.now().year
                
            variations.append(f"{seed_keyword} {current_year}")
            variations.append(f"{seed_keyword} {current_year+1}")
            variations.append(f"best {seed_keyword} {current_year}")
            
            # Generate combinations (use only a subset to avoid too many)
            import random
            combo_before = random.sample(modifiers_before, min(5, len(modifiers_before)))
            combo_after = random.sample(modifiers_after, min(5, len(modifiers_after)))
            
            for before in combo_before:
                for after in combo_after:
                    variations.append(f"{before} {seed_keyword} {after}")
            
            # Remove duplicates and sort by length
            variations = list(set(variations))
            variations.sort(key=len)
            
            # Return requested number
            return variations[:count]
            
        except Exception as e:
            logger.error(f"Error generating related keywords: {str(e)}")
            return [seed_keyword]
    
    def extract_keywords_from_url_list(self, urls: List[str], max_keywords: int = 20) -> Dict[str, Any]:
        """
        Extract common keywords from a list of URLs.
        Placeholder - in a real implementation, we would fetch and analyze each URL.
        
        Args:
            urls: List of URLs to analyze
            max_keywords: Maximum number of keywords to extract
            
        Returns:
            Dict: Analysis of common keywords
        """
        logger.info(f"Extracting keywords from {len(urls)} URLs")
        
        try:
            # In a real implementation, we would:
            # 1. Fetch each URL's content
            # 2. Extract text content from HTML
            # 3. Analyze each text
            # 4. Aggregate the results
            
            # For now, we'll just extract domains and generate mock data
            domains = []
            for url in urls:
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(url).netloc
                    domains.append(domain)
                except:
                    pass
            
            # Mock data based on domains
            mock_keywords = [
                {"word": "keyword1", "score": 0.95},
                {"word": "keyword2", "score": 0.90},
                {"word": "keyword3", "score": 0.85},
                {"word": "keyword4", "score": 0.80},
                {"word": "keyword5", "score": 0.75},
            ]
            
            mock_analysis = {
                "urls_analyzed": len(urls),
                "domains": domains,
                "common_keywords": mock_keywords[:max_keywords],
                "note": "This is a simplified implementation. For accurate results, each URL should be fetched and analyzed."
            }
            
            return mock_analysis
            
        except Exception as e:
            logger.error(f"Error extracting keywords from URLs: {str(e)}")
            return {
                "error": str(e),
                "urls_analyzed": 0,
                "common_keywords": []
            }
    
    def _clean_text(self, text: str) -> str:
        """
        Clean text for analysis.
        
        Args:
            text: Text to clean
            
        Returns:
            str: Cleaned text
        """
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _calculate_tfidf(self, sentences: List[str], tokens: List[str]) -> List[tuple]:
        """
        Calculate TF-IDF scores for tokens.
        
        Args:
            sentences: List of sentences
            tokens: List of tokens
            
        Returns:
            List: List of (token, score) tuples
        """
        # Calculate term frequency (TF)
        tf = Counter(tokens)
        
        # Calculate document frequency (DF)
        df = {}
        for token in set(tokens):
            df[token] = sum(1 for sentence in sentences if token in sentence.lower())
        
        # Calculate TF-IDF
        tfidf = {}
        N = len(sentences)
        for token, freq in tf.items():
            if df[token] > 0:
                tfidf[token] = freq * math.log(N / df[token])
        
        # Sort by score
        sorted_tfidf = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_tfidf
    
    def _calculate_readability(self, text: str, sentences: List[str], words: List[str]) -> Dict[str, Any]:
        """
        Calculate readability metrics.
        
        Args:
            text: Full text
            sentences: List of sentences
            words: List of words
            
        Returns:
            Dict: Readability metrics
        """
        # Count characters (excluding spaces)
        chars = len(text.replace(' ', ''))
        
        # Count words and sentences
        word_count = len(words)
        sentence_count = len(sentences)
        
        if word_count == 0 or sentence_count == 0:
            return {
                "flesch_reading_ease": 0,
                "flesch_kincaid_grade": 0,
                "complex_word_count": 0,
                "avg_words_per_sentence": 0
            }
        
        # Count syllables and complex words
        syllable_count = 0
        complex_word_count = 0
        
        for word in words:
            syllables = self._count_syllables(word)
            syllable_count += syllables
            if syllables >= 3:
                complex_word_count += 1
        
        # Calculate metrics
        avg_words_per_sentence = word_count / sentence_count
        avg_syllables_per_word = syllable_count / word_count
        
        # Flesch Reading Ease
        flesch_reading_ease = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
        
        # Flesch-Kincaid Grade Level
        flesch_kincaid_grade = 0.39 * avg_words_per_sentence + 11.8 * avg_syllables_per_word - 15.59
        
        return {
            "flesch_reading_ease": flesch_reading_ease,
            "flesch_kincaid_grade": flesch_kincaid_grade,
            "complex_word_count": complex_word_count,
            "avg_words_per_sentence": avg_words_per_sentence
        }
    
    def _count_syllables(self, word: str) -> int:
        """
        Count syllables in a word (simplified approach).
        
        Args:
            word: Word to count syllables for
            
        Returns:
            int: Number of syllables
        """
        word = word.lower()
        
        # Count vowels sequences as syllables
        syllables = 0
        vowels = 'aeiouy'
        prev_char_is_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_char_is_vowel:
                syllables += 1
            prev_char_is_vowel = is_vowel
        
        # Handle special cases
        if word.endswith('e'):
            syllables -= 1
        if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
            syllables += 1
        if syllables == 0:
            syllables = 1
        
        return syllables
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Perform simple sentiment analysis.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dict: Sentiment analysis result
        """
        # A very simple approach using basic word lists
        positive_words = {
            'good', 'great', 'excellent', 'best', 'amazing', 'wonderful', 'perfect',
            'love', 'like', 'enjoy', 'recommend', 'positive', 'outstanding', 'fantastic',
            'awesome', 'favorable', 'superior', 'terrific', 'superb', 'delightful',
            'happy', 'glad', 'pleased', 'satisfied', 'impressive', 'exceptional'
        }
        
        negative_words = {
            'bad', 'worst', 'terrible', 'poor', 'horrible', 'awful', 'disappointing',
            'hate', 'dislike', 'inferior', 'negative', 'mediocre', 'inadequate',
            'frustrating', 'useless', 'worthless', 'sad', 'unhappy', 'unsatisfied',
            'fail', 'fails', 'failed', 'failing', 'failure', 'pain', 'painful'
        }
        
        # Tokenize and clean
        tokens = word_tokenize(text.lower())
        filtered_tokens = [token for token in tokens if token.isalpha()]
        
        # Count positive and negative words
        positive_count = sum(1 for token in filtered_tokens if token in positive_words)
        negative_count = sum(1 for token in filtered_tokens if token in negative_words)
        
        # Calculate sentiment score (-1 to 1)
        total = positive_count + negative_count
        if total == 0:
            score = 0
        else:
            score = (positive_count - negative_count) / total
        
        # Determine sentiment label
        if score > 0.1:
            label = "positive"
        elif score < -0.1:
            label = "negative"
        else:
            label = "neutral"
        
        return {
            "score": score,
            "label": label,
            "positive_words": positive_count,
            "negative_words": negative_count
        }
