# src/recommendations.py

def generate_recommendations(metrics, funnel_by_channel, room_type_conversion, user_stage_conversion):
    """
    Generates actionable recommendations and insights based on booking funnel metrics, room type conversion rates,
    user stage conversion rates, and average response time.
    Args:
        metrics (dict): Dictionary containing overall booking metrics, including 'booking_rate' (float) and 'avg_response_time' (float, in hours).
        funnel_by_channel (pandas.Series): Series indexed by booking channel (e.g., 'instant_book') with corresponding conversion rates (float).
        room_type_conversion (pandas.Series): Series indexed by room type (e.g., 'entire home', 'private room') with corresponding booking rates (float).
        user_stage_conversion (dict): Dictionary with user stages as keys (e.g., 'new', 'past booker') and their conversion rates (float).
    Returns:
        list of dict: A list of recommendations, each as a dictionary with 'insight' and 'recommendation' keys.
    """
    recommendations = []

    # 1. Instant Book performance
    if 'instant_book' in funnel_by_channel.index:
        ib_rate = funnel_by_channel.loc['instant_book']
        if ib_rate > metrics['booking_rate'] * 1.5:
            recommendations.append({
                "insight": f"Instant Book has a conversion rate of {ib_rate:.2%}, significantly higher than the average {metrics['booking_rate']:.2%}.",
                "recommendation": "Encourage more hosts to opt in to Instant Book. Consider incentives or feature promotions."
            })

    # 2. Room type performance
    top_room = room_type_conversion.idxmax()
    top_rate = room_type_conversion.max()
    low_room = room_type_conversion.idxmin()
    low_rate = room_type_conversion.min()

    recommendations.append({
        "insight": f"{top_room.title()}s have the highest booking rate at {top_rate:.2%}. {low_room.title()}s convert at only {low_rate:.2%}.",
        "recommendation": f"Surface more {top_room}s in search results, or improve the visibility of better-converting room types."
    })

    # 3. New vs past user conversion
    new_user_rate = user_stage_conversion.get('new', None)
    past_user_rate = user_stage_conversion.get('past booker', None)

    if new_user_rate and past_user_rate:
        if past_user_rate > new_user_rate * 1.3:
            recommendations.append({
                "insight": f"Past bookers convert at {past_user_rate:.2%}, while new users only convert at {new_user_rate:.2%}.",
                "recommendation": "Improve onboarding and trust-building for new users (e.g., better messaging, UI nudges, social proof)."
            })

    # 4. Response time
    if metrics['avg_response_time'] > 12:
        recommendations.append({
            "insight": f"Average host response time is {metrics['avg_response_time']:.1f} hours, which may be too slow for real-time booking expectations.",
            "recommendation": "Improve host responsiveness — consider SMS nudges, response SLAs, or reward fast responders."
        })

    return recommendations
