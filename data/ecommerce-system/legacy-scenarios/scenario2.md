# Scaling Under Peak Load
**Attribute**: Scalability
**Environment**: The system operates in a production environment with variable user traffic, including occasional peak loads triggered by external events.
**Stimulus**: A sudden surge in concurrent user activity, such as 10x the average traffic within a short time window (e.g., during a flash sale or unplanned event).
**Response**: The system dynamically scales resources to handle the increased load without degrading response times beyond 3 seconds for 95% of requests, ensuring system stability and maintaining core functionality.[scenario3.md](scenario3.md)