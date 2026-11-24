# Cat Agent 🐱

A command-line AI agent that answers questions about cats. It is built with [Pydantic AI](https://ai.pydantic.dev/) on Google's **Gemini 2.5 Flash** model and uses **tool calling** to retrieve live data from [The Cat API](https://thecatapi.com/), then composes its answer from the results.

## How it works

```text
 Question ──> Pydantic AI agent ──> Gemini 2.5 Flash
                    │                      │
                    │            decides a tool is needed
                    ▼                      │
              Tool function  <─────────────┘
                    │
                    ▼
          The Cat API (api.thecatapi.com)
                    │
                    ▼
        Structured result returned to the model
                    │
                    ▼
            Final answer printed in the terminal
```

1. The user asks a question on the command line.
2. The agent sends the question to Gemini 2.5 Flash, along with the descriptions of the tools it can call.
3. When the question needs cat data (breeds, temperament, origin, etc.), the model calls a tool, which queries The Cat API.
4. The API response is passed back to the model, which writes the answer grounded in that data.

**Why tool calling?** Grounding answers in an external API reduces reliance on the model's memory and keeps the facts traceable to a source.

## Prerequisites

- Python [3.10+]
- A **Google Account**
- A **Google API key** for the Gemini API, created in [Google AI Studio](https://aistudio.google.com/)
- A **Cat API key**, available free at [thecatapi.com](https://thecatapi.com/)

## Setup & Configuration

```bash
1. git clone https://github.com/[gitonthecloud]/all-about-cats.git
2. cd all-about-cats
3. python -m venv .venv
4. source .venv/bin/activate        # Windows: .venv\Scripts\activate
5. pip install -r requirements.txt
6. Provide your keys as environment variables (or in a `.env` file, which is git-ignored):
    export GOOGLE_API_KEY="your-google-api-key"
    export CAT_API_KEY="your-cat-api-key"
```

> 🔒 Never commit API keys. Make sure `.env` is listed in `.gitignore`.

## Usage

```bash
python -m cat-agent
Ask me about cat breeds (type 'exit' to quit):

At the above prompt, type a question e.g. "Tell me about British Shorthair"

+++++++++

python -m cat-agent
Ask me about cat breeds (type 'exit' to quit): What is so special about Egyption cats?

[...agent's answer...]
The Egyptian Mau is a medium-sized, muscular, and naturally spotted cat breed with distinctive gooseberry-green eyes. It's one of the oldest domestic cat breeds, possibly descended from ancient Egyptian cats, and is the only naturally spotted domestic breed. Their name 'Mau' is the Egyptian word for cat. They are known for being agile, dependent, gentle, intelligent, lively, loyal, playful, and devoted.

```

## Testing and Evaluation

The agent was manually tested with a handful of questions and the results were evaluated. Please refer to [Evaluation.md](Evaluation.md) for details.


## Limitations

- **Daily quota:** the Gemini free tier limits the agent to **20 queries per day**. Further requests will fail until the quota resets.
- **Data scope:** answers are only as good as the data The Cat API provides. Questions outside its coverage may get general or incomplete answers.
- **Command line only:** there is no web interface, and the application is **not deployed** anywhere yet.
- **Requires two API keys** (Google and The Cat API) to run.

## Project structure

```text
├── cat-agent.py             # CLI entry point
├── .env.example             # example of .env file
├── .gitignore               # gitignore file
├── LICENSE.txt              # license file
├── README.md                # Readme file
├── requirements.txt         # system requirements
├── tests                    # tests
│   ├── data                 # test data files
│   ├── test_results.csv     # test result
│   ├── test_score.csv       # test scores
│   └── test_tools.py        # testing for tools.py
└── tools.py                 # Cat API tool functions
```

## Possible future work

- Deploy as a web app or API
- Add tests with mocked Cat API responses
- Add response caching to conserve the daily quota
- Support additional tools (e.g. cat images, facts)
- Define structured output using Pydantic BaseModel
- Use pydantic-evals (LLM-as-judge) in the scoring of test reults
- Automate the scoring of test results

## Licence
© 2026 Swee Hing Lee (All rights reserved)

This repository is publicly viewable for portfolio and evaluation purposes only; it is not open source.


