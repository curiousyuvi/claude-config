---
name: feedback-vendor-language-codes-explicit
description: Language entries map to AssemblyAI/ElevenLabs codes via explicit per-entry overrides, never by stripping the region from codeV2
metadata:
  type: feedback
---

When a language in `src/helper/language.ts` needs a different code for a speech vendor (e.g. fr-CA sends `fr`), set the per-entry `assemblyAICode` / `elevenLabsLanguage` fields on that entry. Do not add a generic "drop the region" helper.

**Why:** Yuvraj wants regional codes preserved wherever a vendor supports them (AssemblyAI has `en_au`, `en_uk`, `de_ch`). A blanket `split("-")[0]` would silently discard that and hide which vendor accepts what.

**How to apply:** New regional language means one entry with explicit vendor overrides. Resolve through `getAssemblyAICode` / `getElevenLabsLanguage`, which fall back to `codeV2`. Related: [[feedback-ask-before-deciding]].
