#!/usr/bin/env python3
"""
Example UDP client to receive Entity Broadcaster messages.

This script demonstrates how external applications can listen for
entity state changes broadcasted by the Home Assistant Entity Broadcaster integration.
"""

import json
import socket
import sys
from datetime import datetime


def listen_for_broadcasts(port: int = 8888):
    """Listen for UDP broadcasts from Entity Broadcaster."""
    print(f"Starting UDP listener on port {port}")
    print("Waiting for entity state broadcasts... (Press Ctrl+C to stop)")
    print("-" * 60)

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Bind to all available interfaces
        sock.bind(("", port))

        while True:
            try:
                # Receive data
                data, addr = sock.recvfrom(4096)

                # Decode JSON message
                message = json.loads(data.decode("utf-8"))

                # Display the received message
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] From {addr[0]}:")
                print(f"  Broadcaster: {message.get('broadcaster_name', 'Unknown')}")
                print(f"  Entity: {message.get('entity_id', 'Unknown')}")
                print(f"  State: {message.get('state', 'Unknown')}")

                # Show some key attributes if available
                attributes = message.get("attributes", {})
                if attributes:
                    # Show friendly name if available
                    if "friendly_name" in attributes:
                        print(f"  Name: {attributes['friendly_name']}")

                    # Show unit of measurement if available
                    if "unit_of_measurement" in attributes:
                        print(f"  Unit: {attributes['unit_of_measurement']}")

                    # Show device class if available
                    if "device_class" in attributes:
                        print(f"  Device Class: {attributes['device_class']}")

                print("-" * 60)

            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
            except UnicodeDecodeError as e:
                print(f"Failed to decode message: {e}")

    except KeyboardInterrupt:
        print("\nStopping UDP listener...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()


if __name__ == "__main__":
    # Get port from command line argument or use default
    port = 8888
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8888.")

    listen_for_broadcasts(port)
