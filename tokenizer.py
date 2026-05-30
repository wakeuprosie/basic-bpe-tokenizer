#!/usr/bin/env python
class BasicTokenizer:
    def __init__(self):
        self.vocab = {i: bytes([i]) for i in range(256)}
        self.merges = {}

    def train(self, text, vocab_size):
        """Train the tokenizer on the given text."""
        #encode text into UTF-8 
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

            self.vocab.append(pairofinterest,newtokenid)
            
            print("merged ", pairofinterest, " as ", newtokenid)

        #replace byte pairs with new token id
    def encode(self, text): 
        tokens = list(text.encode("UTF-8"))

        for item in self.merges:
            i = 0
            while i < len(tokens) - 1:
                if (tokens[i], tokens[i+1]) == item:
                    #replace it with the merge
                    tokens[i] = self.merges.get(item)
                    tokens.pop(i+1)
                    i += 1
                else:
                    i += 1
        return tokens

    def decode(self, ids):
        #for each key in the vocab dict, check if the key is in ids, starting at the end of dict
        string = ""
        for item in self.vocab:
            j = 0
            for j in range(len(ids)): 
                if ids[j] == item: git
                    ids[j] = self.vocab.get(item)
                    string += ids[j].decode("UTF-8")
                    j += 1
                else: 
                    j += 1
        return string


if __name__ == "__main__":
    # Quick test/example usage
    tokenizer = BasicTokenizer()
    print("BasicTokenizer initialized.")
