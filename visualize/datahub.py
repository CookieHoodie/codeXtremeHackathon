import csv
import requests
import time
import nltk
import os
from bs4 import BeautifulSoup
from nltk.corpus import stopwords


data_folder = os.path.join(os.path.dirname(__file__), "data")


class BingData:
    def __init__(self, subscription_key):
        self.subscription_key = subscription_key
        assert self.subscription_key
        self.search_results_json_list = []
        self.search_errors_json_list = []

    def search_for(self, keywords):
        # keywords should be of string type
        if not keywords:
            raise ValueError("keywords cannot be empty or None")
        api_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
        headers = {"Ocp-Apim-Subscription-Key": self.subscription_key}
        offset = 0
        count = 50

        # loop for getting 100 results
        while offset <= 50:
            params = {"q": keywords, "textDecorations": True, "textFormat": "HTML", "count": count, "offset": offset}
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            result = response.json()

            # check if the query exceeds QueryPerSecond
            if result["_type"] == "ErrorResponse":
                retry = False
                error_list = result["errors"]
                for error in error_list:
                    if error["code"] == "RateLimitExceeded":
                        if response.status_code == 429:
                            retry = True
                            break
                # if yes, wait for 1 second before retrying
                if retry:
                    print("QPS exceeded. Retrying in 1 sec...")
                    time.sleep(1)
                    continue
                # otherwise, other errors have occured. Exit the loop
                else:
                    self.search_errors_json_list.append(result)
                    break
            # Normal response
            else:
                # if adult Intent, the resultSet is empty, so directly break out
                if "adultIntent" in result["queryContext"] and "webPages" not in result["queryContext"]:
                    break

                # if not, append to resultList
                self.search_results_json_list.append(result)

                if result["webPages"]["totalEstimatedMatches"] <= 50:
                    break
                else:
                    # if num of results is in between (ie. 75), reduce the count but maintain the offset
                    #  etc. 75 - 50 = 25  ->  so the next loop will retrieve next 25 results from offset 50
                    if result["webPages"]["totalEstimatedMatches"] <= 100:
                        count = result["webPages"]["totalEstimatedMatches"] - count
                    offset += 50

    def get_joined_webpages_list(self):
        # return list of json of webpages
        # important keys: id, name, url, displayUrl(?), snippet
        if len(self.search_results_json_list) < 1:
            return []
        elif len(self.search_results_json_list) == 1:
            return self.search_results_json_list[0]["webPages"]["value"]
        elif len(self.search_results_json_list) == 2:
            first_50 = self.search_results_json_list[0]["webPages"]["value"]
            second_50 = self.search_results_json_list[1]["webPages"]["value"]
            return first_50 + second_50
        else:
            raise ValueError("Search results are more than 100. Probably someone has modified it somewhere.")

    def _tokenize(self, word, keywords=False):
        word_without_tags = BeautifulSoup(word, "html.parser").get_text().lower()
        if keywords:
            word_without_tags.replace()
        # unescaped_title_without_tags = html.unescape(title_without_tags)
        tokenized_word_list = nltk.word_tokenize(word_without_tags)
        # not all(not letter.isalnum() for letter in word) and '\'' not in word
        lowered_tokenized_word_list_without_punct = [word for word in tokenized_word_list if word.isalnum() or ('-' in word and len(word) > 1)]
        stop_words = set(stopwords.words("english"))
        tokens_without_stop_words = [w for w in lowered_tokenized_word_list_without_punct if w not in stop_words]
        return tokens_without_stop_words

    def get_tokenized_titles(self):
        titles = []
        webpages_list = self.get_joined_webpages_list()
        for webpage in webpages_list:
            title = webpage["name"]
            tokenized_title_list = self._tokenize(title)
            titles.append(tokenized_title_list)
        return titles

    def get_tokenized_snippets(self):
        snippets = []
        webpages_list = self.get_joined_webpages_list()
        for webpage in webpages_list:
            snippet = webpage["snippet"]
            tokenized_snippet = self._tokenize(snippet)
            snippets.append(tokenized_snippet)
        return snippets


def load_data(filename):
    data = []
    with open(filename, newline='', encoding="utf-8", errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append([row['title'], row['content']])

    return data


def get_full_path(filename):
    return os.path.join(data_folder, filename)


def tokenize_content(data_list):
    # data_list: ["title", "content"]
    # return: [tokens]
    stop_words = set(stopwords.words("english"))

    def tokenize_data(data):
        """
        Tokenize and clean up punctuations and stopwords in data

        :param data: untokenized string document
        :type data: str
        :return: tokenized list
        :rtype: list[str]
        """
        tokenized_word_list = nltk.word_tokenize(data)
        cleaned_tokens = [word.lower() for word in tokenized_word_list if word.isalpha()]
        tokens_without_stop_words = [word for word in cleaned_tokens if word not in stop_words]
        return tokens_without_stop_words

    cleaned_list = []
    for row in data_list:
        content = row[1]
        tokens = tokenize_data(content)
        cleaned_list.append(tokens)

    return cleaned_list


def save_tagged_data(tokenized_content_list, output_file):
    with open(output_file, "w") as f:
        for content in tokenized_content_list:
            f.write(" ".join(content))
            f.write("\n")
            break
