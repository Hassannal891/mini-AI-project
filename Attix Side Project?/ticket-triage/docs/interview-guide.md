# Explain this project confidently

## A 60-second explanation

“I built a Python support-ticket triage service. It takes a customer message and suggests one of four support queues. I normalize the text and use TF-IDF features with logistic regression. The preprocessing and model are saved together, and FastAPI loads them at startup. The response includes class scores and a human-review flag. I evaluate on a separate synthetic test set using macro-F1, per-class metrics and a simple baseline, and also measure how many tickets would be automatically routed. The project includes API tests, a browser demo, and a Docker deployment configuration. The important limitation is that synthetic-data scores do not establish real-world usefulness.”

Say “I deployed it” only after actually running it on your target host. Read and run the code before presenting the implementation as work you understand; be transparent about AI assistance when asked.

## Walk through one request

1. The browser sends JSON to `POST /predict`.
2. Pydantic rejects empty, numeric-only, or excessively long text.
3. The saved TF-IDF step applies Unicode normalization, lowercasing, email/URL substitution and whitespace cleanup, then transforms words and bigrams using the training vocabulary.
4. Logistic regression computes scores across four classes.
5. The service picks the highest-scoring class and requests review if its score is below 0.55 or no vocabulary features are present.
6. FastAPI returns the category, scores, review reason and model version. The browser displays these using text content.

## Decisions you should be able to defend

**Why not an LLM?** The task is narrow supervised classification. This baseline is cheap, reproducible and easy to inspect. An LLM might handle richer semantics or unseen categories better, but would introduce different cost, latency, privacy and evaluation questions. Compare alternatives on the same representative dataset before choosing.

**Where is preprocessing fitted?** Normalization is deterministic. Vocabulary and inverse document frequencies are fitted only on the training split, inside the pipeline. Test tickets are transformed using that learned vocabulary.

**Why macro-F1?** It gives each category equal importance. Accuracy alone can hide poor minority-class performance. This demo is balanced, but production usually is not.

**How do you avoid leakage?** Separate source files, normalized duplicate checks, and training-only feature fitting. These checks do not detect every semantic paraphrase. Real data needs grouping by customer/conversation and temporal separation.

**What is the threshold doing?** It trades automation coverage against review volume. The current value is illustrative, not validated for a business outcome. Tune the policy on validation data using misrouting costs and reviewer capacity, then evaluate once on a final test set.

**Are the scores trustworthy?** They are model outputs, not calibrated certainty. The model has no general understanding of language and can be confidently wrong, especially outside its training domain. Zero vocabulary overlap is only a basic fallback, not comprehensive out-of-domain detection.

**What is tested?** Representative category predictions, invalid input, normalization, split separation, unknown-token review, forced low-score review, startup failure without a model, health/demo endpoints and saved-model prediction parity.

**How is it deployed?** The Docker image builds the model from versioned training data, then runs Uvicorn as a non-root user. CI trains/tests and smoke-tests the image. In a larger system, training and serving would be separate pipelines, with an artifact registry and promotion criteria.

## A five-minute demo

1. Start the server and open `/docs` or the demo homepage.
2. Submit a billing complaint and explain the JSON response.
3. Submit `quasarzz nebulaqq` to show the unknown-vocabulary fallback.
4. Submit an invalid message to show validation.
5. Open `reports/evaluation.json`: compare baseline, macro-F1, coverage, and mistakes.
6. Show the Dockerfile and workflow. Distinguish tested local behavior from unverified hosted deployment.

## Next improvements, in order

Collect permitted representative tickets and agree a labeling rubric. Add a validation set and time/customer-separated test set. Analyze misroutes and multi-intent messages. Compare a stronger baseline or embeddings. Calibrate scores and set a review policy based on costs. Then add operational monitoring and an authenticated deployment. These steps matter more than adding an LLM without evidence.
