from optimum.intel import OVSentenceTransformer as OV

class run_ov:
    def __init__(self):
        self.model = OV.from_pretrained('/model_ov',
            trust_remote_code=True,
            repo_type="local",
            local_files_only=True)

    def predict(self, *args, **kwargs):
        X = args[0]

        return self.model.encode(X)



