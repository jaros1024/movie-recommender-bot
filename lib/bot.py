from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


class STATE:
    SMALL_TALK = 0
    AWAITING_TITLE = 1


WELCOME_MESSAGE = "hi! i'm a Movie Expert Bot. how are you?"
GENERIC_MESSAGE = "You're a better expert than me. I'm not able to help you :("
NOT_FOUND_MESSAGE = "I don't know this movie. Are you sure the title is correct?"
MOVIES_MESSAGE = "Here's the list of movies that you might be interested in:\n{}"
HELP_MESSAGE = "Please give me a title of your favorite movie and I'll try to help you."
BYE_MESSAGE = "you're welcome! i'm always glad to help you."


small_talks = ['hi there!',
              'hi!',
              'how do you do?',
              'how are you?',
              'i\'m cool.',
              'fine, you?',
              'always cool.',
              'i\'m ok',
              'glad to hear that.',
              'i\'m fine',
              'glad to hear that.',
              'i feel awesome',
              'excellent, glad to hear that.',
              'not so good',
              'sorry to hear that.',
              'what\'s your name?',
              'i\'m movie expert bot. nice to meet you :)']

thanks_talks = ['thanks.',
             'thank you.',
             'you\'re welcome.']

help_talks = ['i need some help.',
              'can you help me?',
              'can you give me some proposals?',
              'can you give me a tip?',
              'can you give me a hand?']


class Bot:
    def __init__(self, recommender):
        self.recommender = recommender
        self.user_data = {}
        self.ai_bot = ChatBot(name='Movie Expert Bot', read_only=True,
                         logic_adapters=['chatterbot.logic.MathematicalEvaluation',
                                         'chatterbot.logic.BestMatch'])

        list_trainer = ListTrainer(self.ai_bot)
        for item in (small_talks, thanks_talks, help_talks):
            list_trainer.train(item)

    def process_message(self, user_id, message):
        if user_id not in self.user_data:
            self.user_data[user_id] = STATE.SMALL_TALK
            return WELCOME_MESSAGE

        if self.user_data[user_id] == STATE.AWAITING_TITLE:
            proposals = self.recommender.get_proposals(message)
            if proposals:
                msg = MOVIES_MESSAGE.format("\n".join(proposals))
                self.user_data[user_id] = STATE.SMALL_TALK
            else:
                msg = NOT_FOUND_MESSAGE
            return msg

        response = self.ai_bot.get_response(message)
        if str(response) in help_talks:
            self.user_data[user_id] = STATE.AWAITING_TITLE
            return HELP_MESSAGE
        if str(response) in thanks_talks:
            self.user_data[user_id] = STATE.SMALL_TALK
            return BYE_MESSAGE

        return response
