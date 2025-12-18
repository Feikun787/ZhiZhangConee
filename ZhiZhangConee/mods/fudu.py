

class Fudu:
    async def main(self, msg,nub):
        if str(msg.raw_message).split(':')[0] == "复读":
            return {'try': 'text', "text": str(msg.raw_message).split(':')[-1], 'nub': nub}