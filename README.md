# LLM Guess the Number

## Query

The following query was sent as-is to various LLMs (inspired by an over-representation of LLMs' certain answers to a thread on [Reddit](https://www.reddit.com/r/OpenAI/comments/1lejvbl/1_question_1_answer_5_models/)):

"I am thinking of a random integer number between 1 and 50. Try to guess what number I am thinking of. You will only get one guess and please return the answer as a plain number."

The results from the query are stored in the ```out```-folder, with filenames indicating models, temperature-parameter,
and replication index.

## Files and runs

The LLMs were called on June 23rd and 25th, 2025. 

Files for the run:

- ```runGuess.py``` : Contains the main loop to query the LLM APIs
- ```gatherGuess.py``` : After running ```runGuess.py```, gathers results from the ```out```-folder and pops out suitable pandas
- ```.env``` : Contains API keys etc needed to run ```runGuess.py```, but omitted from this repo for obvious reasons

## Results

Apparently, if LLMs are not explicitly not stated to use a (pseudo)random generation algorithm for this query, they will
resort to numbers ending in 7 (or 3) quite often. Some decide to go with the mid-range (25). I added the further 
instruction "you will only get one guess" because LLMs often would treat this as a guessing game, where they would get 
multiple guesses with an answer if the true answer was guessed, or if it was lower or higher. For this the obvious optimal
strategy in average would be a binary search tree starting at 25. and checking halving-points to the right direction. 
Instructions to return the answer as a plain number was merely for convenience, so the one to two digit number would be 
easier to RegEx out from the output.

27, 37, 23, 17, and 25 were popular choices. Other notable ones were 1 (Llama 4 Maverick and few by DeepSeek-v3); the 
only surprise really was the lack of 42 (reference to [Douglas Adams' books](https://www.wikihow.com/42-Meaning)); only one who guessed this was o1 (temp 1.0).
The prevalence of numbers ending in 7s may be attributed to the ["blue-seven" social phenomenon](https://en.wikipedia.org/wiki/Blue%E2%80%93seven_phenomenon), although I'm not 
sure how widely accepted this is. But for some reason LLMs do tend towards 7s (and 3s), despite indicating at least on 
some level that the number thought of would be "random".

If the number thought of is not truly random, people tend to avoid "non-random" seeming numbers, such a 1, 50, 25, etc. 
So most likely if this was a question presented at the street, the distribution of the real answer would be something of 
a bimodal distribution within the range 1 to 50, maybe with bumps at places like 23, 27, 33, and 37 or so, and 
statistical under-representation at the ends (1 and 50) and middle (25). Just guessing though.

While most models were quite conservative in how verbose they were in their answers, most adhered to the instructions to 
just return a plain number. Only notable exception was DeepSeek-models (especially -R1), which insisted on justifying its answers in length. 

Results are shown below, stratified according to the temperature parameter. The queries were always replicated 100 times 
with resetting of the client session.

### Temperature 0.0

```commandline
                     modelname  temp  Top answer 2nd answer 3rd answer
     claude-3-5-haiku-20241022   0.0  25 (89.0%) 27 (11.0%)        NaN
    claude-3-5-sonnet-20240620   0.0 27 (100.0%)        NaN        NaN
    claude-3-5-sonnet-20241022   0.0 27 (100.0%)        NaN        NaN
    claude-3-7-sonnet-20250219   0.0 27 (100.0%)        NaN        NaN
        claude-opus-4-20250514   0.0 23 (100.0%)        NaN        NaN
      claude-sonnet-4-20250514   0.0 27 (100.0%)        NaN        NaN
       deepseek-ai_deepseek-r1   0.0  37 (55.0%) 25 (28.0%) 27 (14.0%)
       deepseek-ai_deepseek-v3   0.0  25 (96.0%)   1 (4.0%)        NaN
          gemini-2.0-flash-001   0.0 25 (100.0%)        NaN        NaN
     gemini-2.0-flash-lite-001   0.0 25 (100.0%)        NaN        NaN
  gemini-2.5-pro-preview-03-25   0.0  25 (78.0%) 23 (21.0%)  17 (1.0%)
  gemini-2.5-pro-preview-05-06   0.0  25 (78.0%) 23 (20.0%)  27 (2.0%)
  gemini-2.5-pro-preview-06-05   0.0  37 (79.0%) 25 (21.0%)        NaN
google-deepmind_gemma-3-12b-it   0.0 25 (100.0%)        NaN        NaN
google-deepmind_gemma-3-27b-it   0.0 25 (100.0%)        NaN        NaN
 google-deepmind_gemma-3-4b-it   0.0 25 (100.0%)        NaN        NaN
            gpt-4.1-2025-04-14   0.0 27 (100.0%)        NaN        NaN
       gpt-4.1-mini-2025-04-14   0.0 27 (100.0%)        NaN        NaN
       gpt-4.1-nano-2025-04-14   0.0 25 (100.0%)        NaN        NaN
             gpt-4o-2024-05-13   0.0  27 (81.0%) 25 (19.0%)        NaN
             gpt-4o-2024-08-06   0.0 27 (100.0%)        NaN        NaN
             gpt-4o-2024-11-20   0.0  25 (58.0%) 27 (42.0%)        NaN
                   grok-2-1212   0.0 23 (100.0%)        NaN        NaN
                   grok-3-beta   0.0 27 (100.0%)        NaN        NaN
meta_llama-4-maverick-instruct   0.0   1 (72.0%) 25 (28.0%)        NaN
   meta_llama-4-scout-instruct   0.0 25 (100.0%)        NaN        NaN
            mistral-large-2411   0.0 25 (100.0%)        NaN        NaN
           mistral-medium-2505   0.0  37 (96.0%)  23 (4.0%)        NaN
            mistral-small-2503   0.0 23 (100.0%)        NaN        NaN
```

### Temperature 0.2

```
                     modelname  temp  Top answer 2nd answer 3rd answer
     claude-3-5-haiku-20241022   0.2  25 (91.0%)  27 (9.0%)        NaN
    claude-3-5-sonnet-20240620   0.2 27 (100.0%)        NaN        NaN
    claude-3-5-sonnet-20241022   0.2 27 (100.0%)        NaN        NaN
    claude-3-7-sonnet-20250219   0.2  27 (99.0%)  25 (1.0%)        NaN
        claude-opus-4-20250514   0.2 23 (100.0%)        NaN        NaN
      claude-sonnet-4-20250514   0.2 27 (100.0%)        NaN        NaN
       deepseek-ai_deepseek-r1   0.2  37 (44.0%) 25 (37.0%)  42 (9.0%)
       deepseek-ai_deepseek-v3   0.2  25 (69.0%) 23 (12.0%)  1 (10.0%)
          gemini-2.0-flash-001   0.2 25 (100.0%)        NaN        NaN
     gemini-2.0-flash-lite-001   0.2 25 (100.0%)        NaN        NaN
  gemini-2.5-pro-preview-03-25   0.2  23 (35.0%) 27 (35.0%) 25 (23.0%)
  gemini-2.5-pro-preview-05-06   0.2  27 (38.0%) 23 (37.0%) 25 (19.0%)
  gemini-2.5-pro-preview-06-05   0.2  37 (63.0%) 27 (18.0%) 25 (15.0%)
google-deepmind_gemma-3-12b-it   0.2 25 (100.0%)        NaN        NaN
google-deepmind_gemma-3-27b-it   0.2 25 (100.0%)        NaN        NaN
 google-deepmind_gemma-3-4b-it   0.2 25 (100.0%)        NaN        NaN
            gpt-4.1-2025-04-14   0.2 27 (100.0%)        NaN        NaN
       gpt-4.1-mini-2025-04-14   0.2 27 (100.0%)        NaN        NaN
       gpt-4.1-nano-2025-04-14   0.2 25 (100.0%)        NaN        NaN
             gpt-4o-2024-05-13   0.2  27 (84.0%) 25 (16.0%)        NaN
             gpt-4o-2024-08-06   0.2  27 (99.0%)  37 (1.0%)        NaN
             gpt-4o-2024-11-20   0.2  25 (50.0%) 27 (50.0%)        NaN
                   grok-2-1212   0.2 23 (100.0%)        NaN        NaN
                   grok-3-beta   0.2 27 (100.0%)        NaN        NaN
meta_llama-4-maverick-instruct   0.2   1 (91.0%)  25 (9.0%)        NaN
   meta_llama-4-scout-instruct   0.2 25 (100.0%)        NaN        NaN
            mistral-large-2411   0.2  25 (99.0%)  27 (1.0%)        NaN
           mistral-medium-2505   0.2  37 (87.0%) 23 (13.0%)        NaN
            mistral-small-2503   0.2  23 (98.0%)  25 (2.0%)        NaN
```

### Temperature 1.0

```commandline
                     modelname  temp  Top answer 2nd answer 3rd answer
     claude-3-5-haiku-20241022   1.0  25 (63.0%) 27 (37.0%)        NaN
    claude-3-5-sonnet-20240620   1.0 27 (100.0%)        NaN        NaN
    claude-3-5-sonnet-20241022   1.0 27 (100.0%)        NaN        NaN
    claude-3-7-sonnet-20250219   1.0  27 (59.0%) 25 (20.0%)  17 (9.0%)
        claude-opus-4-20250514   1.0  23 (70.0%) 27 (18.0%) 37 (11.0%)
      claude-sonnet-4-20250514   1.0 27 (100.0%)        NaN        NaN
       deepseek-ai_deepseek-r1   1.0  37 (51.0%) 25 (26.0%)  17 (9.0%)
       deepseek-ai_deepseek-v3   1.0  25 (35.0%) 23 (22.0%) 37 (13.0%)
          gemini-2.0-flash-001   1.0 25 (100.0%)        NaN        NaN
     gemini-2.0-flash-lite-001   1.0 25 (100.0%)        NaN        NaN
  gemini-2.5-pro-preview-03-25   1.0  25 (48.0%) 27 (30.0%)  23 (8.0%)
  gemini-2.5-pro-preview-05-06   1.0  25 (35.0%) 27 (31.0%) 23 (20.0%)
  gemini-2.5-pro-preview-06-05   1.0  27 (44.0%) 37 (35.0%)  25 (7.0%)
google-deepmind_gemma-3-12b-it   1.0  25 (50.0%) 37 (38.0%) 30 (12.0%)
google-deepmind_gemma-3-27b-it   1.0 25 (100.0%)        NaN        NaN
 google-deepmind_gemma-3-4b-it   1.0 25 (100.0%)        NaN        NaN
            gpt-4.1-2025-04-14   1.0  27 (96.0%)  17 (1.0%)  23 (1.0%)
       gpt-4.1-mini-2025-04-14   1.0  27 (99.0%)  23 (1.0%)        NaN
       gpt-4.1-nano-2025-04-14   1.0  25 (89.0%)  27 (9.0%)  23 (1.0%)
             gpt-4o-2024-05-13   1.0  27 (42.0%) 25 (28.0%)  37 (9.0%)
             gpt-4o-2024-08-06   1.0  27 (77.0%)  25 (6.0%)  37 (4.0%)
             gpt-4o-2024-11-20   1.0  27 (46.0%) 25 (45.0%)  37 (6.0%)
                   grok-2-1212   1.0 23 (100.0%)        NaN        NaN
                   grok-3-beta   1.0  27 (99.0%)  25 (1.0%)        NaN
meta_llama-4-maverick-instruct   1.0   1 (65.0%) 25 (35.0%)        NaN
   meta_llama-4-scout-instruct   1.0 25 (100.0%)        NaN        NaN
            mistral-large-2411   1.0  25 (63.0%) 27 (30.0%)  23 (2.0%)
           mistral-medium-2505   1.0  37 (54.0%) 23 (44.0%)  27 (2.0%)
            mistral-small-2503   1.0  23 (74.0%) 25 (18.0%)  27 (8.0%)
                 o1-2024-12-17   1.0  42 (42.0%) 37 (35.0%)  27 (8.0%)
                 o3-2025-04-16   1.0  37 (66.0%) 27 (15.0%) 17 (11.0%)
```