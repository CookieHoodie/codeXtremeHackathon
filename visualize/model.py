from gensim.models.doc2vec import Doc2Vec, TaggedDocument


def tag_data(cleaned_data_list):  # TODO: change
    # data_list: [['title', 'content'],]
    tagged_data = [TaggedDocument(words=row[1], tags=[i]) for i, row in enumerate(data_list)]
    return tagged_data


