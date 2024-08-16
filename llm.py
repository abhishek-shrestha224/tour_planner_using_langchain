from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
import json

load_dotenv()

llm = AzureChatOpenAI(azure_deployment="gpt-4o",
                      api_version="2023-03-15-preview")

# ! ||--------------------------------------------------------------------------------||
# ! ||                                 Itinerary Chain                                ||
# ! ||--------------------------------------------------------------------------------||

itinerary_messages = [("system", """
    You are an expert travel planner. Given the following details, generate a detailed day-by-day travel itinerary. Include recommendations for activities, attractions, dining options, and accommodation for each day of the visit. Ensure that the itinerary aligns with the user's preferences, budget, and interests. 
    Generate the itinerary with the following format:
    Title for Day 1:
    What to do the whole day couple of sentences at most 30 words.

    Title for Day 2:
    What to do the whole day couple of sentences at most 30 words.

    Title for Day 3:
    What to do the whole day couple of sentences at most 30 words.

    The ouput must in the form of json array of objects where each object has plan title as key and daily activity as value
    """),
                      ("human", """
            **My Preferences:**

            - **Full Name:** {full_name}
            - **Country Of Origin:** {country_of_origin}
            - **Occupation:** {occupation}
            - **Main Purpose of Visit:** {main_purpose_of_visit}
            - **Travel Budget:** {travel_budget}
            - **Duration Of Visit:** {duration_of_visit}
            - **Preferred Attractions:** {preferred_attractions}
            - **Special Activities Interested In:** {special_activities}
            - **Number of People Traveling:** {number_of_people}
            - **Transportation & Accommodation Preferences:** {transportation_accommodation}
            - **Interested Places:** {interested_places}
            - **Weather Preference:** {weather_preference}
            - **Month(s) of Visit:** {months_of_visit}

            Make sure the activities and recommendations are suited to the my preferences and budget."""
                       )]

itinerary_prompt = ChatPromptTemplate.from_messages(itinerary_messages)

travel_info = {
    "full_name": "Abhishek Shrestha",
    "country_of_origin": "USA",
    "occupation": "Software Engineer",
    "main_purpose_of_visit": "Travel",
    "travel_budget": "$2000",
    "duration_of_visit": "90 days",
    "preferred_attractions": "Nature, Food",
    "special_activities": "Paragliding",
    "number_of_people": "2",
    "transportation_accommodation": "Flights, Hotels",
    "interested_places": "Pokhara, Kathmandu",
    "weather_preference": "Warm",
    "months_of_visit": "October"
}


def json_decode_array(json_str):
  start_index = json_str.find('[')
  end_index = json_str.rfind(']')

  trimmed_json_str = json_str[start_index:end_index + 1]

  try:
    return json.loads(trimmed_json_str)
  except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    return {}


itinerary = RunnableLambda(lambda x: json_decode_array(x))

itinerary_chain = itinerary_prompt | llm | StrOutputParser() | itinerary

itinerary_result = itinerary_chain.invoke(travel_info)

print(itinerary_result)

# ! ||--------------------------------------------------------------------------------||
# ! ||                                 Guideline Chain                                ||
# ! ||--------------------------------------------------------------------------------||

guideline_messages = [
    ("system", """
      You are a travel guide for Nepal. Provide comprehensive advice to tourists on the following format:

      Rules and Regulations:
        Compare the rules and regulations between the tourist's home country and Nepal.
        Highlight key legal requirements, customs, and restrictions.

      Basic Guidelines and Practices:
        Describe local customs, cultural practices, and etiquette.
        Include tips on appropriate dress and behavior in public and religious places.

      Emergency Contacts:
        Provide contact information for local police, medical facilities, tourist assistance, and embassies or consulates.

      Ensure the advice is clear, relevant, and useful for tourists planning their visit to Nepal. give the advice in form of a json.
      """),
    ("human",
     "I am from {country}. What should I be mindful of when I am travelling to nepal"
     ),
]

guideline_prompt = ChatPromptTemplate.from_messages(guideline_messages)


def json_decode_map(json_str):
  start_index = json_str.find('{')
  end_index = json_str.rfind('}')

  trimmed_json_str = json_str[start_index:end_index + 1]

  try:
    return json.loads(trimmed_json_str)
  except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    return {}


guidelines = RunnableLambda(lambda x: json_decode_map(x))

guideline_chain = guideline_prompt | llm | StrOutputParser() | guidelines

guidelines_result = guideline_chain.invoke({"country": "USA"})

print(guidelines_result)
