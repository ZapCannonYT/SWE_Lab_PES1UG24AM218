# Lab 3: Architecture and Component Diagram

Architecture design for the **Personalized Meal & Diet Subscription Manager**, building on the requirements from Lab 2.

## What I did

- **Chose Client-Server architecture** and justified it against Layered and Microservices alternatives.
- **Reasons given:** centralized control over sensitive clinical data (RBAC, AES-256, audit logging in one place) and a single source of truth for the Draft → Reviewed → Approved meal-plan workflow.
- **Component diagram** with a Subscriber Client App and a Dietitian Dashboard Client talking to a Subscriber & Health Data Server, a Meal Plan Generation Server and a Delivery & Notification Server through named interfaces.
- **Security advantage and performance benefit** of the chosen style (no persistent health data on clients; shared caching and connection pooling for the 2.5 s target at 500 concurrent requests).
- **Requirements traceability table** mapping each FR/NFR to the component and interface that satisfies it.

## Contents

- `PES1UG24AM218_SWE_LAB-03_P19.pdf` — the full write-up (6 pages)
