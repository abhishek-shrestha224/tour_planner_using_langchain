from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

llm = AzureChatOpenAI(azure_deployment="gpt-4o",
                      api_version="2023-03-15-preview")

message = [("system", """
    You are an expert travel planner. Given the following details, generate a detailed day-by-day travel itinerary. Include recommendations for activities, attractions, dining options, and accommodation for each day of the visit. Ensure that the itinerary aligns with the user's preferences, budget, and interests. 
    Generate the itinerary with the following format:
    - **Day 1:**
    What to do the whole day couple of sentences at most 30 words.

    - **Day 3:**
    What to do the whole day couple of sentences at most 30 words.

    - **Day n:**
    What to do the whole day couple of sentences at most 30 words.
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

prompt_template = ChatPromptTemplate.from_messages(message)


# Function to generate itinerary
def generate_itinerary(travel_info):
  prompt = prompt_template.invoke(travel_info)
  response = llm.invoke(prompt)
  return response.content


travel_info = {
    "full_name": "Abhishek Shrestha",
    "country_of_origin": "USA",
    "occupation": "Software Engineer",
    "main_purpose_of_visit": "Travel",
    "travel_budget": "$2000",
    "duration_of_visit": "7 days",
    "preferred_attractions": "Nature, Food",
    "special_activities": "Paragliding",
    "number_of_people": "2",
    "transportation_accommodation": "Flights, Hotels",
    "interested_places": "Pokhara, Kathmandu",
    "weather_preference": "Warm",
    "months_of_visit": "October"
}

itinerary = generate_itinerary(travel_info)
print(itinerary)
