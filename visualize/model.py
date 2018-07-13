from gensim.models.doc2vec import Doc2Vec, TaggedDocument


# def tag_data(cleaned_data_list):
#     # data_list: [['title', [tokens]],]
#     tagged_data = [TaggedDocument(words=row[1], tags=[i]) for i, row in enumerate(cleaned_data_list)]
#     return tagged_data


def train_model(tagged_data, vector_size, epochs):
    model = Doc2Vec(vector_size=vector_size, epochs=epochs, workers=4)
    print("building vocab")
    model.build_vocab(tagged_data)
    print("training")
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    return model


def save_model(model, filename):
    model.save(filename)
