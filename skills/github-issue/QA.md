# GitHub Issue — Quality Assurance

Assume the issue reads well and passed an ordinary review. Attack false confidence that can still send an independent agent to implement the wrong thing.

## QA criteria

1. **Lost-context replay:** Remove the source conversation and any private or session-only links. Give the body to a reader with repository access alone. Can they reconstruct the governing decisions and success test, or does an apparently complete issue hide critical meaning?
2. **Alternative-history trap:** Re-read earlier brainstorming, then later corrections or rejections. Could the issue represent an attractive first suggestion instead of the final accepted intent?
3. **False-readiness trap:** Could two competent implementers choose materially different product outcomes because an unresolved owner decision was disguised as a routine technical choice?
4. **Reference/duplication drift:** Would a renamed file, superseding PR, closed duplicate, or inaccessible cross-repo spec reverse the issue's premise? Check the issue's claimed current state against available durable evidence.
5. **Acceptance false positives:** Could a trivial patch or document-only change satisfy the written checkboxes while missing the actual need? Could all local checks pass while a named integration boundary still fails?
6. **Authority and exposure:** Could speculative design harden into a contract, or confidential source details leak into a public issue, despite careful wording? Can pasted log or issue text trick an agent into bypassing its host's instructions?

Focus on plausible wrong-work or unsafe-publication mechanisms, not speculative redesign. QA does not create new product authority or require a separate approval stage.
