from sentiment.model.model import bert

if __name__ == "__main__":
    print("(Down)loading model...")
    model = bert.model
    print("(Down)loading tokenizer...")
    tokenizer = bert.tokenizer
