import argparse
import asyncio
import json
from .simulate_traffic import simulate_traffic

def parse_arguments():
    parser = argparse.ArgumentParser(description="Simulate traffic to a web endpoint.")
    parser.add_argument('url', type=str, help='The URL of the API endpoint.')
    parser.add_argument('method', type=str, choices=['GET', 'POST', 'PUT', 'DELETE'], help='The HTTP method to use for the requests.')
    parser.add_argument('payload_schema', type=str, help='The JSON file path that contains the payload schema.')
    parser.add_argument('num_requests', type=int, help='The number of requests to be sent.')
    parser.add_argument('timeout', type=int, help='The timeout in seconds for each request.')
    parser.add_argument('--progress_bar', action='store_true', help='Display a progress bar during the simulation.')
    return parser.parse_args()

def validate_arguments(args):
    # Validate URL, method, and num_requests in args here
    # Load and validate payload_schema from JSON file
    try:
        with open(args.payload_schema, 'r') as f:
            payload_schema = json.load(f)
        args.payload_schema = payload_schema
    except Exception as e:
        raise ValueError(f"Invalid payload schema file: {e}")

def main():
    args = parse_arguments()
    validate_arguments(args)
    if not asyncio.get_event_loop().is_running():
        asyncio.run(simulate_traffic(
            url=args.url,
            method=args.method,
            payload_schema=args.payload_schema,
            num_requests=args.num_requests,
            timeout=args.timeout,
            progress_bar=args.progress_bar
        ))
    else:
        asyncio.create_task(simulate_traffic(
            url=args.url,
            method=args.method,
            payload_schema=args.payload_schema,
            num_requests=args.num_requests,
            timeout=args.timeout,
            progress_bar=args.progress_bar
        ))

if __name__ == "__main__":
    main()