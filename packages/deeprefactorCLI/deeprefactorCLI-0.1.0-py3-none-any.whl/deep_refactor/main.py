from rich.console import Console
from rich.padding import Padding
from datetime import datetime
import typer
import requests
import keyring
from rich import box
from rich.markup import escape
from rich.panel import Panel
from rich.text import Text
from urllib.parse import quote
import json
from typing import List
import os
from pathlib import Path
import hashlib

app = typer.Typer()
console = Console()


# Helper functions
def splitByCapital(string):
    return "".join(" " + c if c.isupper() else c for c in string).strip()


def get_color(analysis_type):
    colors = {
        "CodeQuality": "#E53935",
        "DocumentationQuality": "#1E88E5",
        "BugDetection": "#43A047",
        "SecurityAnalysis": "#8E24AA",
        "TestCoverage": "#FB8C00",
        "PerformanceAnalysis": "#00ACB9",
        "AccessibilityAnalysis": "#FDD835",
        "ArchitectureAnalysis": "#6D4C41",
        "ContinuousIntegration": "#3949AB",
        "ResponsivenessAnalysis": "#FF5722",
    }
    return colors.get(analysis_type, "white")


def escape(text):
    # Implement any necessary escaping here
    return text


def display_feedback_comment(comment):
    # Format the line(s) text
    line_range = (
        f"{comment['startLine']}"
        if comment["startLine"] == comment["endLine"]
        else f"{comment['startLine']} - {comment['endLine']}"
    )

    # Create the panel content with padding
    panel_content = Padding(
        Text.assemble(
            ("Type: ", "bold"),
            f"{splitByCapital(comment['type'])}\n",
            ("Severity: ", "bold"),
            f"{comment['severity']}\n",
            ("Comment: ", "bold"),
            f"{escape(comment['message'])}\n",
            ("Recommendation: ", "bold"),
            f"{escape(comment['recommendation'])}\n",
            ("Line(s): ", "bold"),
            line_range + "\n",
        ),
        (1, 2),
    )

    # Get the appropriate color for the border
    border_color = get_color(comment["type"])

    # Create and print the panel
    panel = Panel(
        panel_content,
        title=f"[bold]{splitByCapital(comment['type'])}[/]",
        box=box.ROUNDED,
        border_style=border_color,
        expand=False,
    )
    console = Console()
    console.print(panel)


@app.command()
def login():
    console.print("\n")
    api_key = typer.prompt("Enter your API key", hide_input=True)

    # Basic validation can be added here
    response = requests.post(
        "http://localhost:8080/cli/validate-api-key", json={"api_key": api_key}
    )

    if response.status_code == 200:
        keyring.set_password("deep-refactor", "api_key", api_key)
        console.print("\n")
        typer.echo("Logged in successfully!")
        console.print("\n")
    else:
        console.print("\n")
        typer.echo("Invalid API key. Please try again.")
        console.print("\n")


@app.command()
def logout():
    keyring.delete_password("deep-refactor", "api_key")
    console.print("\n")
    typer.echo("Logged out successfully!")
    console.print("\n")


@app.command()
def repos():
    api_key = keyring.get_password("deep-refactor", "api_key")
    if not api_key:
        console.print("\n")
        console.print("You are not logged in. Please log in first.", style="bold red")
        raise typer.Exit()
        console.print("\n")

    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get("http://localhost:8080/cli/repos", headers=headers)

    if response.status_code == 200:
        repos = response.json()
        count = 1
        for repo in repos:
            project_name = (
                f"[bold cyan]Project Name:[/bold cyan] {repo['project_name']}"
            )
            languages = ", ".join(repo["languages"])
            creation_date = datetime.fromisoformat(repo["creation_date"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            last_modified = datetime.fromisoformat(repo["last_modified"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            repo_details = f"{project_name}\n[bold cyan]Languages:[/bold cyan] {languages}\n\nCreation Date: {creation_date}\nLast Modified: {last_modified}"
            panel = Panel(
                Padding(repo_details, (1, 2)),
                expand=False,
                title=f"Repo - {count}",
                border_style="blue",
            )
            if count == 1:
                console.print("\n")
            console.print(panel)
            console.print("\n")
            count += 1
    else:
        console.print("\n")
        console.print(
            "Failed to fetch repositories. Please check your API key.", style="bold red"
        )
        console.print("\n")


@app.command()
def repo(project_name: str):
    api_key = keyring.get_password("deep-refactor", "api_key")
    if not api_key:
        console.print("You are not logged in. Please log in first.", style="bold red")
        raise typer.Exit()

    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(
        f"http://localhost:8080/cli/repo-details/{project_name}", headers=headers
    )

    if response.status_code == 200:
        repo_info = response.json()
        project_details = repo_info["project"]
        files_info = repo_info["files"]
        comments_by_type = repo_info["commentsByType"]

        # Format and display the project details
        project_panel_content = (
            f"[bold cyan]Project Name:[/bold cyan] {project_details['project_name']}\n"
            f"[bold cyan]Languages:[/bold cyan] {', '.join(project_details['languages'])}\n"
            f"Creation Date: {project_details['creation_date']}\n"
            f"Last Modified: {project_details['last_modified']}"
        )

        project_panel = Panel(
            Padding(project_panel_content, (1, 2)),
            title=project_details["project_name"],
            expand=False,
            border_style="green",
        )

        console.print("\n")
        console.print(project_panel)
        console.print("\n")

        # Display comment analysis types
        analysis_text = Text()
        analysis_text.append("\n")
        for comment_type in comments_by_type:
            # Append each analysis type and count in a different color
            analysis_text.append(
                f"{splitByCapital(comment_type['type'])}: ",
                style=f"bold {get_color(comment_type['type'])}",
            )
            analysis_text.append(f"{comment_type['count']}\n", style="bold")

        # Create a panel with the analysis types text
        analysis_panel = Panel(
            Padding(analysis_text, (1, 2)),
            title="[bold]Analysis Types[/]",
            expand=False,
            border_style="blue",
        )
        console.print(analysis_panel)
        console.print("\n")

        file_comments_map = {}
        for file in files_info:
            if file["count"] == "0":
                continue
            file_path = file["path"]
            severity = file["severity"] or "No Severity"
            count = int(file["count"])

            if file_path not in file_comments_map:
                file_comments_map[file_path] = {
                    "Low": 0,
                    "Medium": 0,
                    "Critical": 0,
                }  # Initialize counts

            file_comments_map[file_path][severity] += count

        feedback_text = Text()
        for file_path, comments in file_comments_map.items():
            feedback_text.append(f"File: {file_path}\n", style="bold blue")
            if comments["Low"] > 0:
                feedback_text.append(
                    f"  - Low Issues: {comments['Low']}\n", style="bold green"
                )
            if comments["Medium"] > 0:
                feedback_text.append(
                    f"  - Medium Issues: {comments['Medium']}\n", style="bold yellow"
                )
            if comments["Critical"] > 0:
                feedback_text.append(
                    f"  - Critical Issues: {comments['Critical']}\n", style="bold red"
                )
            if file_path != list(file_comments_map.keys())[-1]:
                feedback_text.append("\n")

        feedback_panel = Panel(
            Padding(feedback_text, (1, 2)),
            title="[bold violet]Feedback[/]",
            expand=False,
            border_style="violet",
        )

        console.print(feedback_panel)
        console.print("\n")

    else:
        console.print("\n")
        console.print(
            "Failed to fetch repository details. Please check your API key and project name.",
            style="bold red",
        )
        console.print("\n")


@app.command()
def feedback(project_name: str, file_path: str):
    api_key = keyring.get_password("deep-refactor", "api_key")
    if not api_key:
        console.print("You are not logged in. Please log in first.", style="bold red")
        raise typer.Exit()

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    url = f"http://localhost:8080/cli/repo-feedback/{project_name}"
    payload = {"filePath": file_path}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        comments = response.json()
        if not comments:
            console.print(
                f"No comments found for file '{file_path}' in project '{project_name}'.",
                style="bold yellow",
            )
        else:
            for comment in comments:
                # Format the line(s) text
                line_range = (
                    f"{comment['line_start']}"
                    if comment["line_start"] == comment["line_end"]
                    else f"{comment['line_start']} - {comment['line_end']}"
                )

                # Create the panel content with padding
                panel_content = Padding(
                    Text.assemble(
                        ("Type: ", "bold"),
                        f"{splitByCapital(comment['type'])}\n",
                        ("Severity: ", "bold"),
                        f"{comment['severity']}\n",
                        ("Comment: ", "bold"),
                        f"{escape(comment['comment_text'])}\n",
                        ("Recommendation: ", "bold"),
                        f"{escape(comment['recommendation'])}\n",
                        ("Line(s): ", "bold"),
                        line_range + "\n",
                    ),
                    (1, 2),
                )

                # Get the appropriate color for the border
                border_color = get_color(comment["type"])

                # Create and print the panel
                panel = Panel(
                    panel_content,
                    title=f"[bold]{splitByCapital(comment['type'])}[/]",
                    box=box.ROUNDED,
                    border_style=border_color,
                    expand=False,
                )
                console.print(panel)
    else:
        console.print(
            "Failed to fetch file comments. Please check your API key, project name, and file path.",
            style="bold red",
        )


# Helper Functions for AI Analysis
FEEDBACK_DIR = Path.home() / ".deep_refactor"
FEEDBACK_DIR.mkdir(exist_ok=True)
ANALYSIS_CHOICES = {
    "CodeQuality": "Clean, maintainable code",
    "DocumentationQuality": "Thorough, clear documentation",
    "BugDetection": "Identify potential bugs",
    "SecurityAnalysis": "Secure code practices",
    "TestCoverage": "Comprehensive testing assurance",
    "PerformanceAnalysis": "Optimize code efficiency",
    "AccessibilityAnalysis": "Enhanced user accessibility",
    "ArchitectureAnalysis": "Robust architectural design",
    "ContinuousIntegration": "Streamlined code integration",
}


def display_analysis_options():
    console.print("\n")
    console.print("Available Analysis Types:", style="bold underline")
    console.print("\n")
    for analysis_type, description in ANALYSIS_CHOICES.items():
        # Create a Text object and append the formatted parts
        text = Text()
        text.append(analysis_type, style=f"bold {get_color(analysis_type)}")
        text.append(": ")
        text.append(description)
        console.print(text)
    console.print("\n")


def read_file_content(file_path: str):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        console.print(f"File {file_path} not found.", style="bold red")
        raise typer.Exit()


def send_analysis_request(
    api_key: str, file_path: str, file_content: str, analysis_types: List[str]
):
    url = "http://localhost:8080/cli/analysis"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "file_path": file_path,
        "file_content": file_content,
        "analysisOptions": analysis_types,
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        console.print(
            f"Failed to analyze code: {response.json().get('error')}", style="bold red"
        )
        raise typer.Exit()
    return response.json()


def get_relative_path_hash(file_path: str):
    # Compute a hash based on the relative path from the current working directory
    current_dir = Path.cwd()
    absolute_path = Path(file_path).resolve()
    relative_path = absolute_path.relative_to(current_dir)
    return hashlib.sha256(str(relative_path).encode()).hexdigest()


def save_feedback_locally(file_path: str, feedback: dict):
    feedback_file_name = f"{get_relative_path_hash(file_path)}.json"
    feedback_file = FEEDBACK_DIR / feedback_file_name
    with feedback_file.open("w") as f:
        json.dump(feedback, f)


def retrieve_feedback(file_path: str):
    feedback_file_name = f"{get_relative_path_hash(file_path)}.json"
    feedback_file = FEEDBACK_DIR / feedback_file_name
    if feedback_file.exists():
        with feedback_file.open("r") as f:
            return json.loads(f.read())
    console.print(f"No saved feedback for file {file_path}.", style="bold yellow")
    return None


@app.command()
def analyze(file_path: str, analysis_types: List[str]):
    api_key = keyring.get_password("deep-refactor", "api_key")
    if not api_key:
        console.print("You are not logged in. Please log in first.", style="bold red")
        raise typer.Exit()

    # Validate analysis types
    if len(analysis_types) > 2:
        console.print(
            "You can only select up to 2 analysis types per call.", style="bold red"
        )
        display_analysis_options()
        raise typer.Exit()

    invalid_types = [t for t in analysis_types if t not in ANALYSIS_CHOICES]
    if invalid_types:
        console.print(
            f"Invalid analysis type(s): {', '.join(invalid_types)}", style="bold red"
        )
        display_analysis_options()
        raise typer.Exit()

    absolute_file_path = Path(file_path).resolve()
    file_content = read_file_content(str(absolute_file_path))

    if not file_content:
        console.print("File content is empty.", style="bold red")
        raise typer.Exit()

    feedback = send_analysis_request(api_key, file_path, file_content, analysis_types)

    if feedback is not None:
        save_feedback_locally(file_path, feedback)
        console.print("Feedback for the file:", style="bold green")
        for feedback_item in feedback:
            if "cleanedResponse" in feedback_item and feedback_item["cleanedResponse"]:
                for comment in feedback_item["cleanedResponse"]:
                    display_feedback_comment(comment)
    else:
        console.print("There was an issue analyzing the code, please try again.", style="bold red")
        

@app.command()
def local_feedback(file_path: str):
    absolute_file_path = Path(file_path).resolve()
    feedback_json = retrieve_feedback(str(absolute_file_path))

    if feedback_json:
        console.print("Feedback for the file:", style="bold green")
        for feedback_item in feedback_json:
            if "cleanedResponse" in feedback_item and feedback_item["cleanedResponse"]:
                for comment in feedback_item["cleanedResponse"]:
                    display_feedback_comment(comment)
    else:
        console.print(f"No saved feedback available for {file_path}.")


@app.command()
def clear_feedback():
    confirm = typer.confirm("Are you sure you want to clear all saved feedback?")
    if confirm:
        for feedback_file in FEEDBACK_DIR.glob("*.json"):
            feedback_file.unlink()
        console.print("All feedback files have been cleared.", style="bold green")
    else:
        console.print("Operation cancelled.", style="bold yellow")


app()