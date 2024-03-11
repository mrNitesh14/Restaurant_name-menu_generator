import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from secret_key import OPENAI_API_KEY  # Make sure to replace this with your actual API key

# Set the OpenAI API key using the environment variable
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Initialize OpenAI with the specified temperature
llm = OpenAI(temperature=0.7)

def generate_restaurant_name_and_items(cuisine):
    # Prompt template for generating restaurant name
    prompt_template_name = PromptTemplate(
        input_variables=['cuisine'],
        template="I want to open a restaurant for {cuisine} food, suggest me a fancy name for this."
    )
    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="restaurant_name")

    # Prompt template for generating menu items
    prompt_template_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="Suggest me some menu items for {restaurant_name}. Return it as a comma-separated value."
    )
    food_items_chain = LLMChain(llm=llm, prompt=prompt_template_items, output_key="menu_items")

    # Create a sequential chain with both name and menu items generation
    chain = SequentialChain(
        chains=[name_chain, food_items_chain],
        input_variables=["cuisine"],
        output_variables=["restaurant_name", "menu_items"]
    )

    response = chain({'cuisine': cuisine})
    return response

if __name__ == '__main__':
    # Replace 'Indian' with the desired cuisine
    result = generate_restaurant_name_and_items('Indian')
    print(result)
