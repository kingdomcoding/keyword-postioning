import itertools
import re

def get_articles(filename):
    articles = []
    with open(filename, encoding="utf8") as file:
        article = ""
        for line in file:
            if line.strip():
                article += line
            elif article:
                articles.append(article)
                article = ""
            else:
                pass
        if article:
            articles.append(article)

    return articles

def separate_authors_from_titles(articles):
    titles = []

    for article in articles:
        tokens = article.split("\n")
        title = tokens[0]
        titles.append(title)

    
    return titles

def normalize_to_lowercase(titles):
    cleaned_titles = []
    for title in titles:
        lower_case_title = title.lower()
        cleaned_titles.append(lower_case_title)
    return cleaned_titles

def remove_symbols(titles):
    cleaned_titles = []
    for title in titles:
        cleaned_title = re.sub(r'[^\w|^\s|-]', '', title)
        cleaned_titles.append(cleaned_title)
    return cleaned_titles

def remove_stop_words(titles):
    cleaned_titles = []
    with open("Search Engine Stop Words.txt", encoding="utf8") as file:
        stop_words = file.read().splitlines()
        
        for title in titles:
            cleaned_title = " ".join((set(title.split()) - set(stop_words)))
            cleaned_titles.append(cleaned_title)

    return cleaned_titles    

def clean_titles(titles):
    titles = normalize_to_lowercase(titles)
    titles = remove_symbols(titles)
    titles = remove_stop_words(titles)
    return titles

def list_words_and_sources(titles):
    words_and_sources = {}

    for title_index in range(len(titles)):
        title_words = titles[title_index].split()
        for word in title_words:
            if not word in words_and_sources:
                words_and_sources[word] = [title_index]
            else:
                words_and_sources[word].append(title_index)

    return words_and_sources

def filter_high_frequency_words(words_and_sources, high_frequency_threshold):
    high_frequency_words_and_sources = {}
    for word in words_and_sources:
        if len(words_and_sources[word]) >= high_frequency_threshold:
            high_frequency_words_and_sources[word] = words_and_sources[word]
    return high_frequency_words_and_sources

def reconstruct_titles_as_list_of_useful_words(high_frequency_words_and_sources):
    titles = {}

    for word in high_frequency_words_and_sources:
        for title_index in high_frequency_words_and_sources[word]:
            if not title_index in titles:
                titles[title_index] = [word]
            else:
                titles[title_index].append(word)

    return titles


def generate_combinations_of_words(words_and_sources, minimum_number_of_words_articles_in_a_cohort_must_share_in_their_title):
    combinations = []

    number_of_words_articles_in_a_cohort_must_share_in_their_title = minimum_number_of_words_articles_in_a_cohort_must_share_in_their_title
    for combination in itertools.combinations(words_and_sources, number_of_words_articles_in_a_cohort_must_share_in_their_title):
        combinations.append(combination)
    
    return combinations

def find_titles_that_share_combination_of_words(words_and_sources):
    list_of_titles = [title for title in words_and_sources.values()]

    repeated_items_set = set(list_of_titles[0])

    for index in range(1, len(list_of_titles)):
        repeated_items_set = repeated_items_set & set(list_of_titles[index])
    return list(repeated_items_set)

def find_titles_that_share_combinations_of_words(words_and_sources, combinations_of_words):
    combinations_of_words_with_list_of_article_titles_that_share_them = {}

    for combination_of_words in combinations_of_words:
        relevant_words_and_sources = {}
        for word in combination_of_words:
            relevant_words_and_sources[word] = words_and_sources[word]
        titles_that_share_words = find_titles_that_share_combination_of_words(relevant_words_and_sources)
        if titles_that_share_words != []:
            combinations_of_words_with_list_of_article_titles_that_share_them[combination_of_words] = titles_that_share_words

    # DEBUG: find_titles_that_share_combination_of_words({'hello': [1,2,3,4,5,6], 'hi': [2,3,4,7,8], 'hey': [2,3,4,5,9,0]})
    
    return combinations_of_words_with_list_of_article_titles_that_share_them

def filter_combinations_of_words_with_enough_articles_to_form_a_cohort(combinations_of_words_with_list_of_article_titles_that_share_them, minimum_number_of_articles_that_must_be_in_a_cohort):
    valid_cohorts = {}
    for combination_of_words in combinations_of_words_with_list_of_article_titles_that_share_them:
        if len(combinations_of_words_with_list_of_article_titles_that_share_them[combination_of_words]) >= minimum_number_of_articles_that_must_be_in_a_cohort:
            valid_cohorts[combination_of_words] = combinations_of_words_with_list_of_article_titles_that_share_them[combination_of_words]
    
    return valid_cohorts

def combine_repeated_groups_of_articles_into_cohorts(groups_of_articles):
    flipped = {}
  
    for key, value in groups_of_articles.items():
        value = tuple(value)
        key = set(key)
        if value not in flipped:
            flipped[value] = key
        else:
            flipped[value] = flipped[value] | key

    combined = {}
    for key, value in flipped.items():
        value = tuple(value)
        key = set(key)
        combined[value] = list(key)

    # print(combined)
    return combined        

def find_valid_cohorts(words_and_sources, minimum_number_of_words_articles_in_a_cohort_must_share_in_their_title, minimum_number_of_articles_that_must_be_in_a_cohort):
    combinations_of_words = generate_combinations_of_words(words_and_sources, minimum_number_of_words_articles_in_a_cohort_must_share_in_their_title)
    combinations_of_words_with_list_of_article_titles_that_share_them = find_titles_that_share_combinations_of_words(words_and_sources, combinations_of_words)
    
    groups_of_articles = filter_combinations_of_words_with_enough_articles_to_form_a_cohort(combinations_of_words_with_list_of_article_titles_that_share_them, minimum_number_of_articles_that_must_be_in_a_cohort)

    valid_cohorts = combine_repeated_groups_of_articles_into_cohorts(groups_of_articles)
    return valid_cohorts

def format_cohorts_with_article_names(cohorts, articles):
    cohort_with_article_names = {}
    for cohort in cohorts:
        article_names = []
        for article in cohorts[cohort]:
            article_names.append(articles[article])
        cohort_with_article_names[cohort] = article_names
    
    return cohort_with_article_names

def get_list_of_cohort_articles(cohorts, articles):
    article_indices = list(set([article_index for sublist in cohorts.values() for article_index in sublist]))
    article_names = [articles[index] for index in article_indices]
    return article_names

def write_cohorts_to_file(cohorts_with_article_names):
    with open("Cohorts.txt", "w", encoding="utf8") as file:
        for cohort in cohorts_with_article_names:
            file.write("************************************************************\n")
            
            cohort_words = ", ".join(cohort)
            file.write(f"Cohort Words: {cohort_words}\n\n")

            file.write("Cohort Articles:\n")
            for article in cohorts_with_article_names[cohort]:
                file.write(f"{article}\n")
            
            file.write("************************************************************\n\n")


def main():
    articles = get_articles("2016 Software Engineering Papers.txt")

    titles = separate_authors_from_titles(articles)
    titles = clean_titles(titles)

    words_and_sources = list_words_and_sources(titles)

    high_frequency_threshold = 3
    high_frequency_words_and_sources = filter_high_frequency_words(words_and_sources, high_frequency_threshold)

    minimum_number_of_words_articles_in_a_cohort_must_share_in_their_title = 3
    minimum_number_of_articles_that_must_be_in_a_cohort = 3
    valid_cohorts = find_valid_cohorts(high_frequency_words_and_sources, minimum_number_of_words_articles_in_a_cohort_must_share_in_their_title, minimum_number_of_articles_that_must_be_in_a_cohort)
    
    cohorts_with_article_names = format_cohorts_with_article_names(valid_cohorts, articles)

    list_of_cohort_articles = get_list_of_cohort_articles(valid_cohorts, articles)
    
    write_cohorts_to_file(cohorts_with_article_names)
    # write_list_of_files_in_cohorts()

if __name__ == "__main__":
    main()