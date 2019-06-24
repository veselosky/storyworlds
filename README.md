# Storyworlds

DO NOT USE. Just an experimental project right now. Guaranteed to change in
backward-incompatible ways that will cause data loss.

## What is it for?

Storyworlds is a tool for authors, journalists, game creators, and anyone who
wants to tell stories about a complex, interconnected world (real or imagined).
Storyworlds gives you tools to catalog and visualize *facts* about your world
(people, places, events) and how they are connected. It also gives you tools
to organize the *stories* you tell involving those facts.

Some useful visualizations the tool will provide:

* World timeline: Visualize recorded events on a timeline.
* Character timeline: Visualize the events from a single character's perspective.
* Family tree: Visualize the tree of family relationships for a given character.
* Social graph: Visualize a character's relationship network.
* Character connections: Visualize the people, places, and events shared by a set
  of characters.
* World maps: Visualize the geography of the world or part of it as a map.
* Campaign maps: Visualize (world or character) events on a map in chronological order.
* Story boards: Visualize the story events as told (as opposed to chronologically).

## Design Issues Needing Resolution

* Ambiguous dates: Sometimes an exact date is not known, but is known to fall
  before or after some other date or event. Sorting should account for this
  somehow.
* Conflicting sources: Sometimes sources conflict with each other in mutually
  exclusive ways. Ideally we could record these conflicts and visualize them,
  perhaps even marking one as "correct".
* Data model: Currently extremely simplistic. Needs tons of work, listed separately.
* Data entry: Fielded data entry as provided by the Django admin and most other
  interfaces is a clumsy UX. This will get even more tedious as the data model
  becomes more complex. A more intelligent entry form will be needed.

### Data Model Issues

Event significance: Some events are more significant than others. When zooming
out of a timeline, less significant events should fade, leaving only the most
significant events visible. Also, some events may be significant to a character,
but not in the overall context of the world, and vice-versa.

Storage of ambiguous or conflicting dates, and correct sorting thereof, needs
to be modeled correctly.

In general, the types of entities and relationships being stored here may call
for a graph database. Characters need to be related to other people, places,
organizations, with relationships having their own types, start dates, and end
dates. Many of the visualizations are in the form of graphs.

Have a look at Apache TinkerPop, Neo4j, and AWS Neptune for graph data modeling.
