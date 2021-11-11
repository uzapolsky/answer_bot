import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument


def create_intent(project_id, display_name, training_phrases_parts, message_texts):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)

        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    response.raise_for_status()


def main():
    load_dotenv()
    project_id = os.environ['PROJECT_ID']
    training_file = os.environ['TRAINING_FILE']

    with open(training_file, 'r') as f:
        training_phrases = json.load(f)
    
    for display_name, phrases in training_phrases.items():
        questions = phrases['questions']
        answers = [phrases['answer']]
        try:
            create_intent(project_id, display_name, questions, answers)
        except InvalidArgument as e:
            continue


if __name__ == '__main__':
    main()