import os
import subprocess
import psycopg2
import schedule
import time
from datetime import datetime
import json  # Import the json module

print(f"Starting SpeedTest.")

def run_speedtest(server_id=None):
    try:
        command = ['speedtest-cli', '--json']
        if server_id:
            command.extend(['--server', str(server_id)])

        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
        error_output = result.stderr  # Capture stderr output
        
        data = json.loads(output)
        ping = data['ping']
        download = data['download'] / (1024 * 1024)  # Convert from bits/s to Mbps
        upload = data['upload'] / (1024 * 1024)  # Convert from bits/s to Mbps
        server_name = data['server']['name']
        server_country = data['server']['country']
        server_host = data['server']['host']
        server_id = data['server']['id']

        print(f"server_id: {server_id}")
        
        return ping, download, upload, server_name, server_country, server_host
    except subprocess.CalledProcessError as e:
        print(f"Error running speedtest-cli: {e}")
        print(f"Command output: {e.output}")
        print(f"Command error output: {e.stderr}")
        return None, None, None, None, None, None
    except ValueError as e:
        print(f"Error parsing speedtest output: {e}")
        return None, None, None, None, None, None

def save_to_db(ping, download, upload, server_name, server_country, server_host):
    try:
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD']
        )
        cur = conn.cursor()
        
        cur.execute("""
        INSERT INTO public.speedtest_results (ping, download, upload, server_name, server_country, server_host)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (ping, download, upload, server_name, server_country, server_host))
        
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def job(server_id=None):
    ping, download, upload, server_name, server_country, server_host = run_speedtest(server_id)
    if ping is not None and download is not None and upload is not None:
        save_to_db(ping, download, upload, server_name, server_country, server_host)
        print(f"Speedtest completed at {datetime.now()} with ping={ping}, download={download}, upload={upload}, server={server_name}, country={server_country}, host={server_host}")
    else:
        print(f"Speedtest failed at {datetime.now()}")

if __name__ == "__main__":    
    # Manually set a server ID
    selected_server_id = os.getenv('SERVER_ID')

    if selected_server_id:
        selected_server_id = int(selected_server_id)  # Convert to integer if it exists
    else:
        selected_server_id = None  # Default to None if not set
    
    # Run the job immediately upon script initiation
    print(f"Firts time run...")
    job(selected_server_id)

    print(f"Schedule is running...")
    # Then, schedule it to run every hour
    schedule.every(15).minutes.do(job, selected_server_id)
    
    # Continue running the scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(1)
