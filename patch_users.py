import requests
import json

# --- 1. YOUR SETTINGS ---
# Use the URL you found earlier
BASE_URL = "https://showntime-matthew.staffbase.com/api/users"
# Make sure your Token is pasted inside the quotes
import os

API_TOKEN = os.getenv("STAFFBASE_API_TOKEN")
if not API_TOKEN:
    raise RuntimeError("Missing STAFFBASE_API_TOKEN environment variable")
 

# --- 2. THE SECRET HEADERS ---
# We updated the Content-Type to the V2 version you found!
HEADERS = {
    "Authorization": f"Basic {API_TOKEN}",
    "Content-Type": "application/vnd.staffbase.accessors.users.v2+json",
    "Accept": "application/vnd.staffbase.accessors.users.v2+json"
}

def run_update():
    print("🚀 Starting Staffbase Update...")
    
    try:
        # Load your fixed users.json file
        with open('users.json', 'r') as file:
            users = json.load(file)
    except Exception as e:
        print(f"❌ Error: Could not read users.json. Details: {e}")
        return

    for user in users:
        # Transformation: Using Legacy 'EmployeeID' and 'Dept_ID'
        user_id = user.get("EmployeeID")
        new_dept = user.get("Dept_ID")

        # The data package (Payload)
        payload = {
            "profile": {
                "department": new_dept
            }
        }

        # Send the update to the specific user ID
        url = f"{BASE_URL}/{user_id}"

        try:
            # PATCH is the correct way to update just the department
            response = requests.patch(url, headers=HEADERS, json=payload)

            if response.status_code in [200, 204]:
                print(f"✅ SUCCESS: {user.get('GivenName')} (ID: {user_id}) updated to {new_dept}")
            else:
                print(f"❌ FAILED: User {user_id} - Error {response.status_code}")
                # This helps you see why it failed (e.g., if the ID doesn't exist)
                print(f"   Reason: {response.text}")
        
        except Exception as e:
            print(f"⚠️ Network error for {user_id}: {e}")

if __name__ == "__main__":
    run_update()
