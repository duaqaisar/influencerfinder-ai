from services.influencer_service import InfluencerService

# Service that generates a chatbot-friendly response listing top influencers for a topic
class ChatbotService:
    def generate_response(self, topic: str, top_n: int = 5):
        # Initialize the influencer service
        service = InfluencerService()
        # Fetch top influencers matching the given topic
        influencers = service.find_influencers(topic, top_n)
        
        # If the service returned an error/message instead of a list, pass it through with no influencers
        if isinstance(influencers, dict) and "message" in influencers:
            return {"message": influencers["message"], "influencers": []}
        
        # Friendly text response
        # Start building a human-readable summary of the results
        lines = [f"Here are the top {len(influencers)} influencers for **{topic}**:\n"]
        
        # Add a formatted entry for each influencer
        for i, inf in enumerate(influencers, 1):
            lines.append(f"{i}. **@{inf['username']}** ({inf['platform']})")
            lines.append(f"   - Relevance: {inf['relevance_score']}")
            lines.append(f"   - Influence: {inf['influence_score']}")
            lines.append(f"   - Overall Score: {inf['overall_score']}")
            lines.append(f"   - Why: {inf.get('selection_reason', 'Strong match')}\n")
        
        # Combine all lines into a single formatted text block
        friendly_text = "\n".join(lines)
        
        # Return both the friendly text version and the raw structured data
        return {
            "friendly_message": friendly_text,
            "influencers": influencers,
            "topic": topic
        }
