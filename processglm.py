from transformers import AutoTokenizer, AutoModel

class Worker:
    def __init__(self):
        print("loading model")
        self.tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True)
        self.model = AutoModel.from_pretrained("THUDM/chatglm2-6b-int4",trust_remote_code=True).cuda()
        self.model = self.model.eval()
        print("model loaded")

        # self.history = []
    
    def process(self,message):
        response, history = self.model.chat(self.tokenizer, message, history=[])
        return response