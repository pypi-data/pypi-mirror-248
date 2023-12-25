from transformers import AutoModelForCausalLM,AutoTokenizer,AutoModelForMaskedLM
from transformers import pipeline
from pprint import pprint

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

parser.add_argument("-n","--model_name", type=str, default="xlm-roberta-base")
parser.add_argument("-o","--export_path", type=str, default="./data/models/")

if __name__ == "__main__":
    args = parser.parse_args()
    tokenizer = AutoTokenizer.from_pretrained(args.model_name,trust_remote_code=True)
    model = AutoModelForMaskedLM.from_pretrained(args.model_name,trust_remote_code=True)
    export_path = join(args.export_path,args.model_name.replace("/","_"))
    # prepare input
    unmasker = pipeline('fill-mask', model='xlm-roberta-base')
    test_cases = ["Hello I'm a <mask> model.",
                  "<mask> is a great language.",
                  "我是一只小白<mask>。",
                  "都江<mask>是成都的名胜。",
                  "茕茕孑立、沆<mask>一气",
                  "头孢氨<mask>片说明书",
                  "\\sqrt\{3\}\\times\\sqrt\{2\}=\\sqrt\{<mask>}",
                  ]
    for test_case in test_cases:
        print("=== test case ===")
        print("[input]: ",test_case)
        pprint(unmasker(test_case))
        print()
    model.save_pretrained(export_path)
    print("[Model saved to] %s"%(abspath(export_path)))

    

