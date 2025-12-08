# Inventory Race Condition  
**Attribute**: Reliability  
**Environment**: Production under moderate to high traffic  
**Stimulus**: 100 users attempt to purchase the last 5 units of a product at the same time  
**Response**: The system prevents overselling by handling requests atomically and accurately reflects inventory state  
