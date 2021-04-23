# from collections import Counter
import itertools

def get_titles(filename):
    titles = []
    with open(filename, encoding="utf8") as file:
        title = ""
        for line in file:
            if line.strip():
                title += line
            elif title:
                titles.append(title)
                title = ""
            else:
                pass
        if title:
            titles.append(title)

    return titles

def remove_document_name(titles):
    titles.pop(0)
    return titles

def clean_titles(titles):
    titles = remove_document_name(titles)
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

# def find_same_items_in_lists(*args):
#     if not args:
#         return []
#     elif len(args) == 1:
#         return args[0]
#     else:
#         repeated_items_set = set(args[0])
#         for list_index in range(1, len(args)):
#             repeated_items_set = repeated_items_set & set(args[list_index])
#         return list(repeated_items_set)


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
    
    # print(combinations_of_words_with_list_of_article_titles_that_share_them)
    return combinations_of_words_with_list_of_article_titles_that_share_them

def filter_combinations_of_words_with_enough_articles_to_form_a_cohort(combinations_of_words_with_list_of_article_titles_that_share_them, minimum_number_of_articles_that_must_be_in_a_cohort):
    valid_cohorts = {}
    for combination_of_words in combinations_of_words_with_list_of_article_titles_that_share_them:
        if len(combinations_of_words_with_list_of_article_titles_that_share_them[combination_of_words]) >= minimum_number_of_articles_that_must_be_in_a_cohort:
            valid_cohorts[combination_of_words] = combinations_of_words_with_list_of_article_titles_that_share_them[combination_of_words]
    # print(valid_cohorts)
    return valid_cohorts

def find_articles_that_have_set_of_words_in_common(words_and_sources, minimum_number_of_words_articles_in_a_cohort_must_share_in_their_title, minimum_number_of_articles_that_must_be_in_a_cohort):
    combinations_of_words = generate_combinations_of_words(words_and_sources, minimum_number_of_words_articles_in_a_cohort_must_share_in_their_title)
    combinations_of_words_with_list_of_article_titles_that_share_them = find_titles_that_share_combinations_of_words(words_and_sources, combinations_of_words)
    
    valid_cohorts = filter_combinations_of_words_with_enough_articles_to_form_a_cohort(combinations_of_words_with_list_of_article_titles_that_share_them, minimum_number_of_articles_that_must_be_in_a_cohort)

    # print(valid_cohorts)
    # return valid_cohorts




    # minimum_number_of_articles_that_must_be_in_a_cohort
    
    # for combination_of_words in combinations_of_words:
    #     articles_containing_this_combination_of_words = find_same_items_in_lists()
    # pass


def main():
    titles = get_titles("2016 Software Engineering Papers.txt")
    titles = clean_titles(titles)

    words_and_sources = list_words_and_sources(titles)

    high_frequency_threshold = 3
    high_frequency_words_and_sources = filter_high_frequency_words(words_and_sources, high_frequency_threshold)

    minimum_number_of_words_articles_in_a_cohort_must_share_in_their_title = 3
    minimum_number_of_articles_that_must_be_in_a_cohort = 3
    sets_of_words_and_articles_that_have_them_in_common = find_articles_that_have_set_of_words_in_common(high_frequency_words_and_sources, minimum_number_of_words_articles_in_a_cohort_must_share_in_their_title, minimum_number_of_articles_that_must_be_in_a_cohort)
    
    # title_of_useful_words_dict = reconstruct_titles_as_list_of_useful_words(high_frequency_words_and_sources)
    # print(len(high_frequency_words_and_sources))

    # words_in_title_count = count_words_in_titles(titles)

    # for ti

if __name__ == "__main__":
    main()