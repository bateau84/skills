# golang-swagger Reviewer Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

Reviewer compares generated/OpenAPI contract with the **real HTTP surface**:

- routes/methods/path/query/header parameters and content types match actual handlers/router behavior;
- request/response schemas preserve required/optional/nullable/omitempty/zero-value semantics and validation constraints;
- every externally meaningful success/error status and error body is documented consistently; auth/security schemes/scopes reflect middleware enforcement;
- examples are valid against the schema and do not invent behavior; enums/defaults/formats match runtime types;
- generation annotations/source are canonical and reproducible; generated output is not hand-edited into drift;
- compatibility-sensitive schema changes (required field, type/enum removal, endpoint rename) are treated as API evolution, not documentation-only changes.
