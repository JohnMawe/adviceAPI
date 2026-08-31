def response_builder(message, state="failed", data=None):
    if state.lower() == "success":
        return {
            "success": True,
            "message": message,
            "data": data
        }
    
    elif state.lower() == "failed":
        return {
            "success": False,
            "error": message
        }
    return None
