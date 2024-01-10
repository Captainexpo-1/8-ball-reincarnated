import json
class Prompt:
    def __init__(self, path: str):
        self.loaded = json.load(open(path, 'r', encoding="utf-8"))

    def get_prompt(self):
        return self.loaded
    
    def get_prompt_with_input(self, input: str, system_txt: str = None):
        prompt = self.loaded
        prompt.append({"role":"user","content":input})
        if system_txt is not None:
            prompt.append({"role":"system","content":system_txt})
        return prompt
            
if __name__ == "__main__":
    prompt = Prompt("./prompt.json")
    print(prompt.get_prompt_with_input("Hello, this is a test of the prompt class!", "The 8-balls answer is unusually long."))