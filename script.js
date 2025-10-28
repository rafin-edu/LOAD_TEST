import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 10,         // Number of virtual users
  duration: '300s',  // Total test duration
};

export default function () {
  // The URL of your Firebase API or server endpoint that updates the visit count
  const url = 'https://yaeko-pajamaed-contrapuntally.ngrok-free.dev'; 
  
  // You can pass data like user ID or other params if necessary
  const payload = JSON.stringify({
    userId: 'someUserId', // Make this dynamic or random if needed
  });

  // Request to the API endpoint
  const res = http.post(url, payload, {
    headers: { 'Content-Type': 'application/json' },
  });

  // Check if the response was successful (200 OK)
  check(res, {
    'is status 200': (r) => r.status === 200,
  });

  // Sleep to simulate real user activity
  sleep(0.1);  // Sleep for 1 second between requests
}
