import cohere
from dotenv import load_dotenv
import os
from annoy import AnnoyIndex
import numpy as np
import pandas as pd
from utils import preprocess
import openai

openai.api_key = os.getenv("OPENAI_KEY")

load_dotenv()

co = cohere.Client(os.getenv("COHERE_KEY"))


def calculate_embedding(df, query):
    embeds = co.embed(
        texts=list(df["content"].values), model="embed-english-v2.0"
    ).embeddings
    search_index = AnnoyIndex(np.array(embeds).shape[1], "angular")

    for i in range(len(embeds)):
        search_index.add_item(i, embeds[i])
    search_index.build(10)

    query = preprocess(query)
    query_embed = co.embed(texts=[query], model="embed-english-v2.0").embeddings
    similar_item_ids = search_index.get_nns_by_vector(
        query_embed[0], 10, include_distances=True
    )

    results = pd.DataFrame(
        {
            "texts": df.iloc[similar_item_ids[0]]["content"],
            "distance": similar_item_ids[1],
        }
    )

    summary = None
    if len(results.iloc[0]["texts"]) > 250:
        response = co.summarize(
            text=results.iloc[0]["texts"],
            model="command",
            length="short",
            extractiveness="high",
        )

        summary = response.summary
    prompt = f"""Generate statement from the answer using 2nd person pov

question: {query}
answer: {summary if summary is not None else results.iloc[0]["texts"]}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]
