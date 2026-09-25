# Sources: 15-minute BTC Up/Down markets on Limitless

All sources checked on **2026-09-25** (UTC), live, not from memory. Where TOPIC.md and docs.limitless.exchange disagree, the docs win (see "Discrepancies with TOPIC.md").

Raw captures (docs as Markdown, API JSON, CSS tokens) are in
`short/research/limitless_raw/`. The fetch workspace was the session scratchpad `facts/`.

Every Limitless docs page is also served as Markdown by adding `.md` to the URL, for example `https://docs.limitless.exchange/user-guide/fees.md`. Those files are what's quoted below.

---

## 1. Prediction market basics

### 1.1 A YES and a NO share together are backed by $1, and a winning share pays $1
- **Say it:** "Every Yes share has a matching No share. Together they're backed by exactly one dollar. The winner gets the dollar. The loser gets nothing."
- **URL:** https://docs.limitless.exchange/ (docs home, `index.md`)
- **Quote:** "Every pair of "YES" + "NO" shares is fully collateralized by \$1.00 USDC" and "Winning shares pay out **\$1.00**. Losing shares are worthless after market resolution."
- **Checked:** 2026-09-25

### 1.2 Price range
- **Say it:** "Shares trade between 1 cent and 99 cents."
- **URL:** https://docs.limitless.exchange/
- **Quote:** "Shares are **always priced between \$0.01 and \$0.99** USDC"
- **Caveat:** the API and order book run on a 0.1¢ tick. Prices like 61.6¢ are normal, and the fee tables go to \$0.999. See Discrepancies.
- **Checked:** 2026-09-25

### 1.3 A price reads as a probability
- **Say it:** "A price of 62 cents means the market thinks there's about a 62% chance."
- **URL:** https://docs.limitless.exchange/user-guide/what-is-limitless
- **Quote:** "Buy "Yes" shares that BTC will reach \$65k at **\$0.15**, implying a **15% chance** the outcome will be realized"
- **Also:** the live market page labels the price "% Chance" (for example "67.3% Chance" in the sidebar of https://limitless.exchange/markets/btc-up-or-down-15-min-1790341200).
- **Checked:** 2026-09-25

### 1.4 Shares come into existence when both sides agree on odds that add up to $1
- **Say it:** "New shares only appear when a Yes buyer and a No buyer together put up exactly one dollar."
- **URL:** https://docs.limitless.exchange/
- **Quote:** "Shares are created when **opposing sides come to an agreement on odds** — the sum of what each side is willing to pay equals \$1.00"
- **Checked:** 2026-09-25

---

## 2. The order book

### 2.1 Separate Yes and No books, each with bids and asks
- **Say it:** "Each market has two order books, one for Yes and one for No. Each book has bids to buy and asks to sell."
- **URL:** https://docs.limitless.exchange/user-guide/clob-overview
- **Quote:** "Each market has a **Yes** and **No** order book, with separate **Bids** (buy orders) and **Asks** (sell orders)."
- **Checked:** 2026-09-25

### 2.2 Spread, with the docs' own BTC example
- **Say it:** "Sellers ask 51 cents, buyers bid 49. The 2-cent gap is the spread."
- **URL:** https://docs.limitless.exchange/user-guide/clob-overview
- **Quote:** "For example, in a market about the BTC price: Traders are offering to **sell** "Yes" shares at **51 cents** — this is the price you'd pay if you placed a market order to buy. Traders are **bidding** 49 cents to **buy** "Yes" shares — the amount you'd receive if you placed a market order to sell. The difference between them is the **spread**. The lower the better."
- **Checked:** 2026-09-25

### 2.3 The two books mirror each other (a No bid is a Yes ask)
- **Say it (optional):** "Bidding 40 cents for No is the same as offering Yes at 60 cents."
- **URL:** https://docs.limitless.exchange/api-reference/trading/orderbook
- **Quote:** "NO bid @ P ≡ YES ask @ (1 - P) (someone bidding for NO is offering YES)" and "native NO orders are converted into their YES-side equivalent before aggregation". A second page adds: "Buying NO at 0.30 is the same order as selling YES at 0.70, so NO interest appears in the YES asks. One book is complete." (https://docs.limitless.exchange/developers/mcp-server)
- **Checked:** 2026-09-25

---

## 3. Bid-bid matching by minting a new pair (the wow beat)

### 3.1 The user docs: split $1 into a pair, merge a pair back into $1
- **Say it:** "One dollar can be split into one Yes plus one No, and one Yes plus one No can be merged back into a dollar."
- **URL:** https://docs.limitless.exchange/user-guide/merge-split
- **Quote:** "**Split \$1** into **1 Yes share + 1 No share**." / "**Merge 1 Yes share + 1 No share** back into **\$1** collateral." / "Liquidity defragmentation — Under the hood, this enables better order book matching across Yes/No assets"
- **Checked:** 2026-09-25

### 3.2 The exchange contract: a "MINT" match between two buy orders
- **Say it:** "A Yes bid and a No bid that add up to a dollar can fill each other. Nobody is selling. The exchange takes both payments and mints a brand-new Yes+No pair."
- **URL:** https://github.com/limitless-labs-group/limitless-ctf-exchange/blob/main/docs/Overview.md (Limitless's public fork of the Polymarket CTF Exchange. The docs name this repo at https://docs.limitless.exchange/user-guide/security: "Limitless maintains a public fork of the CTF Exchange at limitless-labs-group/limitless-ctf-exchange". The same page says orders are "matched on-chain against the CTF".)
- **Quote:** "The CTF exchange allows for matching operations that include a mint/merge operation which allows orders for complementary outcome tokens to be crossed." Scenario 2, `MINT`: maker "**UserA** BUY **100** token **`A`** @ **\$0.50**", taker "**UserB** BUY **50** token **`A'`** @ **\$0.50**" → "1. Transfer **25** **`C`** from **userB** into `CTFExchange` 2. Transfer **25** **`C`** from **userA** into `CTFExchange` 3. Mint **50** token sets (= **50** token **`A`** + **50** token **`A'`**) 4. Transfer **50** token **`A`** from `CTFExchange` to **userA** 5. Transfer **50** token **`A'`** from `CTFExchange` to **userB**"
- **Exact wording:** the contract docs say **"Mint"** ("Mint 50 token sets") and call the match type **`MINT`**. The mirror case is **`MERGE`**. The user guide says **"Split"/"Merge"**. The CLOB overview page itself does **not** describe bid-bid minting.
- **Worked example for the video (arithmetic, not a quote):** a Yes bid at 60¢ and a No bid at 40¢ fill each other: 0.60 + 0.40 = \$1.00 of collateral → 1 new Yes + 1 new No. This is the same mechanism as the contract's 50¢/50¢ example.
- **Checked:** 2026-09-25

---

## 4. Fees (the twist)

**URL for everything in this section:** https://docs.limitless.exchange/user-guide/fees (checked 2026-09-25)

### 4.1 Makers pay nothing, takers pay
- **Say it:** "If your order waits in the book, you pay no fee. If you take an order that's already there, you pay."
- **Quote:** "**Fees only apply to takers** — orders that instantly settle against the order book." / "Limit orders (makers) | No fees | Even though you sign a transaction with fee terms, you pay nothing if your order is placed in the book" / "If you provide liquidity to the book, you can trade **completely fee-free**."

### 4.2 CLOB fee ranges, and what each fee is paid in
- **Quote (table):** "**Buy** | 0.40% – 3.00% | Outcome tokens (contracts)" / "**Sell** | 0.42% – 1.50% | Collateral (USDC)"
- **Another docs page states the same thing** (https://docs.limitless.exchange/developers/mcp-server): "The published BUY rate is 3.00% for outcomes priced between \$0.01 and \$0.50, tapering above that, and it is charged in shares. SELL fees are charged in USDC."
- **What the % is charged on:** the value of the fill, meaning shares × price. From https://docs.limitless.exchange/user-guide/maker-rebates: "Executed Value (USD) = Executed Size × Fee-Applicable Price". Their worked example: "Buy | \$0.60 | 1,000 | \$600 | 2.0% | \$12.00". That example assumes a 2.0% rate, so don't put it on screen as the real 60¢ rate. The curve says 2.13% at 60¢. On a buy, the fee comes out of the shares you receive. On a sell, it comes out of the USDC you receive.

### 4.3 Full buy fee curve (every point published)
Quote: "Buy fees start at 3.00% for low-probability markets and decrease as probability increases:"

| Price | Buy fee |
|---|---|
| \$0.01 – \$0.50 | 3.00% |
| \$0.55 | 2.52% |
| \$0.60 | 2.13% |
| \$0.65 | 1.80% |
| \$0.70 | 1.51% |
| \$0.75 | 1.26% |
| \$0.80 | 1.05% |
| \$0.85 | 0.85% |
| \$0.90 | 0.68% |
| \$0.95 | 0.53% |
| \$0.99 | 0.42% |
| \$0.999 | 0.40% |

### 4.4 Full sell fee curve (every point published)
Quote: "Sell fees peak at the midpoint (\$0.50) and decrease toward the extremes:"

| Price | Sell fee |
|---|---|
| \$0.01 | 0.42% |
| \$0.05 | 0.60% |
| \$0.10 | 0.78% |
| \$0.20 | 1.11% |
| \$0.30 | 1.32% |
| \$0.40 | 1.44% |
| \$0.50 | **1.50% (peak)** |
| \$0.60 | 1.44% |
| \$0.70 | 1.32% |
| \$0.80 | 1.11% |
| \$0.90 | 0.78% |
| \$0.95 | 0.60% |
| \$0.99 | 0.45% |
| \$0.999 | 0.42% |

(The curve isn't quite symmetric: 0.42% at \$0.01 but 0.45% at \$0.99.)

### 4.5 The fee at the prices the brief asked about
| Price | Taker BUY | Taker SELL |
|---|---|---|
| 5¢ | 3.00% (falls in the \$0.01–\$0.50 band) | 0.60% |
| 10¢ | 3.00% (falls in the \$0.01–\$0.50 band) | 0.78% |
| 50¢ | 3.00% | 1.50% (peak) |
| 90¢ | 0.68% | 0.78% |

### 4.6 No formula, only listed points
- **Quote:** "The curve is not published as a closed-form formula, and the tables above list representative prices rather than every point." → **Only put listed price points on screen.** Don't interpolate. For example, don't show a 62¢ fee.

### 4.7 Why the curve looks like this (Limitless's own words)
- **Say it:** "Limitless says the curve is there to reward early conviction and discourage flip-flopping."
- **Quote:** "The fee model is designed to reward early conviction, discourage manipulation, and give loyal traders significant discounts." / "**Discourage flip-flopping** and short-term manipulation" / "By discouraging exits at the midpoint, the fee curve protects market integrity when uncertainty is highest."

### 4.8 Personal discounts
- **Quote:** "Fees on Limitless adapt to both the **market price** and your **trading experience**." The API signs every order with the user's own fee band (`rank.feeRateBps`, see https://docs.limitless.exchange/developers/eip712-signing). → The tables give the **published** rate. A given trader may pay less. Say "up to" or "the published fee".

### 4.9 These fees apply to the 15-minute crypto markets
- **Evidence:** the live market `btc-up-or-down-15-min-1790341200` has `"tradeType":"clob"` and `"metadata":{"fee":true,…}`. The maker-rebates page's example is set in "**Hourly Crypto** and **15-minute Crypto** markets" and funds rebates from "eligible taker fees" (https://docs.limitless.exchange/user-guide/maker-rebates). A fee-flagged market requires the signed fee rate to match the user's band: "If the market's `metadata.fee` flag is set, the signed `feeRateBps` must exactly equal your profile's fee band" (https://docs.limitless.exchange/developers/quickstart/nodejs).
- **Extra (maker side):** the same market shows `"makerRebateMult":0.3` / `"rebateRate":"0.3"`. Makers on these markets can earn a share of taker fees back (https://docs.limitless.exchange/user-guide/maker-rebates: "When a taker removes liquidity from the order book and pays a taker fee, Limitless credits a portion of that fee back to the maker whose resting order was filled.").

---

## 5. Resolution: Chainlink TWAP and "Price to Beat"

### 5.1 The docs
- **URL:** https://docs.limitless.exchange/user-guide/market-resolution
- **Quote (oracle table):** "**Chainlink TWAP** | Short-cadence crypto up/down markets (5-minute and 15-minute) | Automatic at deadline"
- **Quote (rules):** "Short-cadence crypto up/down markets are moving to **time-weighted average price (TWAP)** resolution. Instead of comparing two instantaneous prices, both sides of the comparison come from the same Chainlink TWAP stream: an average over a fixed window. The market's description names the exact feed and window length."
  - "The **Price to Beat** is the TWAP captured at the market's open time."
  - "At the deadline, the closing TWAP is read from the same stream. The market resolves **Up** when the closing value is greater than or equal to the Price to Beat, and **Down** otherwise."
  - "Because the value is an average over the window rather than a single tick, a momentary price spike at the boundary does not decide the market on its own."
  - "The report at the exact resolution time is used first. If it is unavailable, the first Chainlink observation within the market's stated tolerance window is used. If no report exists in that window, the market is not resolved automatically and is handled per its description."
- **Checked:** 2026-09-25

### 5.2 What the live 15-minute BTC market actually says (window = 60 seconds)
- **URL:** https://limitless.exchange/markets/btc-up-or-down-15-min-1790341200 (API: https://api.limitless.exchange/markets/btc-up-or-down-15-min-1790341200)
- **Description, verbatim:** "This market will resolve to "Up" if the Chainlink BTC/USD 60-second TWAP on September 25, 2026, at 13:15 UTC is greater than or equal to the Price to Beat captured from the same TWAP on September 25, 2026, at 13:00 UTC. Otherwise, this market will resolve to "Down". The Chainlink BTC/USD 60-second TWAP is used for both the Price to Beat and resolution. Other exchanges, spot markets, and oracles will not be used. The report at the exact resolution time is used first. If it is unavailable, the first Chainlink observation within the following 5 seconds will be used. If no report exists in that window, the market will not resolve automatically. The Price to Beat captured from the Chainlink BTC/USD 60-second TWAP on September 25, 2026, at 13:00 UTC was \$84468.016195913763520512."
- **Machine-readable:** `metadata.chainlinkDataStream = {"pair":"BTC/USD","streamType":"twap","twapWindowSeconds":60,"toleranceSeconds":5,"priceDecimals":18,"streamUrl":"https://data.chain.link/streams/btc-usd-twap-60s-streams","feedId":"0x0002ee6757e8822c00d273bc340fc24c9cafe123a4ff2ea1dbdb31944bc7d95f"}`, `priceOracleMetadata.name = "BTC TWAP 60s (Chainlink)"`.
- **Say it:**
  - "The Price to Beat is Bitcoin's average price over the minute before the market opens, from Chainlink."
  - "At the close, it takes the average over the last minute again. Equal or higher, Up wins. Lower, Down wins."
  - "Only that Chainlink number counts. Not Binance, not any other exchange."
- **Tie:** a tie resolves **Up** ("greater than or equal to").
- **The Price to Beat is not a spot price at the open.** It's the 60-second TWAP at the open time, which covers the 60 s before the open (see 6.2).
- **Checked:** 2026-09-25 13:05 UTC

---

## 6. Chainlink product

### 6.1 The feed: Chainlink Data Streams, BTC/USD TWAP 60s
- **URL (stream page named in every market description):** https://data.chain.link/streams/btc-usd-twap-60s-streams. It returned a Vercel bot-check (HTTP 429) to our fetcher, but it's the link Limitless puts in the market text. The product family is Chainlink **Data Streams**: https://docs.chain.link/data-streams
- **URL (TWAP schema):** https://docs.chain.link/data-streams/reference/report-schema-v2
- **Quote:** "The v2 schema is used by TWAP streams. The `price` field carries the time-weighted average price for the stream's configured window, not a spot or median price. Each TWAP stream is scoped to one asset and one window length (for example, 30 seconds or 60 seconds)."
- **Checked:** 2026-09-25

### 6.2 How the 60-second window lines up
- **URL:** https://docs.chain.link/data-streams/how-report-timestamps-work
- **Quote:** "Time Weighted Average Price (TWAP) streams report the average price over a rolling window, rather than a single observed price." / "For example, a 60-second TWAP requested "at `12:05:01`" covers `12:04:01` → `12:05:01`." / "TWAP = (sum of price × duration for each report in the window) / window length in seconds"
- **Say it:** "The close isn't one tick. It's the average of the last 60 seconds. A spike in the final second moves that average by only about a sixtieth of its size."
  - (Arithmetic: a spike lasting 1 s out of a 60 s window carries 1/60 of the weight.)
- **Checked:** 2026-09-25

---

## 7. Live market example (15-minute BTC Up/Down)

Fetched from the public API (no auth) at 2026-09-25 13:05 UTC. Raw JSON is saved.

| Field | Value |
|---|---|
| Title | `BTC Up or Down - 15 Min` |
| Slug | `btc-up-or-down-15-min-1790341200` (stable slug `btc-15min-price` always points to the current round) |
| Window | `startAt` 2026-09-25T13:00:00Z → deadline 13:15:00Z (`minutesDeadline: 15`) |
| Categories / tags | `["Crypto","Bitcoin","15 min"]`, tags include `"Recurring"`, `"Minutes 15"` |
| Outcome labels in UI | **Up / Down** (site config: `labels:["Up","Down"], icons:["↑","↓"]`). The API still calls the two tokens `yes` / `no`, with Up = outcome 0 (the YES token). |
| Price to Beat | \$84,468.016… (60 s TWAP at 13:00:00 UTC) |
| Prices (`prices`) | Up 0.645 / Down 0.355 |
| Book (YES/Up side) | best bid 0.616, best ask 0.669, midpoint 0.6425, `maxSpread` 0.035 (LP-reward setting) |
| Tick size | 0.001 (0.1¢). Book levels like 0.616, 0.593 are on this tick. Docs: "Price between 0 and 1, tick-aligned to `0.001`" (https://docs.limitless.exchange/developers/sdk/rust/orders) |
| Min order size (for rewards) | `minSize` 50,000,000 raw = 50 shares (6 decimals) |
| Collateral | USDC on Base (`0x8335…2913`) |
| Fee flag | `"fee": true` |
| **Taker delay** | `"takerDelayMs": 500`. Taker orders on this market are held **0.5 s** before matching. Docs: "When it is greater than `0`, the matching engine briefly holds marketable (taker) orders before filling them" (https://docs.limitless.exchange/api-reference/markets/get-market). Also: "`postOnly` (maker) orders are never delayed" (same page) |
| Maker rebate | `makerRebateMult` 0.3 |

Second snapshot at 13:15 UTC of the next round (`btc-up-or-down-15-min-1790342100`): Price to Beat \$84,416.37 (60 s TWAP at 13:15), `prices` [0.539, 0.461], YES book best bid 0.656 / best ask 0.719.

Resolution of the 13:00–13:15 market (API re-fetched at 13:18:59 UTC): `status: "RESOLVED"`, `winningOutcomeIndex: 1`, `payoutNumerators: [0,1]`, `chainlinkTwapResolution.outcome: "DOWN"`. Open TWAP (13:00:00) = 84,468.016… and close TWAP (13:15:00, `offsetSeconds: 0`) = 84,416.366…. Close < Price to Beat, so **Down** won. It fell about \$52. The closing TWAP is exactly the next round's Price to Beat (84,416.365817…), so one round's close is the next round's line. The first automatic attempt at 13:15:00.665 found no report yet ("No Chainlink report found within forward tolerance window [1790342100, 1790342105]"). A retry at 13:18:00 used the 13:15:00 report, so payout readiness can lag the deadline by a few minutes.

Also noted: the book carries very large resting size at 0.001 and 0.999. The docs warn: "Books often carry very large resting size at 0.001 and 0.999. That is not tradeable depth." (https://docs.limitless.exchange/developers/mcp-server). Leave those levels out of any on-screen depth or imbalance number.

---

## 8. Order book imbalance

### 8.1 Definition
- **Say it:** "Imbalance compares the buy side with the sell side: bids minus asks, divided by bids plus asks. It runs from −1 to +1."
- **Source:** Gould, M. D. & Bonart, J. (2016). "Queue Imbalance as a One-Tick-Ahead Price Predictor in a Limit Order Book." *Market Microstructure and Liquidity* 2(2). DOI https://doi.org/10.1142/S2382626616500064. Preprint https://arxiv.org/abs/1512.03492
- **Quote (Sec. 3.3, eq. 7):** "at a given time t, let I(t) := [n_b(b_t,t) − n_a(a_t,t)] / [n_b(b_t,t) + n_a(a_t,t)] denote the queue imbalance at time t. The quantity I measures the (normalized) difference between n_b(b_t,t) and n_a(a_t,t), and thereby provides a quantitative assessment of the relative strengths of buying and selling pressure in an LOB." And: "If I > 0 … then the bid queue is longer than the ask queue, which suggests that there is a net positive buying pressure in the LOB."
- **Note:** in the paper, n_b and n_a are the sizes at the **best** bid and best ask. TOPIC.md's "bid depth − ask depth" generalises this to depth over several levels. That's fine to show if the on-screen label says what depth is counted.
- **Checked:** 2026-09-25

### 8.2 Imbalance predicts the next short move (a tendency, not a guarantee)
- **Say it:** "In studies of real order books, when the bid side is much heavier, the next small move is more often up. More often, not always."
- **Source A:** Gould & Bonart (above). **Quote (abstract):** "we fit logistic regressions between the queue imbalance and the direction of the subsequent mid-price movement for each of 10 liquid stocks on Nasdaq. In each case, we find a strongly statistically significant relationship between these variables." They find "a considerable improvement in binary and probabilistic classification for large-tick stocks, and … a moderate improvement … for small-tick stocks."
- **Source B:** Cont, R., Kukanov, A. & Stoikov, S. (2014). "The Price Impact of Order Book Events." *Journal of Financial Econometrics* 12(1): 47–88. DOI https://doi.org/10.1093/jjfinec/nbt003. Preprint https://arxiv.org/abs/1011.6402. **Quote:** "We show that, over short time intervals, price changes are mainly driven by the order flow imbalance, defined as the imbalance between supply and demand at the best bid and ask prices. Our study reveals a linear relation between order flow imbalance and price changes, with a slope inversely proportional to the market depth."
- **Honest caveats:**
  1. Both papers study **US stocks** (Nasdaq and NYSE), not crypto prediction markets.
  2. Gould & Bonart predict only the **next** mid-price move, "one tick ahead". It's a short-horizon tendency, not a forecast of where the market settles.
  3. Cont et al. measure **order flow** imbalance (changes in the queues), a close relative of the static depth ratio but not the same thing.
  4. On Limitless the No book is the mirror of the Yes book (2.3), so the No book's imbalance is just the Yes book's with the sign flipped. Show one book's imbalance, not two independent signals.
  5. Resting orders can be cancelled instantly, so displayed depth can vanish.
- **Checked:** 2026-09-25

---

## 9. Binance as the "fast screen"

### 9.1 What the evidence supports
- **Source A (Binance as main venue for price discovery):** Cosenza, R. & Stalder, S. "Where is the Price of Bitcoin Determined? Price Discovery in a Fragmented Market." SSRN https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4983566 (SSRN blocked our fetcher with 403. Abstract wording as reproduced at https://mlquants.substack.com/p/where-is-the-price-of-bitcoin-determined): "This paper examines the role of unregulated Bitcoin exchanges for price discovery, especially in comparison to regulated spot platforms…" and it identifies "unregulated exchanges, particularly Binance, as the primary source of price discovery", where "lower transaction costs, higher trading volumes, and volatility significantly enhance price discovery". The SSRN listing snippet says the leaders are "spot and perpetual futures on the less-regulated exchange Binance".
- **Source B (Binance's perpetual futures lead the most, more than spot):** Albers, J., Cucuringu, M., Howison, S. & Shestopaloff, A. Y. (2021). "Fragmentation, Price Formation, and Cross-Impact in Bitcoin Markets." https://arxiv.org/abs/2108.09750. **Quote:** "Perpetual swaps and quarterly futures on Binance and Huobi were found to be particularly strong leading markets, while the Bybit and FTX perpetuals were found to be strong laggards." / "the most leading market, the Binance USDT perpetual".
- **Source C (Binance BTC spot is the most liquid spot venue, 2021–22 data):** Gemayel, R., Franus, T. & Bowden, J. (2023). "Price discovery between Bitcoin spot markets and exchange traded products." *Economics Letters* 228, 111152. https://doi.org/10.1016/j.econlet.2023.111152. Open copy: https://openaccess.city.ac.uk/id/eprint/30528/. **Quote:** "the Bitcoin market on Binance is found to be the most liquid across exchanges according to the AI measure."
- **Verdict: mixed on "spot specifically".** The evidence backs "Binance is one of the main places BTC price discovery happens". It does **not** cleanly back "Binance BTC/USDT **spot** is where moves show up first". Binance **perpetual futures** often lead spot. The venue ranking also shifts over time and by time of day.
- **Safe wording:** "Binance is one of the fastest places BTC moves show up." or "Traders watch a fast exchange feed like Binance." **Avoid:** "Binance spot moves first" or "the highest-volume BTC venue" as a flat claim without a current source.
- **Also true, and worth saying in the risk beat:** these markets settle **only** on the Chainlink TWAP. "Other exchanges, spot markets, and oracles will not be used." (live market description, 5.2). So Binance ≠ the settlement price.
- **Checked:** 2026-09-25

---

## 10. Limitless UI palette and feel (for an unofficial look-alike)

Taken from the CSS custom properties served with https://limitless.exchange/markets/btc-up-or-down-15-min-1790341200 and the site's JS config. No logo was downloaded or described.

| Role | Token | Hex |
|---|---|---|
| **Up / Yes** button bg (text white) | `green.500` | **#389A57** |
| **Down / No** button bg (text white) | `red.500` | **#ED5023** |
| Bright green (secondary shades) | `green.200–800` | #0FC591 |
| Bright red (secondary shades) | `red.300–800` | #FF3756 |
| Probability bar 25–50% | `orange.500` | #FF9200 |
| Brand neon accent (promo cards, black text) | `brandNeon.500` | **#C3FF00** |
| Lime | `lime.*` | #97EE2B |
| Brand dark green | `brandDark.500` | #052F1B |
| Pistachio | `pistachio` | #DCF58C |
| Link/info blue | `blue.500` | #0079FF |
| **Dark mode** page bg | `grey.50` | **#121212** |
| Dark mode deepest / card | `grey.100` / `grey.200` / `grey.300` | #000000 / #242424 / #333333 |
| Dark mode text / secondary text | `grey.900` / `grey.700` | #FFFFFF / #B3B3B3 |
| **Light mode** page bg (default) | `grey.50` | **#FFFFFF** |
| Light mode surfaces | `grey.100` / `grey.200` / `grey.300` | #FAFAFA / #F0F0F0 / #EDEDED |
| Light mode text / secondary text | `grey.900` / `grey.700` | #000000 / #747474 |

- **Up/Down config (JS):** `PRICE_MARKET_CONFIG … labels:["Up","Down"], icons:["↑","↓"], colors:{outcome0:{bg:"green.500",text:"white"}, outcome1:{bg:"red.500",text:"white"}}`
- **Probability bar colours:** red.500 up to 25%, orange.500 up to 50%, green.500 above 50%.
- **Theme:** `initialColorMode:"light"`, `useSystemColorMode:false`. Light is the default and dark mode is available. A dark-mode recreation (#121212 bg) reads well on phones and is a fair echo.
- **Type:** UI text is **Inter**. Titles use a display face loaded as `mdNichrome` / `mdNichromeBlack`, which appears to be a commercial typeface. Don't use it without a licence. Use Inter plus a free bold grotesk for titles.
- **Feel:** flat cards, 12px radius (trade panel `border-radius:12px`), 14px base text, prices shown in cents with one decimal ("Up: 44.3¢"), "% Chance" labels, and a thin progress bar splitting Up vs Down.
- **Checked:** 2026-09-25

---

## Numbers safe to show on screen

| Number | Meaning | Source |
|---|---|---|
| \$1.00 | a Yes+No pair is backed by \$1 USDC. A winning share pays \$1 | docs home (1.1) |
| \$0.01–\$0.99 | published price range | docs home (1.2) |
| 15¢ → 15% | docs' own price-as-probability example | what-is-limitless (1.3) |
| 51¢ / 49¢ | docs' own BTC spread example | clob-overview (2.2) |
| 0% | maker fee | fees (4.1) |
| 3.00% | taker BUY fee at any price from \$0.01 to \$0.50 (the max) | fees (4.3) |
| 2.52%, 2.13%, 1.80%, 1.51%, 1.26%, 1.05%, 0.85%, 0.68%, 0.53%, 0.42%, 0.40% | taker BUY fee at 55¢, 60¢, 65¢, 70¢, 75¢, 80¢, 85¢, 90¢, 95¢, 99¢, 99.9¢ | fees (4.3) |
| 1.50% | taker SELL fee peak, at 50¢ | fees (4.4) |
| 0.42%, 0.60%, 0.78%, 1.11%, 1.32%, 1.44% | taker SELL fee at 1¢, 5¢, 10¢, 20¢, 30¢, 40¢ (mirrored at 60¢–95¢: 1.44, 1.32, 1.11, 0.78, 0.60; 0.45% at 99¢, 0.42% at 99.9¢) | fees (4.4) |
| 0.40%–3.00% / 0.42%–1.50% | buy / sell fee ranges | fees (4.2) |
| 15 min | market length | live market (7) |
| 60 seconds | TWAP window of the Chainlink BTC/USD stream used | live market description (5.2) |
| 5 seconds | fallback tolerance for the closing report | live market description (5.2) |
| ≥ | tie goes to Up | market-resolution + live description (5.1, 5.2) |
| 0.5 s (500 ms) | taker delay on the live 15-min BTC market | live market `takerDelayMs` (7) |
| 0.1¢ (0.001) | price tick | API docs + live book (7) |
| 60¢ + 40¢ = \$1 | illustrative bid-bid mint | arithmetic on 1.1 / 3.2 |
| −1 to +1 | range of the imbalance ratio | Gould & Bonart (8.1) |

Rules for the edit:
- Don't show an interpolated fee (e.g. "fee at 62¢"). Use only listed points.
- If the hook shows a real-looking Up price jump (50¢ → 80¢), label it illustrative, or pull it from a real recorded market. That move is not sourced here.
- Label any live-looking BTC price or Price to Beat "example". The live values above (\$84,468.02) are real for 2026-09-25 13:00 UTC.

---

## Discrepancies with TOPIC.md

1. **"Buying cheap long shots costs the most."** Not quite. The buy fee is a **flat 3.00% for every price from \$0.01 up to \$0.50** and only falls above 50¢. A 5¢ buy and a 50¢ buy cost the same 3.00%. Safer line: *"Buying at 50¢ or less costs the top rate, 3%. The fee only drops once the price is above 50¢."*
2. **"Selling costs the most near 50/50."** ✔ Correct: 1.50% peak at 50¢.
3. **"The design punishes quick flips."** Supported only as **Limitless's stated intent**: "Discourage flip-flopping". Attribute it ("Limitless says…").
4. **Fee basis.** TOPIC doesn't say, but the docs do. The buy fee is taken **in shares**, the sell fee **in USDC**. Individual traders can get a lower rate ("trading experience" discounts), so these are the **published** rates. The curve has no formula. Use listed points only.
5. **"The exchange mints a fresh pair."** The user guide doesn't use the word "mint" for order matching. The CLOB overview page only covers the Yes/No books and the spread. The docs home says shares "are created when opposing sides come to an agreement on odds". The **contract docs** (Limitless's fork of the CTF Exchange) call it a **`MINT`** match: "Mint 50 token sets". Wording is fine. Cite 3.2.
6. **TWAP window.** TOPIC says "a fixed window". The live market states **60 seconds** (Chainlink BTC/USD 60-second TWAP). **Price to Beat = the same 60 s TWAP at the market's open time**, not a spot price at the open. Ties resolve **Up**. The docs say these markets "are moving to" TWAP resolution. The live BTC 15-min market already uses it.
7. **"Binance spot is where BTC moves show up first."** Evidence is mixed. Studies put Binance at or near the top for price discovery, but its **perpetual futures** tend to lead, not necessarily spot. Use "one of the fastest places BTC moves show up".
8. **Price range.** Docs home says \$0.01–\$0.99, but the market trades on a **0.1¢ tick** (0.001), and the UI shows prices like 44.3¢. Whole-cent prices on screen are still fine.
9. **Not in TOPIC, and relevant to "the Binance play" and the risk beat:** the live 15-min BTC market has a **500 ms taker delay**. Market orders are held half a second before they can fill. Makers are not delayed. This directly limits "see Binance move, then snipe". Mention latency and the delay in the risk beat.
10. **Order book imbalance** is sourced from **stock** order-book studies. Say "tends to" and don't imply it's been shown on Limitless. The Yes and No books are mirrors, so imbalance is one signal, not two.

---

## Asset licenses

- _Placeholder: fill in music, SFX, fonts and any footage or icons with licence and URL once chosen._
