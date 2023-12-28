import torch

from decoders.simple.beam_search import BeamSearchDecoder
from decoders.simple.stochastic_beam_search import SimpleSBSLogitProcessor, SimpleStochasticBeamSearchDecoder
from decoders import inject_supervitamined_decoders
from transformers import GenerationConfig, AutoTokenizer, AutoModelForSeq2SeqLM

from decoders.strategies.sbs_helpers.logits_process import LogitsProcessorList


def test_simple_bs_quick():
    inputs = ["a b c 1 2 ", "translate English to German: How old are you?"]
    _test_simple_sbs(inputs)


def test_simple_bs_full():
    inputs = ["translate English to German: What is your name, my dear Friend? I missed you so much",
        "translate English to German: How old are you?",
        "a b c 1 2 ",
        "summarize: Lorem ipsum dolor "
    ]
    _test_simple_sbs(inputs)


def _test_simple_sbs(inputs):
    tokenizer = AutoTokenizer.from_pretrained("t5-small")
    model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
    model.eval()
    inject_supervitamined_decoders(model)
    inputs = tokenizer(inputs,
                       return_tensors="pt", padding=True, truncation=True
                       )
    outputs = model.generate(**inputs,
                             generation_strategy=SimpleStochasticBeamSearchDecoder(),
                             generation_config=GenerationConfig(max_new_tokens=100, num_beams=5, num_return_sequences=5),
                             )

    print(f"generated text: {tokenizer.batch_decode(outputs.sequences, skip_special_tokens=True)}")
    print(f"generated probs: {outputs.sequences_scores}")
    print(f"generated gumbels: {outputs.last_scores}")

if __name__ == '__main__':
    import sys

    def debugger_is_active() -> bool:
        """Return if the debugger is currently active"""
        return hasattr(sys, 'gettrace') and sys.gettrace() is not None

    if debugger_is_active():
        test_simple_bs_quick()
    else:
        from arsenal import testing_framework
        testing_framework(globals())