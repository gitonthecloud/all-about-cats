## Evaluation

Since the agent gets its data from an external API, the API is the source of truth. This situation faciliates an important test: whether the agent answers from the tool or makes things up from the model's own knowledge.

To execute this test, I have created a number of questions covering a range of categories:

| Category	    | Test Purpose	|
|---------------|---------------|
| Direct lookup	| Basic tool use |
| Multi field	| Extracting several values correctly |
| Comparison    | Reasoning over retrieved data |
| Missing data	| Telling the truth instead of inventing it |
| Messy input	| Robustness (mispell, mix capitalisation) |
| Off-topic	    | Staying in scope |

The answers to the questions are retrieved directly from the CAT API and used as a baseline. These questions will be fed into the agent and its responses will be collected and compared against the baseline.

There are a number of ways to do the comparison, for example,
* by exact match
* assessed against a rubric
* use an LLM to judge the output

In this test, I will use a number of criteria to determine the quality of the outputs:
| Check Type	| Purpose	    |
|---------------|---------------|
| Content	    | Does the answer include the expected value? |
| Numeric	    | Is the number within a tolerance? |
| Tool-use	    | Did the agent actually call the API, and with sensible arguments? |
| No-call	    | For missing-data and off-topic cases, does the agent reply with a "can't find" answer? |

### Test Results

| Category      | Test Purpose                              | Result   |
|:--------------|:------------------------------------------|:---------|
| Comparison    | Reasoning over retrieved data             | 0/1      |
| Direct lookup | Basic tool use                            | 4/4      |
| Messy input   | Robustness                                | 3/3      |
| Missing data  | Telling the truth instead of inventing it | 1/1      |
| Multi field   | Extract several values correctly          | 0/1      |
| Off-topic     | Staying in scope                          | 1/1      |

Due to the free tier quota limit on the Google API, only a small number of questions can be asked. In the above test, The "Comparison" and "Multi field" categories were not tested due to the limit.


### How well did the agent perform?

|    | Check Type   | Purpose                                                                                | Result   |
|---:|:-------------|:---------------------------------------------------------------------------------------|:---------|
|  0 | Content      | Does the answer include the expected value?                                            | Yes      |
|  1 | Numeric      | Is the number within a tolerance?                                                      | nan      |
|  2 | Tool-use     | Did the agent actually call the API, and with sensible arguments?                      | Yes      |
|  3 | No-call      | For missing-data and off-topic cases, does the agent reply with a "can't find" answer? | Yes      |

The results are promising in the other categories. It can be seen that direct lookup of information appears to be working properly. Messy input such as mispelled breed name and mixed capitalisation of breed name are handled correctly. When the agent is given a non existent breed name, it could not find any relevant information and reported accordingly. When it is being asked an unrelated topic, it also reported appropriately. The agent had also used the expected tool/functions to extract data from the CAT API.

### What next?

Due to the extremely small test result set, no meaningful conclusion can be drawn about the performance of the agent at the moment. More test results should be collected for further analysis.
