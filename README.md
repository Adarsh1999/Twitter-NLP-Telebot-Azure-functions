# Twitter-NLP-Telebot-Azure-functions
🎉This repo just contains the code but further setup of the project as to be done by yourself which is little lengthy.

# Steps to Follow during the project:

###  While dealing with Azure Functions
- [Azure doc](#%20Twitter-NLP-Telebot-Azure-functions%20%F0%9F%8E%89This%20project%20contains%20my%20Demo%20during%20MSP%20meet%20on%20Azure%20Functions%20%20###%20Presentation%20link%20:%20https://bit.ly/2W3dMVx%E2%80%8B%20%20#%20Steps%20to%20Follow%20during%20the%20project:%20-%20Azure%20doc%5Bhttps://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-vs-code?pivots=programming-language-python%5D) this is the perfect article I feel for the start as even I can't explain better than this.
- **VVIMP** : make a venv in the empty directory that you select by typing `python -m venv venv` into terminal.
- Now for installing Azure Functions Core tools from [here](https://github.com/Azure/azure-functions-core-tools) and prefer to use chocolatey method as you can use npm without problem but with chocolatey it will be useful for future too specially for windows.
- You should have python which is at least 3.5 version but less than 3.8
- Your python should be (x64) architecture version.
- After deployment it to the Azure make a point clear in mind that your monitor don't refresh as you expect it too so debugging is not that straight forward.
- Most important thing in after Azure console you will have your own webhook callback url which will be like **https://(botname).azurewebsites.net/api/(HttpTriggerName)**
- Save it for future purpose.

### For creating telegram bot:
- Go to telegram and search `botfather`.
- Then follow the steps according to the bot father says but make sure you send a message as `/start` to him so that he can guide you further.
- Then type `/newbot` for making new bot.
- And then he will ask and other stuff and will finally give you out your API key.
- Now to register for the webhook type this url in your browser : 
**api. telegram. org/bot<your_token>/setWebHook?url=(your_azure_generated_url_mentioned_above)**/

#### Now you are all set to run the code with your own imaginary ideas. Thankyou..



