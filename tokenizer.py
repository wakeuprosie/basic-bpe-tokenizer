class BasicTokenizer:
    def __init__(self):
        #initialize dictionary of token id to bytes
        self.vocab = {i: bytes([i]) for i in range(256)}
        #store pair to tokenid mapping, in order to decode later 
        self.merges = {}

    def train(self, text, vocab_size):
        #encode input text into UTF-8 
        tokens = list(text.encode("UTF-8"))

        #add new token IDs to vocab until vocab size is met
        num_merges = vocab_size - 256

        for i in range(num_merges):
            # Count pair frequencies in current tokens
            paircounts = {}
            for pair in zip(tokens, tokens[1:]):
                paircounts[pair] = paircounts.get(pair, 0) + 1

            if not paircounts:
                break

            pairofinterest = max(paircounts, key=paircounts.get)
            newtokenid = 256 + i

            self.merges[pairofinterest] = newtokenid
            self.vocab[newtokenid] = self.vocab[pairofinterest[0]] + self.vocab[pairofinterest[1]] 

            print("merged ", pairofinterest, " as ", newtokenid)

            #replace byte pairs with new token id
            ## in tokens where you find this pair, replace it with the newtokenid
            idx = 0
            while idx < len(tokens) - 1:
                if tokens[idx] == pairofinterest[0] and tokens[idx + 1] == pairofinterest[1]:
                    tokens[idx] = newtokenid
                    tokens.pop(idx + 1)
                idx +=1

        print(f"Training tokens compressed from {len(text.encode('UTF-8'))} down to {len(tokens)} tokens!")

    def encode(self, text):
        """Encode text into token IDs."""
        raise NotImplementedError()

    def decode(self, ids):
        """Decode token IDs back into text."""
        raise NotImplementedError()


if __name__ == "__main__":
    # Quick test/example usage
    tokenizer = BasicTokenizer()
    print("BasicTokenizer initialized.")
