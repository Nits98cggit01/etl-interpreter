import os
import openai
# openai.api_type = "azure"
# openai.api_base = "https://llmdemo.openai.azure.com/"
# openai.api_version = "2022-12-01"
# openai.api_key = "7ae7bffcd56d4ee89f742dcf20b67269"

# response = openai.Completion.create(
#   engine="gpt-35-turbo",
#   prompt="",
#   temperature=1,
#   max_tokens=100,
#   top_p=0.5,
#   frequency_penalty=0,
#   presence_penalty=0,
#   best_of=1,
#   stop=None)

# export OPENAI_API_TYPE = "azure"
# export OPENAI_API_VERSION = "2022-12-01"
# export OPENAI_API_BASE = "https://llmdemo.openai.azure.com/"
# export OPENAI_API_KEY = "7ae7bffcd56d4ee89f742dcf20b67269"
# export DEPLOYMENT_NAME = "gpt-35-turbo"


from codeinterpreterapi import CodeInterpreterSession, File


async def main():
    # context manager for auto start/stop of the session
    async with CodeInterpreterSession() as session:
        # define the user request
        user_request = "Analyze this dataset and plot something interesting about it."
        files = [
            File.from_path("C:\\Users\\NITINS\\Downloads\\Architect Information.xlsx"),
        ]

        # generate the response
        response = await session.generate_response(
            user_request, files=files
        )

        # output to the user
        print("AI: ", response.content)
        for file in response.files:
            file.show_image()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())