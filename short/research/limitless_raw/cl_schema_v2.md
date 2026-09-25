# Report Schema: Crypto Standard (v2)
Source: https://docs.chain.link/data-streams/reference/report-schema-v2

> For the complete documentation index, see [llms.txt](/llms.txt).

> **NOTE: Get started**
>
> Data Streams is self-serve, no sales call required. [Sign up](https://app.chain.link) to get started, or follow the
> [sign-up guide](/data-streams/sign-up).

Cryptocurrency streams adhere to the report schema outlined below.

## Time-Weighted Average Price (TWAP)

The v2 schema is used by TWAP streams. The `price` field carries the time-weighted average price for the stream's configured window, not a spot or median price. Each TWAP stream is scoped to one asset and one window length (for example, 30 seconds or 60 seconds). The window length is part of the stream's name and metadata. See [How Report Timestamps Work](/data-streams/how-report-timestamps-work) for how timestamps apply to TWAP streams.

## Schema Fields

| Field                   | Type      | Description                                                                                                                   |
| ----------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `feedId`                | `bytes32` | Unique identifier for the Data Streams feed                                                                                   |
| `validFromTimestamp`    | `uint32`  | Earliest timestamp when the price is valid (seconds) — [How report timestamps work](/data-streams/how-report-timestamps-work) |
| `observationsTimestamp` | `uint32`  | Latest timestamp when the price is valid (seconds) — [How report timestamps work](/data-streams/how-report-timestamps-work)   |
| `nativeFee`             | `uint192` | Legacy onchain verification fee field                                                                                         |
| `linkFee`               | `uint192` | Legacy onchain verification fee field; not used for subscription billing                                                      |
| `expiresAt`             | `uint32`  | Expiration date of the report (seconds)                                                                                       |
| `price`                 | `int192`  | Time-weighted average price (TWAP) for the stream's window                                                                    |

**Note**: Future Cryptocurrency streams may use different report schemas.