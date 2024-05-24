import pandas as pd
import random
from datetime import datetime, timedelta

# Generate synthetic web server logs with additional games and countries
def generate_logs(num_entries):
    # Define lists of possible values for each column
    ips = ['192.168.0.1', '10.0.0.1', '172.16.0.1']
    request_types = ['GET', 'POST']
    resources = ['/index.html', '/about.html', '/contact.html']
    status_codes = [200, 404, 500]
    users = ['user1', 'user2', 'user3']
    sports = ['football', 'basketball', 'soccer', 'tennis', 'golf']  # Add more games
    countries = {
        'North America': ['USA', 'Canada', 'Mexico'],
        'South America': ['Brazil', 'Argentina', 'Chile'],
        'Europe': ['UK', 'Germany', 'France'],
        'Africa': ['Nigeria', 'South Africa', 'Kenya'],
        'Asia': ['China', 'India', 'Japan'],
        'Oceania': ['Australia', 'New Zealand', 'Fiji']
    }
    genders = ['Male', 'Female']
    
    
    # Initialize empty list to store logs
    logs = []
    
    # Generate logs
    for _ in range(num_entries):
        timestamp = datetime.now() - timedelta(minutes=random.randint(0, 10080))  # Random timestamp within the last week
        ip = random.choice(ips)
        request_type = random.choice(request_types)
        resource = random.choice(resources)
        status_code = random.choice(status_codes)
        user = random.choice(users)
        sport = random.choice(sports)
        
        # Randomly select a country from each continent
        continent = random.choice(list(countries.keys()))
        country = random.choice(countries[continent])
        
        gender = random.choice(genders)
        
        log = {'Timestamp': timestamp, 'IP Address': ip, 'Request Type': request_type,
               'Resource': resource, 'Status Code': status_code, 'User': user,
               'Sport': sport, 'Country': country, 'Gender': gender, 'Continent': continent }
        
        logs.append(log)
    
    return logs

# Generate logs with at least 1000 entries
logs = generate_logs(1000)
df = pd.DataFrame(logs)

# Save logs to CSV file
df.to_csv('web_server_logsfile.csv', index=False)
