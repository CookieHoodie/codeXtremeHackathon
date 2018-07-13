from pathlib import Path
from gensim.models.doc2vec import TaggedLineDocument

import visualize.datahub as datahub
import visualize.model as v_model


def main():
    model_file = datahub.get_full_path("doc2vec.model")
    if not Path(model_file).exists():
        tokenized_file = datahub.get_full_path("articles1_token.txt")
        if not Path(tokenized_file).exists():
            print("data is not yet tokenized and saved. Doing now.")
            print("loading data")
            data_list = datahub.load_data(datahub.get_full_path("articles1.csv"))
            print("tokenizing data")
            tokenized_content_list = datahub.tokenize_content(data_list)
            print("saving tokenizing data in txt file")
            datahub.save_tagged_data(tokenized_content_list, tokenized_file)

        vector_size = 50
        epochs = 100
        print("training model")
        trained_model = v_model.train_model(TaggedLineDocument(tokenized_file), vector_size, epochs)
        print("saving model")
        v_model.save_model(trained_model, model_file)
        print("finish")
    else:
        print("{} already exists. Exiting.".format(model_file))


main()
