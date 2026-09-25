> ## Documentation Index
> Fetch the complete documentation index at: https://docs.limitless.exchange/llms.txt
> Use this file to discover all available pages before exploring further.

# CLOB Overview

> How the Limitless Central Limit Order Book works

## Overview

Interacting with Limitless's order book is simple and familiar for both traders and market makers. Market orders provide instant execution at the best available price, while limit orders allow you to set your price, participate in price discovery, and earn rewards.

## The order book

Each market has a **Yes** and **No** order book, with separate **Bids** (buy orders) and **Asks** (sell orders).

<Frame>
  <img className="block dark:hidden" src="https://mintcdn.com/limitless/KX4_j-Y88TyVRbCP/images/orderbook-light.png?fit=max&auto=format&n=KX4_j-Y88TyVRbCP&q=85&s=e593cb87282a06751a078cb2d6678ba6" alt="Order book example" width="1704" height="868" data-path="images/orderbook-light.png" />

  <img className="hidden dark:block" src="https://mintcdn.com/limitless/KX4_j-Y88TyVRbCP/images/orderbook-dark.png?fit=max&auto=format&n=KX4_j-Y88TyVRbCP&q=85&s=51f9ab50d4b2bd786a96558c4603ffef" alt="Order book example" width="1704" height="868" data-path="images/orderbook-dark.png" />
</Frame>

For example, in a market about the BTC price:

* Traders are offering to **sell** "Yes" shares at **51 cents** — this is the price you'd pay if you placed a market order to buy.
* Traders are **bidding** 49 cents to **buy** "Yes" shares — the amount you'd receive if you placed a market order to sell.

The difference between them is the **spread**. The lower the better.

## Order types

| Type                                      | Description                               | Best for                          |
| ----------------------------------------- | ----------------------------------------- | --------------------------------- |
| [Market order](/user-guide/market-orders) | Instant execution at best available price | Quick trades                      |
| [Limit order](/user-guide/limit-orders)   | Set your own price                        | Price control, earning LP rewards |

## Advanced features

* **[Merge / Split shares](/user-guide/merge-split)** — Convert between collateral and share pairs
* **[NegRisk markets](/user-guide/negrisk-overview)** — Category markets where only one outcome wins
