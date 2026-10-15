# user-stories-and-scenarios Quality Assurance

## User Story

### QA criteria

- Find a plausible implementation that satisfies the literal story while leaving the actor unable to tell whether the goal succeeded.
- Replace the named actor with a materially different user context and check whether the story was actually generic when it should have split.
- Search for hidden UI/architecture assumptions disguised as human goals.
- Check whether the story was reverse-engineered from the proposed feature rather than derived from accepted user/product need.
- Attack compound stories whose multiple goals can succeed/fail independently.
- Look for success defined only by system completion rather than what the human can perceive, decide, or accomplish.

### QA depth

Increase depth where a vague story could steer many downstream design decisions.

## Design Scenario

### QA criteria

- Walk the scenario as a distracted, mistaken, interrupted, or partially informed person rather than the ideal user.
- Find states where the scenario silently assumes knowledge the person has not been given.
- Attack failure paths that end in "shows an error" without a recoverable or truthful human outcome.
- Search for a scenario whose success is really a backend event the person cannot perceive.
- Check whether the scenario presupposes a specific UI pattern and thereby hides alternative designs.
- Look for missing abandonment/re-entry behavior when interruption is realistic.
- Check whether a mock/future capability is being used to make the journey appear complete.

### QA depth

Increase depth where the scenario is intended to constrain many flows or serve as acceptance evidence.
