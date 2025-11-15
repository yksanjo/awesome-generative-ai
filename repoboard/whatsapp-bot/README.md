# RepoBoard WhatsApp Bot

WhatsApp integration for RepoBoard. Choose between unofficial (free) or official (paid) options.

## Options Comparison

| Feature | WhatsApp Web (Unofficial) | Twilio (Official) |
|---------|---------------------------|-------------------|
| **Cost** | Free | $0.005 per message |
| **Setup** | Easy | Easy |
| **Reliability** | Medium | High |
| **Approval** | None | Twilio account |
| **Best For** | Personal use | Production |

## Option 1: WhatsApp Web (Unofficial) - Free

### Setup

1. **Install dependencies:**
```bash
pip install whatsapp-web.py
```

2. **Configure:**
```bash
# Add to .env
WHATSAPP_PHONE=+1234567890  # Your phone with country code
REPOBOARD_API_URL=http://localhost:8000
```

3. **Run:**
```bash
python bot.py
```

4. **Connect:**
   - Scan QR code with WhatsApp
   - Keep phone connected
   - Bot is ready!

### Limitations

- ⚠️ Unofficial API (can break)
- ⚠️ Requires phone to stay connected
- ⚠️ Against WhatsApp ToS (use at own risk)
- ✅ Free
- ✅ Easy setup

## Option 2: Twilio WhatsApp API - Official

### Setup

1. **Create Twilio account:**
   - Go to https://www.twilio.com
   - Sign up (free $15.50 credit)
   - Get WhatsApp-enabled number

2. **Install dependencies:**
```bash
pip install flask twilio requests
```

3. **Configure:**
```bash
# Add to .env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886  # Twilio's sandbox
REPOBOARD_API_URL=http://localhost:8000
```

4. **Run:**
```bash
python bot_twilio.py
```

5. **Set webhook:**
   - In Twilio console, set webhook URL
   - Use ngrok for local testing: `ngrok http 5000`
   - Set webhook to: `https://your-ngrok-url.ngrok.io/whatsapp`

6. **Join sandbox:**
   - Send "join [code]" to Twilio's WhatsApp number
   - Code shown in Twilio console

### Cost

- **Free tier:** $15.50 credit (3,100 messages)
- **After:** $0.005 per message
- **Example:** 1,000 messages/month = $5/month

### Advantages

- ✅ Official API
- ✅ Reliable
- ✅ Good documentation
- ✅ Free tier available

## Commands

Both bots support:

- `/start` or `start` - Welcome message
- `/boards` or `boards` - List all boards
- `/search <query>` - Search repositories
- `/trending` - Get trending repos
- `/help` - Show commands

## Deployment

### Local Testing

```bash
# Use ngrok for webhook
ngrok http 5000

# Update Twilio webhook to ngrok URL
```

### Production (Twilio)

```bash
# Deploy to Railway/Render
railway up

# Set webhook in Twilio console
# https://your-app.railway.app/whatsapp
```

## Cost Comparison

### Personal Use (You + Small Group)

**WhatsApp Web (Unofficial):**
- Cost: $0/month
- Messages: Unlimited
- Reliability: Medium

**Twilio:**
- Cost: $0-10/month (free tier covers most)
- Messages: 3,100 free, then $0.005 each
- Reliability: High

### Public Bot (100+ users)

**Twilio:**
- Cost: $20-100/month (depending on usage)
- Messages: $0.005 each
- Reliability: High

**WhatsApp Business API:**
- Cost: $0.005-0.01 per message
- Messages: Pay per use
- Reliability: Highest

## Recommendation

### For Personal Use
**Use: WhatsApp Web (Unofficial)**
- Free
- Easy setup
- Good enough for personal use

### For Small Group (10-50 people)
**Use: Twilio**
- $0-10/month (free tier)
- Reliable
- Easy setup

### For Public Bot (100+ users)
**Use: Twilio or WhatsApp Business API**
- Twilio: Easier setup
- Business API: More features

## Security Notes

⚠️ **WhatsApp Web (Unofficial):**
- Uses your personal WhatsApp
- Keep phone secure
- Don't share bot publicly
- Use only for personal/small group

✅ **Twilio:**
- Official API
- Secure
- Can be public
- Production-ready

## Next Steps

1. Choose your option (Web or Twilio)
2. Set up according to instructions
3. Test with yourself first
4. Share with small group
5. Scale if needed

