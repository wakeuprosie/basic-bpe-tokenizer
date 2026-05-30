#!/usr/local/google/home/risapark/.venv/bin/python
import time
import os
import sys

# Ensure current directory is in path so we can import tokenizer
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from tokenizer import BasicTokenizer

def run_dataset_test():
    dataset_path = os.path.join(os.path.dirname(__file__), "taylorswift.txt")
    if not os.path.exists(dataset_path):
        print(f"Dataset file not found at {dataset_path}")
        return

    print("=" * 60)
    print(" BPE TOKENIZER DATASET TEST RUN ".center(60, "="))
    print("=" * 60)

    # Load text
    with open(dataset_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    print(f"Dataset Loaded: {os.path.basename(dataset_path)}")
    print(f"Text Size: {len(text):,} characters ({len(text.encode('utf-8')):,} UTF-8 bytes)")
    
    tokenizer = BasicTokenizer()
    
    # We train with a vocabulary size of 300 (which means 44 merges)
    vocab_size = 300
    print(f"\n[1/3] Training BPE Tokenizer on dataset...")
    print(f"      Base vocab size: 256 | Target vocab size: {vocab_size}")
    
    start_time = time.time()
    try:
        # Train on first 5,000 characters for a quick, efficient test run
        tokenizer.train(text[:5000], vocab_size)
        train_time = time.time() - start_time
        print(f"      Training completed in {train_time:.4f} seconds.")
    except AttributeError as e:
        print(f"      [ERROR] Training failed: {e}")
        print("      (Note: self.vocab.append is causing this error because vocab is a dictionary)")
        return
    except Exception as e:
        print(f"      [ERROR] Training failed: {e}")
        return

    # Encode
    print(f"\n[2/3] Encoding sample text...")
    sample = "Taylor Swift is an American singer-songwriter. Her songwriting has been praised by critics."
    print(f"      Sample: {repr(sample)}")
    
    try:
        start_time = time.time()
        encoded = tokenizer.encode(sample)
        encode_time = time.time() - start_time
        
        num_bytes = len(sample.encode('utf-8'))
        num_tokens = len(encoded)
        compression = (num_bytes - num_tokens) / num_bytes * 100 if num_bytes > 0 else 0
        
        print(f"      Encoding completed in {encode_time:.6f} seconds.")
        print(f"      Original Bytes: {num_bytes}")
        print(f"      Encoded Token IDs: {encoded}")
        print(f"      Compression Ratio: {compression:.2f}% fewer tokens than UTF-8 bytes")
    except NotImplementedError:
        print("      [SKIP] encode() is not implemented.")
        return
    except Exception as e:
        print(f"      [ERROR] Encoding failed: {e}")
        return

    # Decode
    print(f"\n[3/3] Decoding token IDs...")
    try:
        start_time = time.time()
        decoded = tokenizer.decode(encoded)
        decode_time = time.time() - start_time
        
        print(f"      Decoding completed in {decode_time:.6f} seconds.")
        print(f"      Decoded Text: {repr(decoded)}")
        
        success = (sample == decoded)
        print(f"\nRoundtrip Verification: {'PASSED' if success else 'FAILED'}")
    except NotImplementedError:
        print("      [SKIP] decode() is not implemented.")
    except Exception as e:
        print(f"      [ERROR] Decoding failed: {e}")

    print("=" * 60)

if __name__ == "__main__":
    run_dataset_test()
