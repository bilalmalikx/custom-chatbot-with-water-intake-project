import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_message(user_input, response):
    with open("chat_log.txt", "a") as f:
        f.write(f"User: {user_input}\n")
        f.write(f"Assistant: {response}\n\n")

    
def log_error(error):
    logging.error(error)