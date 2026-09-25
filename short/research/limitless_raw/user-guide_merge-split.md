> ## Documentation Index
> Fetch the complete documentation index at: https://docs.limitless.exchange/llms.txt
> Use this file to discover all available pages before exploring further.

# Merging & Splitting Shares

> Convert between collateral and outcome share pairs

## Overview

Prediction markets have two native mechanisms that don't exist in traditional instruments: **Merging** and **Splitting** shares.

<Frame>
  <img className="block dark:hidden" src="https://mintcdn.com/limitless/KX4_j-Y88TyVRbCP/images/merge-split-light.png?fit=max&auto=format&n=KX4_j-Y88TyVRbCP&q=85&s=199091bbe09eb7d695e3a6f81f09d6b9" alt="Merge and split interface" style={{maxWidth: "400px"}} width="768" height="694" data-path="images/merge-split-light.png" />

  <img className="hidden dark:block" src="https://mintcdn.com/limitless/KX4_j-Y88TyVRbCP/images/merge-split-dark.png?fit=max&auto=format&n=KX4_j-Y88TyVRbCP&q=85&s=2992d7c045aecdc6428c537a69d047f1" alt="Merge and split interface" style={{maxWidth: "400px"}} width="768" height="694" data-path="images/merge-split-dark.png" />
</Frame>

## Splitting

**Split \$1** into **1 Yes share + 1 No share**.

This is useful when you want to take a position on one side without buying from the order book. Split collateral and sell the side you don't want.

## Merging

**Merge 1 Yes share + 1 No share** back into **\$1** collateral.

This lets you exit both sides of a position and recover your collateral without selling on the order book.

## Why use merge / split?

* **Capital efficiency** — Open and close positions without relying on order book liquidity
* **Better execution** — Avoid paying the spread
* **Liquidity defragmentation** — Under the hood, this enables better order book matching across Yes/No assets

<Info>
  Merge and split operations are available directly in the market UI. Look for the **Merge/Split** option on the market page.
</Info>

## Merge and split via the API

Server-wallet accounts can split and merge programmatically through the REST API:

* [`POST /portfolio/split`](/api-reference/portfolio/split) — convert collateral into a full outcome set
* [`POST /portfolio/merge`](/api-reference/portfolio/merge) — convert a full outcome set back into collateral

These endpoints sign the on-chain transaction with the managed server wallet, so they only work for server-wallet (Web2 mode) accounts. If you trade with an EOA or your own smart wallet, use the **Merge/Split** option in the UI or call `splitPosition` / `mergePositions` on the Conditional Tokens Framework contract yourself. See [Smart Contracts](/user-guide/smart-contracts) for the deployed addresses.
