from openai import OpenAI #a ne pas commit

def ask_gpt(commande, file):
  # Ouvrir le fichier en mode lecture ('r' pour read)
  with open(file, 'r') as fichier:
      # Lire tout le contenu du fichier dans une variable
      contenu = fichier.read()

  client = OpenAI()

  Prompt = "this is a python code :\n" + contenu + "\n" + commande + "Format your response by: Showing the whole modified code"


  response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": Prompt}
    ]
  )

  answer = response.choices[0].message.content
  return answer

def extract_command(gptCommand):
      
  blocks = []
  temp = ""
  writing = False

  for line in gptCommand.splitlines():
    if line == "```" : 
      writing = False
      blocks.append(temp)
      temp = ""

    if writing :
      temp += line
      temp+="\n"

    if line == "```python" or line == "```yaml": 
      writing = True

  return blocks

def save_as(content, path):
  #use at the end of replace_2 as save_as(end_result, "file_path")
  with open(path, 'w') as file:
    file.write(content)
  print("file saved !")

#ask = ask_gpt("for the node bot add a new output position and a new input dig, for the node control_op add a new input position and a output dig", "graphs/dataflow.yml")
#ask = ask_gpt("When I receive a input position, I want to be able to go the GOAL_OBJECTIVE, send output coordinate if the bot needs to move and if the y of GOAL_OBJECTIVE is lower than the y of the input, send output dig to dig the ground", "control_op.py")
#ask = ask_gpt("when I get a text input, I want to read what's the text inside, if the text is dig then send a dig output, if it's jump send jump output, if it's drink send a drink output", "operators/control_op.py")
#ask = ask_gpt("when I get a jump input, make the bot jump, when I get a drink input use minecraft command to give to the bot an health potion and drink it, when I get a dig input dig the ground under the feet of the bot", "operators/bot.py")
ask = ask_gpt("I have some errors in the code, but I don't know where, so put some print inside to check for errors", "operators/microphone_op.py")

save_as(extract_command(ask)[0], "operators/microphone_op.py")

"""
modifier bot pour activer une nouvelle fonctionnalité
modifier graph pour ajouter un nouveau noeud

note: le facon d'appeller les outputs et inputs pour eviter les erreurs 
"""