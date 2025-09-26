from flask import Flask, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Interview data stored locally in a dictionary (similar to JSON)
# The interview times are set dynamically for demonstration purposes.
interview_details = {
    "CAND001": {
        "UserName": "John Doe",
        "Role": "Software Developer",
        # Scenario 1: Interview is more than 6 hours away
        "InterviewScheduledTime": (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    },
    "CAND002": {
        "UserName": "Jane Smith",
        "Role": "Data Analyst",
        # Scenario 2: Interview is less than 6 hours away
        "InterviewScheduledTime": (datetime.now() + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S")
    },
    "CAND003": {
        "UserName": "Peter Jones",
        "Role": "Project Manager",
        "InterviewScheduledTime": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    }
}

@app.route('/interview/<string:candidate_id>', methods=['GET'])
def get_interview_details(candidate_id):
    """
    Fetches the interview details for a specific candidate ID.
    """
    if candidate_id in interview_details:
        candidate_info = interview_details[candidate_id]
        
        # Convert the interview schedule string back to a datetime object for comparison
        interview_time = datetime.strptime(candidate_info["InterviewScheduledTime"], "%Y-%m-%d %H:%M:%S")
        
        # Calculate the time difference between now and the interview time
        time_difference = interview_time - datetime.now()

        # Base response data
        response_data = {
            "CandidateID": candidate_id,
            "UserName": candidate_info["UserName"],
            "Role": candidate_info["Role"],
            "InterviewScheduledTime": candidate_info["InterviewScheduledTime"]
        }

        # Scenario 1: Time to start the interview is more than 6 hours
        if time_difference > timedelta(hours=6):
            response_data["Status"] = "Interview is scheduled."
            response_data["Notes"] = "Full interview details are available. Please prepare accordingly."
        
        # Scenario 2: Time to start the interview is less than 6 hours
        else:
            response_data["Status"] = "Interview is starting soon."
            response_data["Notes"] = "Please be ready for your interview. Ensure your setup is working."

        return jsonify(response_data), 200
    
    else:
        # If the CandidateID is not found in our data
        return jsonify({"error": "CandidateID not found"}), 404

if __name__ == '__main__':
    # Runs the app in debug mode.
     app.run(host='0.0.0.0')