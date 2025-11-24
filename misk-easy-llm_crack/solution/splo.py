import requests
import sys
from collections import deque

URL = sys.argv[1]
PORT = 8888

s = requests.Session()

def choice_words_all(input_text, repeat=4):
    """Делает несколько запросов и собирает ВСЕ возможные фразы."""
    hint_words = set()

    for _ in range(repeat):
        headers={"Content-Type": "application/json"}
        data = {"input_text": input_text}
        final_res = None
        res = s.post(f"http://{URL}:{PORT}/api/input", headers=headers, json=data).json()

        final_res = res
        for word in res.get("hint_words", []):
            if word not in hint_words:
                hint_words.add(word)

    return hint_words, final_res


def search_flag(start_phrase=""):
    queue = deque([start_phrase])
    visited = set([start_phrase])

    while queue:
        phrase = queue.popleft()

        hint_words, result = choice_words_all(phrase)

        if "vka{" in result:
            print("FOUND FLAG:", result)
            return

        for tok in hint_words:
            new_phrase = (phrase + " " + tok).strip()

            if new_phrase not in visited:
                visited.add(new_phrase)
                queue.append(new_phrase)

        print("Checked:", phrase, "| Next:", hint_words)

    print("Flag not found.")


if __name__ == "__main__":
    search_flag("хакер взломал")
