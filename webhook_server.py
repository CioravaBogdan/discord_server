from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel
import asyncio
import logging
import uvicorn
import discord
from typing import Optional, List, Dict, Any
from config import Config, setup_logging

# Setup logging
logger = setup_logging()

# Pydantic models for request validation
class DiscordMessage(BaseModel):
    channel_id: int
    content: str
    embeds: Optional[List[Dict[str, Any]]] = None

class DiscordEmbed(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    color: Optional[int] = None
    url: Optional[str] = None
    thumbnail: Optional[Dict[str, str]] = None
    image: Optional[Dict[str, str]] = None
    fields: Optional[List[Dict[str, Any]]] = None

# FastAPI app
app = FastAPI(
    title="Discord Bot Webhook Server",
    description="Webhook server pentru bot-ul Discord care primește comenzi de la n8n",
    version="1.0.0"
)

# Global reference to bot
discord_bot = None

def set_bot_instance(bot):
    """Set the Discord bot instance"""
    global discord_bot
    discord_bot = bot

# Health check endpoint for Docker
@app.get("/health")
async def health_check():
    """Health check endpoint for Docker containers"""
    try:
        # Check if bot is connected
        bot_status = "connected" if discord_bot and discord_bot.client.is_ready() else "disconnected"
        
        return {
            "status": "healthy",
            "bot_status": bot_status,
            "webhook_port": Config.WEBHOOK_PORT,
            "docker_mode": Config.IS_DOCKER
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

@app.post("/send-message")
async def send_message(request: Request, message: DiscordMessage, background_tasks: BackgroundTasks):
    """Send a message to Discord via webhook from n8n"""
    if not discord_bot:
        raise HTTPException(status_code=503, detail="Discord bot not available")
    
    # Check if message comes from n8n automation
    source = request.headers.get("X-Source", "").lower()
    is_n8n_automation = source == "n8n-automation"
    
    logger.info(f"Webhook primit pentru canalul {message.channel_id}: {message.content[:50]}...")
    if is_n8n_automation:
        logger.info("🤖 Mesaj detectat ca fiind de la n8n automation")
    
    # Add special prefix for n8n messages to prevent re-processing
    content = message.content
    if is_n8n_automation and not content.startswith("🤖🔒"):
        content = f"🤖🔒 {content}"
        logger.info("🔒 Adăugat prefix anti-buclă pentru mesaj n8n")
    
    # Process embeds if provided
    discord_embeds = None
    if message.embeds:
        discord_embeds = []
        for embed_data in message.embeds:
            embed = discord.Embed(
                title=embed_data.get('title'),
                description=embed_data.get('description'),
                color=embed_data.get('color'),
                url=embed_data.get('url')
            )
            
            # Add thumbnail
            if embed_data.get('thumbnail'):
                embed.set_thumbnail(url=embed_data['thumbnail'].get('url'))
            
            # Add image
            if embed_data.get('image'):
                embed.set_image(url=embed_data['image'].get('url'))
            
            # Add fields
            if embed_data.get('fields'):
                for field in embed_data['fields']:
                    embed.add_field(
                        name=field.get('name', ''),
                        value=field.get('value', ''),
                        inline=field.get('inline', False)
                    )
            
            discord_embeds.append(embed)
      # Send message asynchronously using the Discord bot's loop
    try:
        # Schedule the message sending in the Discord bot's event loop
        channel = discord_bot.client.get_channel(message.channel_id)
        if not channel:
            raise HTTPException(status_code=404, detail=f"Channel with ID {message.channel_id} not found")
          # Create the message coroutine and run it in the Discord event loop
        loop = discord_bot.client.loop
        if loop and loop.is_running():
            # Use asyncio to schedule the task in the bot's event loop
            future = asyncio.run_coroutine_threadsafe(
                channel.send(content=content, embeds=discord_embeds),
                loop
            )
            # Wait for the result with a timeout
            future.result(timeout=10)
            logger.info(f"Mesaj trimis în canalul {channel.name}")
            return {"status": "success", "message": "Message sent to Discord"}
        else:
            raise HTTPException(status_code=503, detail="Discord bot event loop not available")
            
    except Exception as e:
        logger.error(f"Eroare la trimiterea mesajului: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

@app.post("/webhook/n8n")
async def n8n_webhook(request: Request, data: Dict[str, Any]):
    """Generic webhook endpoint for n8n to send data"""
    
    # Check if request comes from n8n automation
    source = request.headers.get("X-Source", "").lower()
    is_n8n_automation = source == "n8n-automation"
    
    logger.info(f"Date primite de la n8n: {data}")
    if is_n8n_automation:
        logger.info("🤖 Request identificat ca fiind de la n8n automation")
    
    # Process the data from n8n
    # This can be customized based on your n8n workflow needs
    
    if "action" in data:
        action = data["action"]
        
        if action == "send_message":
            # Extract message data
            channel_id = data.get("channel_id")
            content = data.get("content", "")
            embeds = data.get("embeds")
            
            if not channel_id:
                raise HTTPException(status_code=400, detail="channel_id is required")
            
            # Add anti-loop prefix for n8n automation messages
            if is_n8n_automation and not content.startswith("🤖🔒"):
                content = f"🤖🔒 {content}"
                logger.info("🔒 Adăugat prefix anti-buclă pentru mesaj n8n")
            
            message = DiscordMessage(
                channel_id=channel_id,
                content=content,
                embeds=embeds
            )
            
            return await send_message(request, message, BackgroundTasks())
    
    return {"status": "received", "data": data}

def run_webhook_server():
    """Run the webhook server"""
    logger.info(f"Pornesc serverul webhook pe {Config.WEBHOOK_HOST}:{Config.WEBHOOK_PORT}")
    uvicorn.run(
        app,
        host=Config.WEBHOOK_HOST,
        port=Config.WEBHOOK_PORT,
        log_level=Config.LOG_LEVEL.lower()
    )

if __name__ == "__main__":
    run_webhook_server()
