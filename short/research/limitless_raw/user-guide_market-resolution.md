> ## Documentation Index
> Fetch the complete documentation index at: https://docs.limitless.exchange/llms.txt
> Use this file to discover all available pages before exploring further.

# Market Resolution

> How markets are resolved on Limitless Exchange

## Overview

Every market on Limitless has a defined resolution condition and deadline. When the deadline passes, the market is resolved based on objective data from the designated oracle source.

## Resolution process

<Steps>
  <Step title="Market deadline passes">
    Each market has a specific deadline (e.g., "Feb 16, 17:00 UTC"). Limitless accepts no new trades after this time.
  </Step>

  <Step title="Oracle reports the outcome">
    The designated oracle source provides the verified result. **Pyth Network** now resolves the majority of markets automatically.
  </Step>

  <Step title="Team reviews (if needed)">
    For manually resolved markets, the Limitless team reviews the outcome against the resolution criteria defined on the market page. Resolution typically occurs within **24–72 hours** of the market deadline, depending on event complexity and data availability.
  </Step>

  <Step title="Winning shares pay out">
    Winning shares ("Yes" or "No" depending on outcome) are redeemable for \$1.00 each after the payout has been settled on-chain. Losing shares become worthless.
  </Step>
</Steps>

## Claiming vs. selling before resolution

Redeeming winning shares after a market resolves is **not the same** as selling them on the order book before resolution:

| Action                     | When                                                        | Payout                                  | Fees                                                                              |
| -------------------------- | ----------------------------------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------- |
| **Claim / redeem**         | After the market resolves and the on-chain payout is posted | Exactly \$1.00 USDC per winning share   | No trading fee on the redemption itself                                           |
| **Sell on the order book** | Anytime before resolution (or before you claim)             | Current market price (less than \$1.00) | Taker fee applies if the order matches immediately (see [Fees](/user-guide/fees)) |

<Note>
  If you sold or accepted "claim now" liquidity on the order book before resolution, the USDC you received is the market price minus the taker sell fee. That amount is not the \$1.00 redemption value. The sell fee on CLOB markets is dynamic and peaks at **1.50%** near \$0.50. See the [sell fee curve](/user-guide/fees#sell-fee-curve) for the full table. Maker (resting limit) sells are fee-free.
</Note>

## Oracle sources

<Info>
  Market resolution and on-chain redemption readiness are related but not identical. A market can appear resolved in the API before the underlying payout is fully settled on-chain. Direct redemption attempts may need to wait until the payout data has been posted.
</Info>

<Note>
  The exact method of market resolution is normally determined on the market page. Always check the resolution source and criteria on the specific market before trading.
</Note>

**Pyth Network** now resolves the majority of markets. Other markets may use manual resolution by the Limitless team.

| Oracle             | Used for                                                                | Resolution time                      |
| ------------------ | ----------------------------------------------------------------------- | ------------------------------------ |
| **Pyth Network**   | Majority of markets — crypto prices, stock prices, and other data feeds | Automatic at deadline                |
| **Chainlink TWAP** | Short-cadence crypto up/down markets (5-minute and 15-minute)           | Automatic at deadline                |
| **Manual**         | Custom event markets (sports, politics, etc.)                           | Typically 24–72 hours after deadline |

For Pyth-resolved markets, both the captured baseline price (`metadata.openPrice`) and the strike price quoted in the auto-generated market description use the full precision of the underlying Pyth feed. That is typically 8 decimal places for crypto feeds. Chainlink-resolved markets use the 18-decimal padded value matching the on-chain feed.

### Chainlink TWAP resolution

Short-cadence crypto up/down markets are moving to **time-weighted average price (TWAP)** resolution. Instead of comparing two instantaneous prices, both sides of the comparison come from the same Chainlink TWAP stream: an average over a fixed window. The market's description names the exact feed and window length.

* The **Price to Beat** is the TWAP captured at the market's open time.
* At the deadline, the closing TWAP is read from the same stream. The market resolves **Up** when the closing value is greater than or equal to the Price to Beat, and **Down** otherwise.
* Because the value is an average over the window rather than a single tick, a momentary price spike at the boundary does not decide the market on its own.
* The report at the exact resolution time is used first. If it is unavailable, the first Chainlink observation within the market's stated tolerance window is used. If no report exists in that window, the market is not resolved automatically and is handled per its description.

Each TWAP market's description states the exact feed, window, tolerance, and Price to Beat — always the authoritative source for that market's rule.

## Resolution for different market types

### Standard (CLOB) markets

Binary Yes/No outcome. One side wins, the other loses.

### NegRisk (category) markets

Only one outcome in the group can win. All other outcomes resolve to "No". See [NegRisk markets](/user-guide/negrisk-overview) for details.

## Market-specific resolution rules

The mechanics above describe how a Yes/No outcome pays out once chosen. The resolution criteria on each market page decide **which** outcome wins. Those criteria can cover event-specific edge cases — for example, a tied match, a cancelled game, or a "None of the above / Other" clause on a bracket-style market.

<Note>
  Always read the market page before you trade. It defines exactly which real-world results resolve **Yes**, which resolve **No**, and how ties, cancellations, or unlisted outcomes are handled. If the stated criteria for **Yes** are not met, the market resolves **No**. This includes cases where the market page lists a fallback such as "Other" or "None of the above".
</Note>

If the published criteria are ambiguous or you cannot apply them to the real-world result, Limitless treats the market as misresolved and refunds users per the [Refund Policy](/user-guide/refund-policy). You get back the bet amount, not the \$1.00 payout.

## Disputes and misresolutions

If a market is misresolved, Limitless refunds the bet amount. See the [Refund Policy](/user-guide/refund-policy) for details.

If you believe a market was resolved incorrectly, contact the team through the **support channel** on [limitless.exchange](https://limitless.exchange) (footer), via email at [help@limitless.network](mailto:help@limitless.network), or on [Discord](https://discord.com/invite/yb4SscD8RZ).
