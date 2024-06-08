# Exchange Rates Newsletter

## Project Overview
The Exchange Rates Newsletter is an automated service that sends subscribers daily updates on current exchange rates along with advice on which currencies are worth buying based on market trends.

## Key Features
- **Daily Exchange Rates Updates:** Automatically fetch and send the latest exchange rates.
- **Expert Buying Advice:** Provide recommendations on which currencies to buy.
- **Personalized Emails:** Tailor content to each subscriber.
- **Subscription Management:** Easy sign-up, unsubscribe, and preference updates.

## Future Enhancements
- Detailed financial analysis and forecasts.
- Web-based dashboard for historical trends.
- Premium subscription plans with additional features.

By implementing the Exchange Rates Newsletter, users will receive timely and valuable information to make better financial decisions in the dynamic currency exchange market.

## After first docker-compose build create two topics
- kafka-topics --create --bootstrap-server localhost:29092 --partitions 1 --replication-factor 1 --topic currency-rates
- kafka-topics --create --bootstrap-server localhost:29092 --partitions 1 --replication-factor 1 --topic bitcoin-rates

## Check topics list 
- kafka-topics --list --bootstrap-server localhost:29092
