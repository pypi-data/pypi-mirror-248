from transformers import AutoTokenizer

def print_tokenizer_tests(tokenizer):
    test_strings = ["This is a test string.",
                    "This senteeice contians a very loooooooooooong word and many typos.",
                    "我好想吃超大的西瓜啊！",
                    "w(ﾟДﾟ)w  (づ ◕‿◕ )づ (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ (╥﹏╥) _(:з」∠)_ (╯°Д°)╯︵ ┻━┻ "]
    # print general tokenizer information
    print("[name]       ", tokenizer.name_or_path)
    print("[vocab size] ", tokenizer.vocab_size)
    print()

    # test tokenizer
    for idx,test_string in enumerate(test_strings):
        print("=== test string %d ==="%(idx+1))
        tokens = tokenizer.tokenize(test_string)
        print("[tokens]            ", tokens)
        # convert back to string
        print("[test string]       ", test_string)
        print("[recovered string]  ",tokenizer.convert_tokens_to_string(tokens))

        print()

# add args
import argparse
import os
from os.path import join,abspath
parser = argparse.ArgumentParser()
sample_tokenizer_names = ["google/byt5-small",
                          "microsoft/trocr-large-handwritten",
                          "xlm-roberta-base",
                          "xlm-roberta-large",
                          "xlm-roberta-xlarge"]

parser.add_argument("-n","--tokenizer_name", type=str, default="google/byt5-small")
parser.add_argument("-o","--export_path", type=str, default="./data/tokenizers/")

if __name__ == "__main__":
    args = parser.parse_args()
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_name)
    export_path = join(args.export_path,args.tokenizer_name.replace("/","_"))
    os.makedirs(export_path, exist_ok=True)
    print_tokenizer_tests(tokenizer)
    tokenizer.save_pretrained(export_path)
    print("[Tokenizer saved to] %s"%(abspath(export_path)))

    

