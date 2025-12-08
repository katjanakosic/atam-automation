# Description
The model problem represents a simple online store that allows users to browse products, add items to a shopping cart, and process orders. The main goals of the system are to support a large number of concurrent users, to ensure a seamless customer experience even during peak traffic events such as Black Friday, and to provide a reliable inventory and order management system to prevent overselling and stock inconsistencies.

# System Interactions
The system interacts with various external and internal components to ensure smooth operation. It integrates with third party payment gateways such as Stripe and PayPal to handle secure transactions. It also provides APIs to connect to external inventory management systems, enabling real-time stock synchronisation. Finally, the system facilitates user interaction, allowing customers to browse products, make purchases and submit reviews within the platform.

# Technical constraints
The system is required to use specific programming frameworks, with React for the front-end and Spring Boot for the back-end. It must also be hosted on a cloud infrastructure such as AWS or Microsoft Azure to ensure scalability, reliability and deployment flexibility.