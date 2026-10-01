Patrick Mannix

Livestream Co-Host AI Companion: Prototype Proposal

Slide 1: Title & Working Title

Title: Autonomous Livestream Companion Architecture
Working Title: Project Crowd-Conscious AI Co-Host

Slide 2: Project Format & Description

Project Format: Real-time multi-agent LLM livestream overlay integrated via WebSockets with YouTube and Twitch chat APIs, driven by viewer subscription triggers and a persistent local context model.
Project Description: An autonomous AI co-host integrated into live streaming platforms that dynamically moderates and converses with chat in exchange for subscription milestones while maintaining an independent personality and continuous situational awareness of the streamer.

Slide 3: User & Integrator Experience (Part 1)

Viewers experience the AI companion as a distinct digital entity on stream that reacts instantly to chat messages, addresses specific users by name, and adopts a unique, unscripted persona.
When a viewer triggers a subscription milestone, the AI alters its current behavior loop to fulfill custom prompts or launch interactive mini-segments requested by the subscriber.
Simultaneously, the streamer interacts with the AI through an audio-to-text feedback channel, allowing the human host to pivot conversation topics or signal the AI to back off during critical gameplay moments.

Slide 4: User & Integrator Experience (Part 2)

The system balances two independent streams of consciousness: one dedicated to processing high-velocity public chat inputs and another dedicated to maintaining a private context window with the primary host.
Integrators or platform operators deploy the system by authenticating via OAuth with YouTube and Twitch developer portals and mapping custom text-to-speech visual avatars to the overlay window.
The interface provides real-time transparency indicators showing whether the AI is currently processing public chat, responding to a subscriber trigger, or listening to the main host.

Slide 5: System Description (Operational Architecture)

The application runs on a local orchestration server utilizing LangChain to route incoming WebSocket events from Twitch and YouTube chat APIs into separate processing queues.
A fine-tuned open-weight LLM instance handles persona generation and response formulation, constrained by a strict safety filter that drops flagged toxic or spam inputs before they reach the text-to-speech and avatar animation pipeline.
Subscription webhook events bypass standard message queues to grant immediate priority weighting in the generation pipeline, forcing the AI to acknowledge financial contributions within a three-second window.
The system continuously logs chat state histories into a localized vector database, allowing the AI to recall recurring community inside jokes and user names across multiple broadcast sessions.

Slide 6: Explicit Dependency

Explicit Dependency: This project depends on stable, low-latency WebSocket connection stability and uninterrupted API rate limits from Twitch and YouTube developer portals.
If streaming platform APIs experience throttling, rate-limiting, or unexpected schema deprecations, the real-time chat polling loop fails, causing the AI co-host to freeze or output delayed responses that break the synchronized illusion of a live conversational partner.
