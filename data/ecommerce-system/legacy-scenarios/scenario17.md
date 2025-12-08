# Order Processing Failure  
**Attribute**: Reliability  
**Environment**: Production with transient infrastructure issues  
**Stimulus**: A database write fails during order placement  
**Response**: The system retries the operation or rolls back changes to avoid inconsistent order states  
