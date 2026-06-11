# The Unofficial Guide: Seoul Food and Activities

## Domain

This project is an unofficial Korea travel guide focused on Seoul restaurants and food-centered activities. It emphasizes old, renowned, dish-specific local restaurants, market food, and practical itinerary pairings instead of generic "best restaurants" lists.

This information is hard to find in one official place because it is scattered across Korean-language tourism pages, Michelin entries, Korean blogs, Reddit threads, YouTube food videos, Instagram/Beli-style social recommendations, and English travel guides. Official sources can verify locations and history, but they rarely explain which places feel local, what dish to order, which places are splurges, or how to combine restaurants with nearby activities.

## Document Sources

The corpus contains 20 manually collected `.txt` source-note documents in `documents/`. These are not live scrapes; I transformed public source material into structured notes with titles, URLs, source type, collection date, cleaning notes, and retrieval-friendly English/Korean keywords.

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Allegra Im / Beli Instagram Seoul seed list | Social recommendation seed | https://www.instagram.com/p/DYNhqUpmFlb/; `documents/01_allegra_beli_instagram_local_seed.txt` |
| 2 | Michelin Guide: Born and Bred | Michelin restaurant entry | https://guide.michelin.com/us/en/seoul-capital-area/kr-seoul/restaurant/born-and-bred; `documents/02_michelin_born_and_bred.txt` |
| 3 | Michelin Guide: Gwanghwamun Gukbap | Michelin restaurant entry | https://guide.michelin.com/us/en/seoul-capital-area/kr-seoul/restaurant/gwanghwamun-gukbap; `documents/03_michelin_gwanghwamun_gukbap.txt` |
| 4 | Gangnam Myeonok official + Korean review notes | Official site + Korean review notes | https://xn--939au0g88jc8l.net/; `documents/04_gangnam_myeonok_official_korean.txt` |
| 5 | Choigane Beoseot Maeuntang Kalguksu notes | Korean local/social notes | https://www.instagram.com/p/DW_F0HHEX8W/; `documents/05_choigane_mushroom_kalguksu_korean_local.txt` |
| 6 | Michelin Guide: Escondido | Michelin restaurant entry | https://guide.michelin.com/us/en/seoul-capital-area/kr-seoul/restaurant/escondido; `documents/06_michelin_escondido.txt` |
| 7 | Myongwolgwan blog and YouTube notes | Korean blog + YouTube notes | https://daisy3690.tistory.com/113; `documents/07_myongwolgwan_korean_blog_youtube.txt` |
| 8 | Imun Seolnongtang Michelin + Korean heritage notes | Michelin + Korean heritage notes | https://guide.michelin.com/kr/ko/seoul-capital-area/kr-seoul/restaurant/imun-seolnongtang; `documents/08_imun_seolnongtang_michelin_korean.txt` |
| 9 | Hadongkwan Michelin + Korean review notes | Michelin + Korean review notes | https://guide.michelin.com/kr/ko/seoul-capital-area/kr-seoul/restaurant/hadongkwan; `documents/09_hadongkwan_michelin_korean.txt` |
| 10 | Woo Lae Oak Michelin + Visit Seoul notes | Michelin + Visit Seoul notes | https://guide.michelin.com/kr/ko/seoul-capital-area/kr-seoul/restaurant/woo-lae-oak; `documents/10_wooraeok_michelin_visitseoul_korean.txt` |
| 11 | Jinju Hoegwan Visit Seoul + blog/news notes | Visit Seoul + Korean blog/news | https://korean.visitseoul.net/restaurants/%EC%A7%84%EC%A3%BC%ED%9A%8C%EA%B4%80-K/KOP012654; `documents/11_jinju_hoegwan_korean_visitseoul_blog.txt` |
| 12 | Andongjang Visit Seoul source | Official Visit Seoul page | https://english.visitseoul.net/area/Andongjang-E/ENP012838; `documents/12_andongjang_visitseoul_old_chinese.txt` |
| 13 | Yeokjeon Hoegwan Visit Seoul source | Official Visit Seoul page | https://english.visitseoul.net/area/yukjeon/ENPz0vpvy; `documents/13_yeokjeon_hoegwan_visitseoul.txt` |
| 14 | Gwangjang Market food sources | Market guide + food/social notes | https://www.bonappetit.com/story/mayak-kimbap; `documents/14_gwangjang_market_local_food_sources.txt` |
| 15 | Euljiro back alleys Visit Korea article | Official Visit Korea article | https://korean.visitkorea.or.kr/detail/rem_detail.do?cotid=089a4363-ae72-4b0c-840f-7d05ae4db98d; `documents/15_euljiro_back_alley_korean_visitkorea.txt` |
| 16 | Eater 38 Seoul filtered notes | English food guide | https://www.eater.com/maps/best-seoul-restaurants-38; `documents/16_eater_38_seoul_filtered.txt` |
| 17 | The Infatuation Seoul filtered notes | English restaurant guide | https://www.theinfatuation.com/seoul/guides/best-restaurants-seoul; `documents/17_infatuation_seoul_filtered.txt` |
| 18 | Reddit r/koreatravel food threads | Crowd-sourced forum notes | https://www.reddit.com/r/koreatravel/comments/16uvtur/great_restaurants_in_myeongdong/; `documents/18_reddit_koreatravel_food_threads.txt` |
| 19 | YouTube Seoul food vlog notes | Video/social source notes | https://www.youtube.com/results?search_query=seoul+old+restaurant+food+vlog; `documents/19_youtube_seoul_food_vlogs_filtered.txt` |
| 20 | Visit Seoul food/activity pages | Official tourism guide | https://english.visitseoul.net/restaurants; `documents/20_visitseoul_food_activities_korean_official.txt` |

## Chunking Strategy

**Chunk size:** 700 characters target size.  
**Overlap:** 150 characters.  
**Final chunk count:** 60 chunks across 20 documents.

The ingestion pipeline in `ingest.py` loads every `.txt` file, extracts metadata fields such as `TITLE`, `SOURCE_TYPE`, and `URL`, cleans whitespace, then chunks the `DOCUMENT_TEXT` section. I used paragraph-aware chunking first, then sentence splitting for long paragraphs, because the corpus is made of short structured notes rather than long PDFs. A 700-character target usually keeps one complete restaurant/activity idea together, while 150 characters of overlap helps preserve transitions from dish description to recommendation guidance.

### Sample Chunks

1. `documents/08_imun_seolnongtang_michelin_korean.txt`: Imun Seolnongtang is recommended for old Seoul, historical restaurants, soup, breakfast/lunch, gentle flavors, and a pre/post Insadong or Jongno walk. The chunk explains table seasoning with salt, pepper, scallion, or kimchi.

2. `documents/09_hadongkwan_michelin_korean.txt`: Hadongkwan is useful in Myeongdong where travelers may want a historically meaningful alternative to tourist restaurants. The chunk recommends gomtang, old Myeongdong, central lunch, and no-nonsense Korean beef soup.

3. `documents/11_jinju_hoegwan_korean_visitseoul_blog.txt`: Jinju Hoegwan is described as a top summer answer for kongguksu, cold noodles in thick soy-milk broth. The chunk emphasizes soybean quality, texture, temperature, and noodle chew.

4. `documents/10_wooraeok_michelin_visitseoul_korean.txt`: Woo Lae Oak is described as essential for understanding Pyongyang naengmyeon: chilled broth, buckwheat noodles, restrained seasoning, and quiet beef aroma.

5. `documents/02_michelin_born_and_bred.txt`: Born and Bred is recommended for high-budget users, omakase-style beef, special occasions, hanwoo education, and luxury dining, but not for old local nopos, cheap eats, solo budget meals, or street food.

## Embedding Model

**Model used:** `sentence-transformers/all-MiniLM-L6-v2`

I chose this model because it runs locally, is fast, and does not require paid embedding API calls. In production, I would compare it against stronger multilingual embedding models because this corpus mixes English, romanized Korean, and Korean terms such as `평양냉면`, `곰탕`, and `광장시장`. The main tradeoffs would be Korean-language retrieval accuracy, context length, latency, hosting cost, and whether an API-hosted model handles short review/social text better than a small local model.

## Retrieval

The vector store uses ChromaDB in `chroma_db/`. `query.py --build` embeds the chunks and stores chunk text plus metadata: title, source type, URL, source file, and chunk index. Retrieval uses semantic search with top-k = 5, then applies a small keyword rerank for clear user intent terms such as "Myeongdong," "summer," "hanwoo," and "cold noodle." I added this rerank after testing showed that semantic-only retrieval sometimes ranked a generally related soup/noodle source above the exact restaurant source.

### Retrieval Test Examples

**Query 1:** "Which Seoul restaurant should I choose if I want one of the oldest local soup institutions near Jongno or Insadong?"

Top returned chunks included:
- Imun Seolnongtang, distance 0.5408: recommends it for old Seoul, historical restaurants, soup, and a pre/post Insadong or Jongno walk.
- Andongjang, distance 0.5070: old Seoul Chinese-Korean food near Euljiro/Jongno.
- Visit Seoul official guide, distance 0.6726: pairs Imun Seolnongtang with Insadong/Jogyesa/Jongno.

Why relevant: Imun Seolnongtang directly answers the old soup/Jongno/Insadong part of the query. Andongjang is only partially relevant because it matches old Seoul and Jongno, but the dish is oyster jjamppong rather than the intended soup institution.

**Query 2:** "I am staying in Myeongdong and want a classic old beef soup instead of a tourist-trap meal. What should I eat?"

Top returned chunks included:
- Hadongkwan, distance 0.9994: says it is useful in Myeongdong for travelers avoiding tourist restaurants and recommends gomtang / old Myeongdong / no-nonsense Korean beef soup.
- Hadongkwan, distance 0.8866: describes it as an important beef-soup institution with 80+ years of history.
- Choigane mushroom kalguksu, distance 0.7473: related Korean comfort soup/noodle content but not the best answer.

Why relevant: The top Hadongkwan chunk directly contains Myeongdong, tourist restaurants, gomtang, and beef soup, so retrieval succeeds despite one off-topic comfort-soup chunk.

**Query 3:** "What is a good summer-specific noodle dish in Seoul, and where should I try it?"

Top returned chunks included:
- Jinju Hoegwan, distance 0.6247: recommends kongguksu as a summer Seoul dish.
- Andongjang, distance 0.6117: off-target old noodle/soup source.
- Woo Lae Oak, distance 0.6143: cold noodle source, relevant to noodles but not summer-specific.

Why relevant: The top chunk directly supports Jinju Hoegwan and kongguksu. The second and third chunks show the system's weakness with broad "noodle" language, which can pull in other noodle sources.

## Grounded Generation

**System prompt grounding instruction:**

```text
You are a grounded RAG assistant for an unofficial Seoul restaurant and activity guide. Answer using only the provided retrieved context. Do not use outside knowledge. If the context does not contain enough information, say exactly: "I don't have enough information in the collected documents to answer that." Cite source numbers like [1] or [2] in the answer whenever you make a claim.
```

Source attribution is surfaced in two ways: the model is instructed to cite source numbers in the answer, and `query.py` also returns a programmatic source list containing source title, local file, and URL. The app displays answer, sources, and retrieved chunks as separate fields.

### Example Responses

**Question:** "I am staying in Myeongdong and want a classic old beef soup instead of a tourist-trap meal. What should I eat?"

**Answer:** The system recommended Hadongkwan for gomtang in Myeongdong, explaining that it is a historically meaningful alternative to tourist restaurants and that gomtang is clearer and beefier than milkier seolleongtang. It cited Hadongkwan chunks in the answer.

**Visible sources:** Hadongkwan Michelin/Korean review source, Choigane mushroom kalguksu source, Myongwolgwan source, and Imun Seolnongtang source.

**Question:** "What place should I choose for a high-budget hanwoo splurge, and what should I not expect from it?"

**Answer:** The system recommended Born and Bred for a premium hanwoo splurge, describing it as a curated beef/omakase-style experience. It warned not to expect an old local nopo, cheap eat, solo budget meal, or street food.

**Visible sources:** Michelin Guide: Born and Bred; Yeokjeon Hoegwan; Allegra/Beli seed list.

**Out-of-scope question:** "What is the best ski resort in Busan?"

**Refusal response:** "I don't have enough information in the collected documents to answer that."

## Query Interface

The project includes both a CLI and a Gradio UI.

Setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# add GROQ_API_KEY to .env
python query.py --build
```

CLI usage:

```bash
python query.py "What cold noodle place should I try in Seoul, and how are the styles different?"
```

Gradio usage:

```bash
python app.py
```

Then open `http://127.0.0.1:8008`.

The interface has one input field, `Question`, and three output fields: `Answer`, `Sources`, and `Retrieved chunks`.

Sample interaction transcript:

```text
Input:
What is a good summer-specific noodle dish in Seoul, and where should I try it?

Answer:
For a good summer-specific noodle dish in Seoul, try kongguksu at Jinju Hoegwan. The retrieved context describes kongguksu as cold noodles in a thick soy-milk broth and frames Jinju Hoegwan as a strong summer recommendation near City Hall / Deoksugung / Namdaemun.

Sources:
Jinju Hoegwan: Visit Seoul Korean + Korean food blog/news
documents/11_jinju_hoegwan_korean_visitseoul_blog.txt
```

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which Seoul restaurant should I choose if I want one of the oldest local soup institutions near Jongno or Insadong? | Imun Seolnongtang near Jongno/Insadong; old Seoul seolleongtang institution. | Recommended Imun Seolnongtang and also mentioned Hadongkwan. | Relevant | Partially accurate |
| 2 | I am staying in Myeongdong and want a classic old beef soup instead of a tourist-trap meal. What should I eat? | Hadongkwan for Myeongdong gomtang, dating to 1939 / 80+ years. | Recommended Hadongkwan, explained gomtang, Myeongdong usefulness, and old beef-soup context. | Relevant | Accurate |
| 3 | What is a good summer-specific noodle dish in Seoul, and where should I try it? | Jinju Hoegwan for kongguksu, especially in hot weather near City Hall / Deoksugung / Namdaemun. | Recommended kongguksu at Jinju Hoegwan and explained cold soy-milk broth. | Partially relevant | Accurate |
| 4 | What cold noodle place should I try in Seoul, and how are the styles different? | Woo Lae Oak for subtle Pyongyang naengmyeon; Gangnam Myeonok for Hamhung-style naengmyeon. | Recommended Woo Lae Oak and mentioned Gangnam Myeonok, but relied mostly on Woo Lae Oak context. | Partially relevant | Partially accurate |
| 5 | What place should I choose for a high-budget hanwoo splurge, and what should I not expect from it? | Born and Bred for premium hanwoo; not cheap, old street-level local, or market food. | Recommended Born and Bred and warned it is modern, expensive, and not a cheap nopo/street-food option. | Relevant | Accurate |

Full raw outputs are saved in `data/evaluation_results.json`.

## Failure Case Analysis

**Question that failed:** "What cold noodle place should I try in Seoul, and how are the styles different?"

**What the system returned:** The answer correctly recommended Woo Lae Oak for Pyongyang naengmyeon and mentioned Gangnam Myeonok as a contrast, but the support for Gangnam Myeonok was thin. It also added Jinju Hoegwan/kongguksu, which is a cold noodle dish but not the main naengmyeon comparison the question asked for.

**Root cause:** This is a retrieval-stage weakness. The embedding model treats "cold noodle" broadly, so it retrieves Woo Lae Oak and Jinju Hoegwan strongly, plus only one lower-ranked Gangnam Myeonok chunk. Because the strongest retrieved context was about Woo Lae Oak, the generated answer had much more detail for Pyongyang naengmyeon than Hamhung naengmyeon.

**What I would change:** I would add metadata or tags for dish families such as `naengmyeon`, `kongguksu`, `gukbap`, `gomtang`, and `hanwoo`, then allow metadata filtering or stronger hybrid search. For this query, filtering to `naengmyeon` would keep Woo Lae Oak and Gangnam Myeonok while excluding Jinju Hoegwan.

## Spec Reflection

**One way the spec helped during implementation:** Writing the spec first made the chunking and retrieval code much more concrete. Instead of asking for a generic RAG pipeline, the implementation had to preserve source titles, URLs, Korean keywords, and dish-specific notes because those were already named in `planning.md`.

**One way implementation diverged from the spec, and why:** The original retrieval plan was semantic-only top-k search. After testing, I added a small keyword rerank on top of semantic retrieval because the embedding model sometimes ranked broadly related soup/noodle chunks above exact matches like Hadongkwan for Myeongdong gomtang. I also used Gradio 4.44.1 instead of the assignment's suggested `gradio>=6.9.0` because the available package index did not offer a 6.x release for this environment.

## AI Usage

**Instance 1**

- *What I gave the AI:* My chosen domain, the source corpus I had collected, and specific questions about whether the domain and `.txt` documents fit the assignment requirements.
- *What it produced:* Feedback on missing inputs, possible grading traps, and a reviewable structure for the planning decisions I needed to approve before implementation.
- *What I changed or overrode:* I kept the Korea travel domain, confirmed the use of manually collected `.txt` source notes, approved the core chunking/retrieval/evaluation decisions, and added stronger requirements around URL transparency, refusal behavior, and a harder cold-noodle evaluation question before implementation.

**Instance 2**

- *What I gave the AI:* The approved planning sections for chunking, retrieval, generation, and interface.
- *What it produced:* `ingest.py`, `query.py`, `evaluate.py`, and `app.py`, plus generated chunk/evaluation artifacts.
- *What I changed or overrode:* I inspected real retrieval results and directed a change from semantic-only retrieval to semantic retrieval plus keyword reranking after the Myeongdong beef-soup and summer-noodle queries exposed weak ranking. I also kept the README failure case instead of hiding the partial cold-noodle result.

**Demo**

https://drive.google.com/file/d/1KMSm2kTFThAekLjJrRdLcz_lu4aroDsQ/view?usp=sharing
