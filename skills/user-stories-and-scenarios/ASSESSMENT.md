# user-stories-and-scenarios Assessment

## User Story

### Review criteria

- The story traces to accepted product/user authority and does not create a new capability or promise.
- Actor/context is specific enough to explain why this person's situation matters to the design.
- Trigger, goal, and observable success describe human intent rather than a feature, screen, API, or technical mechanism.
- One coherent goal is represented; materially different goals/actors are not packed into one story.
- Observable success is actually perceivable by the person rather than an internal implementation event.
- The story is distinct from a Behavioral Requirement: it informs human-facing design without pretending to define complete normative system semantics.
- Concrete journeys, branches, and failure situations that matter are delegated to Scenarios rather than overloaded into the story.

### Review depth

Scale with consequence, actor diversity, ambiguity of the human goal, and amount of downstream design that depends on the story.

## Design Scenario

### Review criteria

- The scenario traces to accepted human-facing authority and does not create product scope.
- Context is concrete enough that it can influence design rather than saying only "a user uses the feature."
- Goal is human-centered and separated from the interface mechanism.
- The sequence is end-to-end and human-visible; backend/API/database operations are absent unless they are themselves visible constraints.
- At least one material failure, interruption, mistake, degraded response, or edge condition is represented where applicable.
- Observable outcome makes success/recovery/failure recognizable to the person.
- Assumptions about user knowledge/context are explicit when consequential.
- The scenario is distinct from a Quality Scenario and can be reused for design validation/acceptance.

### Review depth

Scale with journey length, interruption/recovery complexity, pressure, and number of meaningful branches.
