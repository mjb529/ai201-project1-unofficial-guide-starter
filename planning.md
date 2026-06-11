# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

This project is an unofficial Korea travel guide focused on Seoul restaurants and food-centered activities. The guide emphasizes old, renowned, dish-specific local restaurants, market food, and practical itinerary pairings rather than generic "best restaurants" lists.

This knowledge is valuable because a traveler usually has to piece it together from scattered sources: Korean-language official pages, Michelin entries, food blogs, Reddit threads, YouTube videos, social recommendations, and English travel guides. Official tourism pages can verify locations and history, but they do not always explain which places feel local, which restaurants are splurges versus everyday meals, what dishes to order, or how to combine food stops with nearby activities.

---

## Documents

| # | Source | Description | URL and local file |
|---|--------|-------------|--------------------|
| 1 | Allegra Im / Beli Instagram Seoul seed list | Social recommendation seed list with high-rated Seoul restaurants and Korean retrieval keywords | https://www.instagram.com/p/DYNhqUpmFlb/; `documents/01_allegra_beli_instagram_local_seed.txt` |
| 2 | Michelin Guide: Born and Bred | Premium hanwoo / Korean beef dining source | https://guide.michelin.com/us/en/seoul-capital-area/kr-seoul/restaurant/born-and-bred; `documents/02_michelin_born_and_bred.txt` |
| 3 | Michelin Guide: Gwanghwamun Gukbap | Pork gukbap source with office-district lunch context | https://guide.michelin.com/us/en/seoul-capital-area/kr-seoul/restaurant/gwanghwamun-gukbap; `documents/03_michelin_gwanghwamun_gukbap.txt` |
| 4 | Gangnam Myeonok official + Korean review notes | Hamhung naengmyeon, galbijjim, and mandu source | https://xn--939au0g88jc8l.net/; `documents/04_gangnam_myeonok_official_korean.txt` |
| 5 | Choigane Beoseot Maeuntang Kalguksu local notes | Local/social source for mushroom spicy soup, kalguksu, and fried rice sequence | https://www.instagram.com/p/DW_F0HHEX8W/; `documents/05_choigane_mushroom_kalguksu_korean_local.txt` |
| 6 | Michelin Guide: Escondido | Contemporary / Mexican-influenced Seoul fine-dining source | https://guide.michelin.com/us/en/seoul-capital-area/kr-seoul/restaurant/escondido; `documents/06_michelin_escondido.txt` |
| 7 | Myongwolgwan Korean blog + YouTube notes | Upscale Walkerhill Korean barbecue source | https://daisy3690.tistory.com/113; `documents/07_myongwolgwan_korean_blog_youtube.txt` |
| 8 | Imun Seolnongtang Michelin + Korean heritage notes | Historic seolleongtang / old Seoul restaurant source | https://guide.michelin.com/kr/ko/seoul-capital-area/kr-seoul/restaurant/imun-seolnongtang; `documents/08_imun_seolnongtang_michelin_korean.txt` |
| 9 | Hadongkwan Michelin + Korean local notes | Historic Myeongdong gomtang source | https://guide.michelin.com/kr/ko/seoul-capital-area/kr-seoul/restaurant/hadongkwan; `documents/09_hadongkwan_michelin_korean.txt` |
| 10 | Woo Lae Oak Michelin + Visit Seoul notes | Pyongyang naengmyeon and Euljiro old-restaurant source | https://guide.michelin.com/kr/ko/seoul-capital-area/kr-seoul/restaurant/woo-lae-oak; `documents/10_wooraeok_michelin_visitseoul_korean.txt` |
| 11 | Jinju Hoegwan Visit Seoul + blog/news notes | Kongguksu / summer noodle source | https://korean.visitseoul.net/restaurants/%EC%A7%84%EC%A3%BC%ED%9A%8C%EA%B4%80-K/KOP012654; `documents/11_jinju_hoegwan_korean_visitseoul_blog.txt` |
| 12 | Andongjang Visit Seoul source | Old Chinese-Korean restaurant and oyster jjamppong source | https://english.visitseoul.net/area/Andongjang-E/ENP012838; `documents/12_andongjang_visitseoul_old_chinese.txt` |
| 13 | Yeokjeon Hoegwan Visit Seoul source | Historic Mapo crispy bulgogi and makgeolli source | https://english.visitseoul.net/area/yukjeon/ENPz0vpvy; `documents/13_yeokjeon_hoegwan_visitseoul.txt` |
| 14 | Gwangjang Market local food sources | Market food and activity source for bindaetteok, mayak gimbap, yukhoe, kalguksu, and mandu | https://www.bonappetit.com/story/mayak-kimbap; `documents/14_gwangjang_market_local_food_sources.txt` |
| 15 | Euljiro back alleys Visit Korea article | Activity source for old Seoul alleys, Seun Sangga, Cheonggyecheon, and old restaurants | https://korean.visitkorea.or.kr/detail/rem_detail.do?cotid=089a4363-ae72-4b0c-840f-7d05ae4db98d; `documents/15_euljiro_back_alley_korean_visitkorea.txt` |
| 16 | Eater 38 Seoul filtered notes | Broad English-language food-guide cross-check | https://www.eater.com/maps/best-seoul-restaurants-38; `documents/16_eater_38_seoul_filtered.txt` |
| 17 | The Infatuation Seoul filtered notes | Traveler-facing restaurant scenario and neighborhood source | https://www.theinfatuation.com/seoul/guides/best-restaurants-seoul; `documents/17_infatuation_seoul_filtered.txt` |
| 18 | Reddit r/koreatravel food threads | Crowd-sourced practical travel questions and restaurant discussion source | https://www.reddit.com/r/koreatravel/comments/16uvtur/great_restaurants_in_myeongdong/; `documents/18_reddit_koreatravel_food_threads.txt` |
| 19 | YouTube Seoul food vlog notes | Video/social source for food-crawl patterns and experience descriptions | https://www.youtube.com/results?search_query=seoul+old+restaurant+food+vlog; `documents/19_youtube_seoul_food_vlogs_filtered.txt` |
| 20 | Visit Seoul official food/activity pages | Official tourism source for restaurants, activities, neighborhoods, and itinerary pairings | https://english.visitseoul.net/restaurants; `documents/20_visitseoul_food_activities_korean_official.txt` |

---

## Chunking Strategy

**Chunk size:** 700 characters target size per chunk, using paragraph-aware splitting before falling back to sentence/character splitting.

**Overlap:** 150 characters between adjacent chunks from the same source.

**Reasoning:** The documents are short-to-medium structured notes, not long PDFs. Most useful facts appear in compact sections: restaurant name, dish, neighborhood, how to recommend it, and Korean keywords. A 700-character target should usually keep one complete restaurant/activity idea together without mixing too many unrelated restaurants in the same embedding. The 150-character overlap helps when the source transitions from dish description to recommendation guidance, so a query can still retrieve the restaurant name and the relevant advice together. During implementation I will inspect sample chunks; if the corpus produces fewer than 50 chunks, I may lower the target size or add source-title metadata to every chunk, then update this section.

---

## Retrieval Approach

**Embedding model:** `sentence-transformers/all-MiniLM-L6-v2`

**Top-k:** 5 retrieved chunks per query.

**Weak-retrieval behavior:** The system should expose distance scores during retrieval testing and refuse to answer when retrieved context is clearly off-topic. In the generation layer, the prompt will instruct the LLM to say it does not have enough information if the answer is not supported by the retrieved chunks. The implementation should also allow a distance threshold to be tuned after the first retrieval tests.

**Production tradeoff reflection:** `all-MiniLM-L6-v2` is a good project model because it runs locally, is fast, and does not require paid embedding API usage. For a production Korea travel guide, I would compare it against stronger multilingual or domain-robust embedding models because this corpus mixes English, romanized Korean, and Korean text such as `평양냉면`, `곰탕`, and `광장시장`. I would weigh retrieval accuracy on Korean restaurant names, context length, latency, hosting cost, and whether an API model performs better on short social-review style text. If users asked many Korean-language queries, multilingual quality would matter more than local speed.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Which Seoul restaurant should I choose if I want one of the oldest local soup institutions near Jongno or Insadong? | Imun Seolnongtang should be recommended because the corpus describes it as one of Seoul/Korea's oldest restaurants, associated with seolleongtang, Seoul permit number one, Jongno/Insadong context, and table seasoning with salt, pepper, scallion, or kimchi. |
| 2 | I am staying in Myeongdong and want a classic old beef soup instead of a tourist-trap meal. What should I eat? | Hadongkwan should be recommended because it is a Myeongdong gomtang institution dating to 1939, with a clean but deep beef soup. The answer may contrast gomtang with milkier seolleongtang. |
| 3 | What is a good summer-specific noodle dish in Seoul, and where should I try it? | Jinju Hoegwan should be recommended for kongguksu, cold soybean noodles, especially in hot weather near City Hall / Deoksugung / Namdaemun. |
| 4 | What cold noodle place should I try in Seoul, and how are the styles different? | The answer should retrieve naengmyeon sources and distinguish Woo Lae Oak as Pyongyang naengmyeon, which is subtler and broth-focused, from Gangnam Myeonok as Hamhung-style naengmyeon, which is associated with chewy noodles and spicy mixed style. |
| 5 | What place should I choose for a high-budget hanwoo splurge, and what should I not expect from it? | Born and Bred should be recommended for premium hanwoo / polished beef dining / special occasion. The answer should say it is not an old street-level local restaurant, cheap eat, or casual market meal. |

---

## Anticipated Challenges

1. Korean and English naming variation may hurt retrieval. A user might search for "cold noodles," "naengmyeon," `냉면`, "Pyongyang noodles," or a romanized restaurant name, and the embedding model may not always connect all variants. To reduce this risk, each document includes Korean keywords and English explanations, and chunks should preserve source titles and restaurant names.

2. Broad guide sources could overpower specific local sources. Documents like Eater, Infatuation, Reddit, and YouTube are useful, but they are less authoritative for old-restaurant history than Korean official pages, Michelin Korean entries, and Visit Seoul/Korea pages. The retrieval and final evaluation should check whether old-local queries return sources like Imun Seolnongtang, Hadongkwan, Woo Lae Oak, Jinju Hoegwan, Andongjang, Yeokjeon Hoegwan, or Euljiro rather than only generic travel-guide chunks.

3. Some restaurant files are transformed notes rather than full copied articles. That is acceptable for a manually collected text corpus, but the README must be transparent about the collection/cleaning process. The system should not make claims stronger than the notes support, especially for social sources, YouTube summaries, and Instagram/Beli seed ratings.

---

## Architecture

```mermaid
flowchart LR
    A[Document Ingestion<br/>Python pathlib reads .txt files<br/>from documents/] --> B[Cleaning + Chunking<br/>strip metadata labels when needed<br/>paragraph-aware 700 char chunks<br/>150 char overlap]
    B --> C[Embedding + Vector Store<br/>sentence-transformers<br/>all-MiniLM-L6-v2<br/>ChromaDB local collection]
    C --> D[Retrieval<br/>top-k = 5<br/>return chunk text, distance,<br/>source filename, title]
    D --> E[Generation<br/>Groq llama-3.3-70b-versatile<br/>answer only from retrieved context<br/>append visible source attribution]
    E --> F[Query Interface<br/>Gradio or CLI<br/>question in, answer + sources out]
```

---

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:** I will use Codex to help implement the ingestion/chunking script. I will give it the Documents and Chunking Strategy sections from this plan and ask it to load every `.txt` file in `documents/`, keep source metadata, clean repeated labels if necessary, and produce paragraph-aware chunks near 700 characters with 150 characters of overlap. I will verify the output by printing the total chunk count and at least 5 labeled sample chunks, checking that each chunk is readable, source-attributed, and not just metadata or a sentence fragment.

**Milestone 4 — Embedding and retrieval:** I will use Codex to implement ChromaDB storage and semantic retrieval. I will give it the Retrieval Approach section and architecture diagram, and ask for code that embeds chunks with `sentence-transformers/all-MiniLM-L6-v2`, stores text plus metadata in ChromaDB, and retrieves the top 5 chunks with distance scores. I will verify it with at least 3 evaluation queries before connecting the LLM, checking that retrieved chunks visibly answer the question.

**Milestone 5 — Generation and interface:** I will use Codex to wire retrieval into Groq generation and a simple query interface. I will give it the grounding requirement, the Evaluation Plan, and the architecture diagram. I expect it to produce an `ask()` function and either a Gradio or CLI interface that returns an answer plus visible source list. I will verify that the prompt tells the model to answer only from retrieved context, that source attribution is appended or enforced structurally, and that an out-of-scope query produces a refusal instead of a made-up travel answer.
