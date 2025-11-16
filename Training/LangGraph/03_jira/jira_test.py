#!/usr/bin/env python3
"""
Simple test script to validate Jira API connectivity and issue creation.
Tests the minimum call needed to create a Jira issue.
"""

import json
import os
from dotenv import load_dotenv
from langchain_community.utilities.jira import JiraAPIWrapper

# Load environment variables
load_dotenv(override=True)

def test_jira_connection():
    """Test basic Jira connection and retrieve available projects."""
    print("=" * 60)
    print("Testing Jira Connection")
    print("=" * 60)

    # Get credentials from environment
    jira_instance_url = os.environ.get("JIRA_INSTANCE_URL")
    jira_username = os.environ.get("JIRA_USERNAME")
    jira_api_token = os.environ.get("JIRA_API_TOKEN")

    print(f"Jira Instance URL: {jira_instance_url}")
    print(f"Jira Username: {jira_username}")
    print(f"Jira API Token: {'*' * 20}...")

    if not all([jira_instance_url, jira_username, jira_api_token]):
        print("ERROR: Missing required Jira environment variables!")
        return False

    try:
        # Initialize JiraAPIWrapper
        jira_api = JiraAPIWrapper(
            jira_instance_url=jira_instance_url,
            jira_username=jira_username,
            jira_api_token=jira_api_token
        )
        print("\n✓ Successfully initialized JiraAPIWrapper")

        # Test 1: Get available projects
        print("\n" + "=" * 60)
        print("Test 1: Retrieving Available Projects")
        print("=" * 60)
        try:
            projects = jira_api.jira.projects()
            print(f"Found {len(projects)} projects:")
            for project in projects:
                # Handle both dict and object responses
                if isinstance(project, dict):
                    print(f"  - {project.get('key')}: {project.get('name')}")
                else:
                    print(f"  - {project.key}: {project.name}")
        except Exception as e:
            print(f"ERROR retrieving projects: {str(e)}")
            return False

        # Test 2: Get project details for AUT
        print("\n" + "=" * 60)
        print("Test 2: Retrieving AUT Project Details")
        print("=" * 60)
        try:
            aut_project = jira_api.jira.project("AUT")
            # Handle both dict and object responses
            if isinstance(aut_project, dict):
                print(f"✓ Found AUT project: {aut_project.get('name')}")
                print(f"  Project Key: {aut_project.get('key')}")
                print(f"  Project ID: {aut_project.get('id')}")
            else:
                print(f"✓ Found AUT project: {aut_project.name}")
                print(f"  Project Key: {aut_project.key}")
                print(f"  Project ID: {aut_project.id}")
        except Exception as e:
            print(f"ERROR retrieving AUT project: {str(e)}")
            return False

        # Test 3: Get available issue types in AUT project
        print("\n" + "=" * 60)
        print("Test 3: Retrieving Available Issue Types in AUT")
        print("=" * 60)
        try:
            issue_types = jira_api.jira.issue_types_for_project("AUT")
            print(f"Found {len(issue_types)} issue types:")
            for issue_type in issue_types:
                print(f"  - {issue_type.name} (ID: {issue_type.id})")
        except Exception as e:
            print(f"ERROR retrieving issue types: {str(e)}")

        # Test 4: Create a test issue
        print("\n" + "=" * 60)
        print("Test 4: Creating a Test Issue")
        print("=" * 60)

        test_issue_data = {
            "summary": "Test Issue from jira_test.py",
            "description": "This is a test issue created to validate Jira API connectivity.",
            "issuetype": "Story",
            "project": "AUT"
        }

        print(f"Creating issue with data:")
        print(json.dumps(test_issue_data, indent=2))

        try:
            # Convert to JSON string for the API
            issue_json = json.dumps(test_issue_data)
            result = jira_api.issue_create(issue_json)
            print(f"\n✓ Successfully created issue!")
            print(f"  Result: {result}")
            return True
        except Exception as e:
            print(f"\nERROR creating issue: {str(e)}")
            print(f"Error type: {type(e).__name__}")

            # Try alternative approach with direct Jira client
            print("\n" + "=" * 60)
            print("Test 4b: Trying Direct Jira Client Approach")
            print("=" * 60)
            try:
                issue_dict = {
                    "summary": "Test Issue from Direct Jira Client",
                    "description": "This is a test using the direct Jira client.",
                    "issuetype": {"name": "Story"},
                    "project": {"key": "AUT"}
                }
                print(f"Creating issue with direct client:")
                print(json.dumps(issue_dict, indent=2))

                new_issue = jira_api.jira.create_issue(fields=issue_dict)
                print(f"\n✓ Successfully created issue using direct client!")
                print(f"  Issue Key: {new_issue.key}")
                print(f"  Issue URL: {new_issue.permalink()}")
                return True
            except Exception as e2:
                print(f"\nERROR with direct client: {str(e2)}")
                return False

    except Exception as e:
        print(f"ERROR initializing JiraAPIWrapper: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_jira_connection()
    print("\n" + "=" * 60)
    if success:
        print("✓ All Jira tests passed!")
    else:
        print("✗ Jira tests failed - check errors above")
    print("=" * 60)
