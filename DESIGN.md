
---

# TextPulse `/analyze` — Data Contract

## Request

**`AnalysisRequest`**
| Field | Type | Required | Description |
|---|---|---|---|
| `comment` | `str` | ✓ | The raw customer feedback text to analyze |
| `product_id` | `UUID` | ✓ | ID of the product being reviewed |
| `commenter_id` | `UUID` | ✓ | ID of the customer who submitted the feedback |
| `lan` | `Literal["english", "german", "italian"]` | ✗ | Optional language hint; API auto-detects if omitted |

---

## Sub-models

**`AspectResult`**
| Field | Type | Description |
|---|---|---|
| `aspect` | `str` | Aspect name, e.g. "delivery", "packaging" |
| `polarity` | `float` | Sentiment score bounded between -1.0 (very negative) and 1.0 (very positive) |
| `excerpt` | `str` | The exact substring of the original comment that triggered this aspect |

**`EntityResult`**
| Field | Type | Description |
|---|---|---|
| `text` | `str` | The named entity surface form, e.g. "DHL", "Berlin" |
| `label` | `str` | Entity type label, e.g. "ORG", "LOC", "PERSON" |

**`LinguisticMetrics`**
| Field | Type | Description |
|---|---|---|
| `lexical_density` | `float` | Ratio of content words to total words; higher means more information-dense |
| `negation_detected` | `bool` | Whether the feedback contains negation, e.g. "not good", "never arrived" |

---

## Response

**`AnalysisResponse`**
| Field | Type | Description |
|---|---|---|
| `product_id` | `UUID` | Echoed back from the request |
| `commenter_id` | `UUID` | Echoed back from the request |
| `detected_language` | `str` | Language the API detected, regardless of hint |
| `processed_at` | `datetime` | Server timestamp of when the analysis was performed |
| `aspects` | `list[AspectResult]` | All aspects found with polarity and excerpt |
| `keywords` | `list[str]` | Significant words extracted from the feedback |
| `entities` | `list[EntityResult]` | Named entities found in the feedback |
| `metrics` | `LinguisticMetrics` | Lexical density and negation detection |

---
