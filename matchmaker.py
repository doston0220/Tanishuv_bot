
class Matchmaker:
    def __init__(self):
        self.waiting_users = []
        self.pairs = {}

    async def add_user(self, user_id, update):
        if user_id in self.pairs:
            await update.message.reply_text("Siz allaqachon suhbatdasiz. /stop buyrug‘i bilan tugating.")
            return

        if user_id in self.waiting_users:
            await update.message.reply_text("Siz allaqachon kutyapsiz...")
            return

        if self.waiting_users:
            partner_id = self.waiting_users.pop(0)
            self.pairs[user_id] = partner_id
            self.pairs[partner_id] = user_id
            await update.message.reply_text("✅ Suhbatdosh topildi!")
            await update.get_bot().send_message(chat_id=partner_id, text="✅ Suhbatdosh topildi!")
        else:
            self.waiting_users.append(user_id)
            await update.message.reply_text("⏳ Kuting, suhbatdosh qidirilmoqda...")

    async def remove_user(self, user_id):
        partner_id = self.pairs.pop(user_id, None)
        if partner_id:
            self.pairs.pop(partner_id, None)
            return partner_id
        elif user_id in self.waiting_users:
            self.waiting_users.remove(user_id)
        return None

    def get_partner(self, user_id):
        return self.pairs.get(user_id)
