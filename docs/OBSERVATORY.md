# Molecularis Observatory

Observatory is the live, read-only engineering and scientific-readiness interface for Agentics Molecularis.

- [Open the Observatory source](../observatory/index.html)
- [Run instructions and data methodology](../observatory/README.md)

Run from the repository root:

```bash
python -m http.server 8765 --directory observatory
```

Then open http://localhost:8765. The interface reads the public `CORE` branch from GitHub and requires internet access.

**Integrity:** repository declarations and file counts are not proof of software correctness or scientific validity. Observatory labels these distinctions and does not invent progress scores.
