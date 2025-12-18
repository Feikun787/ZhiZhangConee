

class SupportMe:
    async def support_me(self,msg,nub):
        if msg.raw_message == "赞我":
            nub1 = 0
            a = await self.api.send_like(msg.user_id,10)
            if a['status'] == 'ok':
                nub1 += 1
            text = f'给你点赞{nub1*10}次'
            if nub1 == 0:
                text = '你已赞过'
            return {'try': 'text', "text": text, 'nub': nub}