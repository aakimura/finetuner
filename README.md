# Finetuner for GPT-3

Finetuner is a set of scripts to help you prepare training data for GPT-3's Fine-tuning.

## Usage

You can use these scripts by running them on a Python terminal.

```bash
python -i main.py
```

Example: parse a WhatsApp conversation

```python
whatsapp.parse_convo(file='whatsapp_convo.txt', user='Selina Kyle', export_path='prepared/result.jsonl', remove='Bruce Wayne', include_user=False)
```

Will export a JSON Lines file formatted for your inspection.

```json
{"prompt": "2012-07-27T21:01:54 - You were supposed to be a shut-in.", "completion": ""}
{"prompt": "2012-07-27T21:02:03 - Why didn't you call the police?", "completion": ""}
{"prompt": "2012-07-27T21:02:34 - Yeah? Who are you pretending to be?", "completion": ""}
{"prompt": "2012-07-27T21:02:56 - His wife's in Ibiza. She left her diamonds behind, though. Worried they'd get stolen.", "completion": ""}
...
```

If you'd want to build an entity extractor, your completions could look like:

```json
{"prompt": "2012-07-27T21:01:54 - You were supposed to be a shut-in.", "completion": " named_entities= \ntime=2012-07-27T21:01:54\nEND"}
{"prompt": "2012-07-27T21:02:03 - Why didn't you call the police?", "completion": "named_entities=police\ntime=2012-07-27T21:02:03"}
{"prompt": "2012-07-27T21:02:34 - Yeah? Who are you pretending to be?", "completion": "named_entities=\ntime=2012-07-27T21:02:34\nEND"}
{"prompt": "2012-07-27T21:02:56 - His wife's in Ibiza. She left her diamonds behind, though. Worried they'd get stolen.", "completion": "named_entities=Ibiza\ntime=2012-07-27T21:02:56\nEND"}
...
```

Then you can run the `openai` tool to prepare your final JSON Lines:

```bash
openai tools fine_tunes.prepare_data -f prepared/result.jsonl -q
```

## General considerations

Although the `prepare_data` tool helps you setting separation tokens, it is good
practice to set them explicitly by yourself (so you know what to pass when using
the model).

### Prompt tokens

|Token|Description|
|---|---|
|`\n`|If you're passing multi-line prompts|
|`\n\n###\n\n`|Token to indicate where the prompt ends. Should be different to the completion's stop sequence.|

### Comlpletion tokens

Token|Description|
|---|---|
|` ` (whitespace)| Start every completion with a whitespace so GPT-3 knows where it starts|
|`\n`|If expect multi-part completions, like the entity extraction example from above|
|`###`, ` END`, etc.|Stop sequence to indicate where the completion ends. Needs to be different to the prompt's ending token.

## Why I wrote these scripts

We launched a private beta where users sent us their meals via WhatsApp. We analyzed their nutrients and provided meal feedback so they can reduce their risk of Type 2 Diabetes.

WhatsApp allows exporting conversations, but we needed a way to anonymize the data and structure it so we can fine-tune an entity extraction model.

These scripts help with that.

## Fine-tuning vs prompts

If you have already used GPT-3, the logic behind fine-tuning is quite similar: provide a prompt and an example of what you expect GPT-3 will return as a completion.

However, there is a big difference: you need to provide hundreds of examples to train GPT-3. This is similar to "normal" machine learning, where you curate training data and pass it to a statistical model.

The benefit of Fine-tuning is that you reduce drastically the costs per prompt because you save tokens by not having to give instructions to GPT-3 on each request.

The disadvantage is the amount of effort you need to put into curating each example and the quantity of training data you need to train GPT-3 appropriately. OpenAI suggests providing "a few hundred examples" of each case to have decent results.

## Resources

- [Official documentation](https://beta.openai.com/docs/guides/fine-tuning): Check out the case studies for prompt design ideas.
- [OpenAI cookbook: classification](https://github.com/openai/openai-cookbook/blob/main/examples/Fine-tuned_classification.ipynb): A Jupyter notebook that contains a nice classification example.
- [OpenAI cookbook: data collection](https://github.com/openai/openai-cookbook/blob/main/examples/fine-tuned_qa/olympics-1-collect-data.ipynb): Another Jupyter notebook for building datasets.
