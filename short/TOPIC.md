# Topic: how short-duration crypto prediction markets work (Limitless Exchange)

## Spine

"These traders aren't guessing. They're watching another screen."

Follow one 15-minute BTC Up/Down market on Limitless from open to close. Every concept shows up as a part of that one trade, in roughly this order:

1. **Hook (0–2 s).** The Up price rockets from about 50¢ to about 80¢ in seconds while a Binance BTC ticker moves beside it.
2. **Prediction market basics.** A YES share and a NO share together always pay out $1, so a price is a probability: 62¢ means the crowd thinks 62%.
3. **The order book.** There are separate YES and NO books, each with bids and asks, a spread and depth.
4. **Bid-bid matching (the wow beat).** A YES bid at 60¢ and a NO bid at 40¢ add up to $1. Neither trader is a seller, yet the exchange mints a fresh YES+NO pair from $1 of collateral and fills both.
5. **Fees (the twist).** Makers pay nothing. Takers pay a fee that depends on price: buying cheap long shots costs the most, and selling costs the most near 50/50. The design punishes quick flips.
6. **Order book imbalance.** Imbalance = (bid depth − ask depth) / (bid depth + ask depth). When one side is much heavier, the price tends to drift toward it in the short term.
7. **The Binance play.** These markets settle on a Chainlink TWAP (an average price over a fixed window) against a stated "Price to Beat". Binance spot is where BTC moves show up first, so traders compare the current price with the Price to Beat, the time left and the volatility to estimate the real chance of "Up". They buy when the market's price is below that estimate. The twist: because the TWAP averages over a window, a last-second spike counts for less than it looks, which catches people who chase the Binance candle.
8. **Ending.** One beat on the real risks (fees, latency, TWAP ≠ Binance, you can lose the whole stake), then loop back to the hook.

If this spine can't hold a beat every 5–8 s, tighten or reorder it and note what changed.

## Facts to verify at build time (docs.limitless.exchange wins over this list)

- Makers pay no fees; fees apply only to taker orders. (user-guide/fees)
- On order-book (CLOB) markets, taker buy fees run from about 0.40% to 3.00%, highest at low prices. Taker sell fees run from about 0.42% to 1.50% and peak at 50¢. (user-guide/fees)
- Each market has a YES book and a NO book with bids and asks. Complementary YES and NO bids can be matched by minting a new pair, and YES+NO can be merged back into $1 USDC. (user-guide/clob-overview)
- Short-cadence crypto up/down markets (5- and 15-minute) resolve on a Chainlink TWAP against a Price to Beat stated in each market's description. (user-guide/market-resolution)
- Shares are priced from $0.01 to $0.99 USDC, and a winning share pays $1.00. (docs home)

Record every fact with its URL in sources.md.

## Constraints

- This is education, not financial advice. Show "Not financial advice" on screen for 1–2 s and put it in the description. No profit promises and no "easy money" framing.
- I'm not affiliated with Limitless. You may echo their palette and UI feel, but use no official logo as a sign-off, nothing implying they made or endorse the video, and a small "unofficial explainer" tag at the end.
- Binance appears only as a price source (a ticker or chart), never as a sponsor.
- Recreate UIs in the video's own medium. No raw screenshots.
