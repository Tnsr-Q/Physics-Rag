use anyhow::Result;
use regex::Regex;

pub fn clean_and_normalize_text(text: &str) -> String {
    // Remove extra whitespace, newlines, and convert to lowercase
    let cleaned = text.replace("\n", " ").replace("\r", " ");
    let re_multi_space = Regex::new(r"\s+").unwrap();
    let normalized = re_multi_space.replace_all(&cleaned, " ").to_lowercase();
    normalized.trim().to_string()
}

pub fn extract_keywords(text: &str, num_keywords: usize) -> Vec<String> {
    let cleaned_text = clean_and_normalize_text(text);

    // Simple stop word list (can be expanded)
    let stop_words = [
        "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
        "and", "or", "but", "if", "then", "else", "when", "where", "why", "how",
        "for", "with", "without", "at", "by", "from", "to", "of", "on", "in",
        "this", "that", "these", "those", "it", "its", "he", "she", "they", "we",
        "i", "me", "you", "him", "her", "us", "them", "my", "your", "his", "her",
        "our", "their", "what", "which", "who", "whom", "whose", "can", "will",
        "would", "should", "could", "may", "might", "must", "have", "has", "had",
        "do", "does", "did", "not", "no", "yes", "very", "just", "only", "much",
        "more", "most", "less", "least", "also", "even", "such", "as", "so", "than",
        "too", "very", "s", "t", "d", "ll", "m", "o", "re", "ve", "y", "ain",
        "aren", "couldn", "didn", "doesn", "hadn", "hasn", "haven", "isn", "ma",
        "mightn", "mustn", "needn", "shan", "shouldn", "wasn", "weren", "won", "wouldn",
        "about", "above", "across", "after", "afterwards", "again", "against", "all",
        "almost", "alone", "along", "already", "also", "although", "always", "am",
        "among", "amongst", "amount", "an", "and", "another", "any", "anyhow",
        "anyone", "anything", "anyway", "anywhere", "are", "around", "as", "at",
        "back", "be", "became", "because", "become", "becomes", "becoming", "been",
        "before", "beforehand", "behind", "being", "below", "beside", "besides",
        "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can",
        "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe",
        "detail", "do", "done", "down", "due", "during", "each", "eg", "eight",
        "either", "eleven", "else", "elsewhere", "empty", "enough", "etc", "even",
        "ever", "every", "everyone", "everything", "everywhere", "except", "few",
        "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former",
        "formerly", "forty", "found", "four", "from", "front", "full", "further",
        "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her",
        "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself",
        "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in",
        "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep",
        "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may",
        "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most",
        "mostly", "move", "much", "must", "my", "myself", "name", "namely",
        "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none",
        "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often",
        "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise",
        "our", "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
        "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming",
        "seems", "serious", "several", "she", "should", "show", "side", "since",
        "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime",
        "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than",
        "that", "the", "their", "them", "themselves", "then", "thence", "there",
        "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they",
        "thick", "thin", "third", "this", "those", "though", "three", "through",
        "throughout", "thru", "thus", "to", "together", "too", "top", "toward",
        "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon",
        "us", "very", "via", "was", "we", "well", "were", "what", "whatever",
        "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby",
        "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
        "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
        "within", "without", "would", "yet", "you", "your", "yours", "yourself",
        "yourselves", "the", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
        "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
        "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-",
    ].iter().map(|&s| s.to_string()).collect::<std::collections::HashSet<String>>();

    let words = cleaned_text.split_whitespace()
        .filter(|word| !stop_words.contains(&word.to_string()))
        .collect::<Vec<&str>>();

    let mut word_counts = std::collections::HashMap::new();
    for word in words {
        *word_counts.entry(word).or_insert(0) += 1;
    }

    let mut sorted_words: Vec<(&str, &i32)> = word_counts.iter().collect();
    sorted_words.sort_by(|a, b| b.1.cmp(a.1));

    sorted_words.into_iter()
        .take(num_keywords)
        .map(|(word, _)| word.to_string())
        .collect()
}

