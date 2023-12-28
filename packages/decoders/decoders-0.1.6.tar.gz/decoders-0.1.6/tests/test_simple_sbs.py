from decoders.simple.beam_search import BeamSearchDecoder
from decoders.simple.stochastic_beam_search import SimpleSBSLogitProcessor, SimpleStochasticBeamSearchDecoder
from decoders import inject_supervitamined_decoders, SmallProbTransformer, SmallProbTransformerConfig
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
                             generation_strategy=BeamSearchDecoder(),
                             generation_config=GenerationConfig(max_new_tokens=100, num_beams=5,
                                                                num_return_sequences=5),
                             logits_processor=LogitsProcessorList([SimpleSBSLogitProcessor()]),
                             )

    print(f"generated text: {tokenizer.batch_decode(outputs.sequences, skip_special_tokens=True)}")
    print(f"generated probs: {outputs.sequences_scores}")
    print(f"generated gumbels: {outputs.last_scores}")

def test_small_prob_transformer():
    import torch
    inputs = torch.tensor([[-2]]*2)
    model = SmallProbTransformer(SmallProbTransformerConfig())
    inject_supervitamined_decoders(model)
    output = model.generate(inputs,
                   generation_strategy=BeamSearchDecoder(),
                   generation_config=GenerationConfig(max_new_tokens=100, num_beams=10, num_return_sequences=10),
                   logits_processor=LogitsProcessorList([SimpleSBSLogitProcessor()]),
                   )
    print(f"generated seqs: {output.sequences}")
    print(f"generated probs: {output.sequences_scores}")
    print(f"generated gumbels: {output.last_scores}")

if __name__ == '__main__':
    import sys

    def debugger_is_active() -> bool:
        """Return if the debugger is currently active"""
        return hasattr(sys, 'gettrace') and sys.gettrace() is not None

    if debugger_is_active():
        test_small_prob_transformer()
    else:
        from arsenal import testing_framework
        testing_framework(globals())