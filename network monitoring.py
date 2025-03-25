#Chatgpt
import socket
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class NetworkMonitorError(Exception):
    """Custom exception for network monitoring errors."""
    pass

class NetworkMonitor:
    def __init__(self, servers, timeout=5, max_threads=4):
        self.servers = servers
        self.timeout = timeout
        self.max_threads = max_threads
    
    def check_server(self, server, port=80):
        """Check if a server is reachable on a specific port."""
        try:
            logging.info(f"Checking server {server} on port {port}...")
            sock = socket.create_connection((server, port), timeout=self.timeout)
            sock.close()
            logging.info(f"Server {server} is reachable.")
            return (server, True)
        except socket.timeout:
            logging.error(f"Connection to {server} timed out.")
            return (server, False)
        except socket.error as e:
            logging.error(f"Failed to connect to {server}: {e}")
            return (server, False)

    def check_servers_concurrently(self):
        """Check servers concurrently using multithreading."""
        threads = []
        results = []

        def target(server):
            result = self.check_server(server)
            results.append(result)

        for server in self.servers:
            thread = threading.Thread(target=target, args=(server,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return results

    def run(self):
        """Run the network monitoring process."""
        try:
            results = self.check_servers_concurrently()
            logging.info("Network monitoring results:")
            for server, is_reachable in results:
                status = "UP" if is_reachable else "DOWN"
                logging.info(f"{server}: {status}")
        except NetworkMonitorError as e:
            logging.error(f"Network monitoring error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

# Example usage
def main():
    servers = ["google.com", "example.com", "nonexistentwebsite.xyz"]
    monitor = NetworkMonitor(servers)
    monitor.run()

if __name__ == "__main__":
    main()

