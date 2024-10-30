import sentence_transformers import SentenceTransformer as ST

class run_st:
    def __init__(self):
        self.model = ST.from_pretrained('/model',
            trust_remote_code=True,
            local_files_only=True)

    def predict(self, *args, **kwargs):
        X = args[0]

        return self.model.encode(X)






