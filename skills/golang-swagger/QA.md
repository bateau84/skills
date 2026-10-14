# golang-swagger Quality Assurance

Adversarial validation for any agent. Assume competent production and normal review; attack residual false confidence without inventing new requirements.

## QA criteria

Critic compares a real request/response/error/auth path to the spec and asks whether generated clients could behave correctly. Probe nullable/omitted fields, undocumented errors, auth failure, validation edge values, and old client compatibility.

Block when consumers rely on a materially false API contract or a generated artifact hides an unauthorized breaking change. Cosmetic description omissions are proportional.

## QA depth

Increase depth with external consumers, schema breadth, compatibility lifetime, auth/security, polymorphism/nullable semantics, and code-generation reliance.
