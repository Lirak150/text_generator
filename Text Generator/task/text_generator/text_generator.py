# Write your code here
from nltk.tokenize import WhitespaceTokenizer
from nltk import trigrams
from collections import defaultdict, Counter
import random

sentence_marks = ".!?\""


def generate_random_string(markov_chain_dict: dict):
    first_word, second_word = get_start_word(markov_chain_dict)
    result = first_word + " " + second_word + " "
    count = 2
    while not (count >= 5 and (second_word[len(second_word) - 1]
                               in sentence_marks or first_word[
                                   len(first_word) - 1] in sentence_marks)):
        words = get_next_word(second_word,
                              markov_chain_dict[(first_word, second_word)],
                              markov_chain_dict)
        if words is None:
            first_word, second_word = get_start_word(markov_chain_dict)
            result = first_word + " " + second_word + " "
            count = 2
        else:
            first_word, second_word = words
        result += first_word + " " + second_word + " "
        count += 2
    if first_word[len(first_word) - 1] in sentence_marks:
        result = result.strip().removesuffix(second_word)
    result.strip()
    print(result)


def get_third_word(first_word: str, second_word: str, markov_chain_dict: dict):
    return markov_chain_dict[(first_word, second_word)][0][0]


def get_start_word(markov_chain_dict: dict):
    list_keys = list(markov_chain_dict.keys())
    first_word, second_word = random.choice(list_keys)

    while not first_word[0].isalpha() or first_word[0].islower() or \
            first_word[len(first_word) - 1] in sentence_marks:
        first_word, second_word = random.choice(list_keys)
    return first_word, second_word


def get_next_word(second_word: str, third_words: list,
                  markov_chain_dict: dict):
    third_word = random.choices([word for word, _ in third_words],
                                weights=[count for _, count in third_words])[0]
    chain_list = markov_chain_dict[(second_word, third_word)]
    if len(chain_list) == 0:
        return None
    tail_list = list()
    count_list = list()
    for tail, count in chain_list:
        tail_list.append(tail)
        count_list.append(count)
    random_tail = random.choices(population=tail_list, weights=count_list)[0]
    return third_word, random_tail


def start_program():
    file_name = input()
    corpus = open(file_name, encoding="UTF-8", mode="rt")
    my_trigrams = get_tokenize_list(corpus.read())
    markov_chain_dict = process_trigrams(my_trigrams)
    for _ in range(10):
        generate_random_string(markov_chain_dict)
    corpus.close()


def process_trigrams(my_trigrams: list):
    markov_chain_dict = defaultdict(list)
    count = Counter(my_trigrams)
    for trigram, c in count.most_common():
        first_word, second_word, third_word = trigram
        markov_chain_dict[(first_word, second_word)].append((third_word, c))
    return markov_chain_dict


def get_tokenize_list(text: str):
    tokenize_list = WhitespaceTokenizer().tokenize(text=text)
    return list(trigrams(tokenize_list))


start_program()
