# Data card

80 training and 24 held-out test examples, authored synthetically for this project. Four balanced English categories. No customer records or external dataset were used. The test examples were authored separately; no automated random splitting or paraphrase generation is used. Exact normalized duplicates across splits are rejected during training.

This tiny, clean dataset tests the implementation, not commercial usefulness. Shared topic vocabulary and one author make the test optimistic. It does not represent multilingual messages, multi-intent tickets, abuse, production class imbalance, or changing products. Do not report these scores as customer-data results. For a real pilot, obtain permission to use anonymized tickets, label with a written rubric, split by customer and time, tune on a validation set, and preserve a final untouched test set.

Labels: billing = charges/payments/invoices; account = login/identity access; cancellation = ending a plan/renewal; technical = product malfunction. Multiple intents should be manually reviewed in a production system; this baseline cannot reliably detect them.
